import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import requests
import threading
import queue
from datetime import datetime
import pandas as pd
from pathlib import Path
import logging
import time
import hashlib
import socket
import dns.resolver
import whois
from urllib.parse import urlparse

class ThreatIntelligence:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.api_keys = self.config_manager.get_setting("threat_intelligence", "api_keys")
        self.update_interval = self.config_manager.get_setting("threat_intelligence", "update_interval")
        self.cache_duration = self.config_manager.get_setting("threat_intelligence", "cache_duration")
        self.max_requests = self.config_manager.get_setting("threat_intelligence", "max_requests_per_minute")
        
        self.cache = {}
        self.request_times = []
        self.search_queue = queue.Queue()
        self.searching = False
        self.search_thread = None
        
        # Initialize logging
        self.logger = logging.getLogger("ThreatIntelligence")
        
        # Create cache directory
        self.cache_dir = Path("cache/threat_intelligence")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def create_ui(self, parent):
        """Create the threat intelligence UI"""
        # Create main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create search frame
        search_frame = ttk.LabelFrame(main_frame, text="Threat Intelligence Search")
        search_frame.pack(fill='x', padx=5, pady=5)
        
        # Create search input
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side='left', padx=5)
        
        # Create search type
        self.search_type = tk.StringVar(value="ip")
        ttk.Radiobutton(search_frame, text="IP", variable=self.search_type, value="ip").pack(side='left', padx=5)
        ttk.Radiobutton(search_frame, text="Domain", variable=self.search_type, value="domain").pack(side='left', padx=5)
        ttk.Radiobutton(search_frame, text="Hash", variable=self.search_type, value="hash").pack(side='left', padx=5)
        
        # Create search button
        search_btn = ttk.Button(search_frame, text="Search", command=self.start_search)
        search_btn.pack(side='left', padx=5)
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create results tab
        self.create_results_tab()
        
        # Create history tab
        self.create_history_tab()
        
        # Create settings tab
        self.create_settings_tab()
        
        # Add export button
        export_btn = ttk.Button(main_frame, text="Export Results", command=self.export_results)
        export_btn.pack(pady=5, anchor='ne')
    
    def create_results_tab(self):
        """Create the results tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Search Results')
        
        # Create results tree
        self.results_tree = ttk.Treeview(frame, columns=(
            'source', 'type', 'score', 'details', 'timestamp'
        ), show='headings')
        
        # Set column headings
        self.results_tree.heading('source', text='Source')
        self.results_tree.heading('type', text='Type')
        self.results_tree.heading('score', text='Score')
        self.results_tree.heading('details', text='Details')
        self.results_tree.heading('timestamp', text='Timestamp')
        
        # Set column widths
        self.results_tree.column('source', width=100)
        self.results_tree.column('type', width=80)
        self.results_tree.column('score', width=80)
        self.results_tree.column('details', width=300)
        self.results_tree.column('timestamp', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack results tree
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add right-click menu
        self.create_context_menu(self.results_tree)
    
    def create_history_tab(self):
        """Create the history tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Search History')
        
        # Create history tree
        self.history_tree = ttk.Treeview(frame, columns=(
            'query', 'type', 'timestamp', 'results'
        ), show='headings')
        
        # Set column headings
        self.history_tree.heading('query', text='Query')
        self.history_tree.heading('type', text='Type')
        self.history_tree.heading('timestamp', text='Timestamp')
        self.history_tree.heading('results', text='Results')
        
        # Set column widths
        self.history_tree.column('query', width=200)
        self.history_tree.column('type', width=80)
        self.history_tree.column('timestamp', width=150)
        self.history_tree.column('results', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack history tree
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add right-click menu
        self.create_context_menu(self.history_tree)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Settings')
        
        # Create settings form
        settings_frame = ttk.LabelFrame(frame, text="API Settings")
        settings_frame.pack(fill='x', padx=5, pady=5)
        
        # VirusTotal API key
        ttk.Label(settings_frame, text="VirusTotal API Key:").pack(anchor='w', padx=5, pady=2)
        self.vt_key_var = tk.StringVar(value=self.api_keys.get('virustotal', ''))
        ttk.Entry(settings_frame, textvariable=self.vt_key_var, width=50).pack(anchor='w', padx=5, pady=2)
        
        # AbuseIPDB API key
        ttk.Label(settings_frame, text="AbuseIPDB API Key:").pack(anchor='w', padx=5, pady=2)
        self.abuse_key_var = tk.StringVar(value=self.api_keys.get('abuseipdb', ''))
        ttk.Entry(settings_frame, textvariable=self.abuse_key_var, width=50).pack(anchor='w', padx=5, pady=2)
        
        # AlienVault API key
        ttk.Label(settings_frame, text="AlienVault API Key:").pack(anchor='w', padx=5, pady=2)
        self.alienvault_key_var = tk.StringVar(value=self.api_keys.get('alienvault', ''))
        ttk.Entry(settings_frame, textvariable=self.alienvault_key_var, width=50).pack(anchor='w', padx=5, pady=2)
        
        # Save button
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.pack(anchor='w', padx=5, pady=5)
    
    def create_context_menu(self, tree):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(tree, tearoff=0)
        self.context_menu.add_command(label="View Details", command=lambda: self.view_details(tree))
        self.context_menu.add_command(label="Copy to Clipboard", command=lambda: self.copy_to_clipboard(tree))
        self.context_menu.add_command(label="Export Selection", command=lambda: self.export_selection(tree))
        
        tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show the context menu on right-click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def start_search(self):
        """Start a threat intelligence search"""
        query = self.search_var.get().strip()
        search_type = self.search_type.get()
        
        if not query:
            messagebox.showerror("Error", "Please enter a search query")
            return
        
        # Validate query based on type
        if search_type == "ip" and not self.is_valid_ip(query):
            messagebox.showerror("Error", "Invalid IP address")
            return
        elif search_type == "domain" and not self.is_valid_domain(query):
            messagebox.showerror("Error", "Invalid domain")
            return
        elif search_type == "hash" and not self.is_valid_hash(query):
            messagebox.showerror("Error", "Invalid hash")
            return
        
        # Add to search queue
        self.search_queue.put((query, search_type))
        
        # Start search thread if not already running
        if not self.searching:
            self.searching = True
            self.search_thread = threading.Thread(target=self.run_search)
            self.search_thread.start()
    
    def run_search(self):
        """Run threat intelligence search"""
        try:
            while not self.search_queue.empty():
                query, search_type = self.search_queue.get()
                
                # Check cache
                cache_key = f"{search_type}:{query}"
                if cache_key in self.cache:
                    results = self.cache[cache_key]
                else:
                    # Perform search
                    results = self.search_threat_intelligence(query, search_type)
                    
                    # Cache results
                    self.cache[cache_key] = results
                    self.save_to_cache(cache_key, results)
                
                # Update UI
                self.update_results(query, search_type, results)
                
                # Add to history
                self.add_to_history(query, search_type, results)
            
            self.searching = False
        
        except Exception as e:
            self.logger.error(f"Error in search: {str(e)}")
            self.searching = False
    
    def search_threat_intelligence(self, query, search_type):
        """Search threat intelligence sources"""
        results = []
        
        try:
            # Check rate limits
            self.check_rate_limits()
            
            # Search VirusTotal
            if self.api_keys.get('virustotal'):
                vt_results = self.search_virustotal(query, search_type)
                results.extend(vt_results)
            
            # Search AbuseIPDB
            if self.api_keys.get('abuseipdb'):
                abuse_results = self.search_abuseipdb(query, search_type)
                results.extend(abuse_results)
            
            # Search AlienVault
            if self.api_keys.get('alienvault'):
                alienvault_results = self.search_alienvault(query, search_type)
                results.extend(alienvault_results)
            
            # Add local analysis
            local_results = self.analyze_locally(query, search_type)
            results.extend(local_results)
        
        except Exception as e:
            self.logger.error(f"Error searching threat intelligence: {str(e)}")
        
        return results
    
    def search_virustotal(self, query, search_type):
        """Search VirusTotal"""
        results = []
        
        try:
            headers = {
                "x-apikey": self.api_keys['virustotal']
            }
            
            if search_type == "ip":
                url = f"https://www.virustotal.com/api/v3/ip_addresses/{query}"
            elif search_type == "domain":
                url = f"https://www.virustotal.com/api/v3/domains/{query}"
            elif search_type == "hash":
                url = f"https://www.virustotal.com/api/v3/files/{query}"
            
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if response.status_code == 200:
                # Extract relevant information
                if search_type in ["ip", "domain"]:
                    stats = data['data']['attributes']['last_analysis_stats']
                    score = (stats['malicious'] + stats['suspicious']) / (stats['malicious'] + stats['suspicious'] + stats['undetected'] + stats['harmless']) * 100
                    
                    results.append({
                        'source': 'VirusTotal',
                        'type': search_type,
                        'score': score,
                        'details': f"Malicious: {stats['malicious']}, Suspicious: {stats['suspicious']}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                elif search_type == "hash":
                    stats = data['data']['attributes']['last_analysis_stats']
                    score = (stats['malicious'] + stats['suspicious']) / (stats['malicious'] + stats['suspicious'] + stats['undetected'] + stats['harmless']) * 100
                    
                    results.append({
                        'source': 'VirusTotal',
                        'type': search_type,
                        'score': score,
                        'details': f"Malicious: {stats['malicious']}, Suspicious: {stats['suspicious']}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        except Exception as e:
            self.logger.error(f"Error searching VirusTotal: {str(e)}")
        
        return results
    
    def search_abuseipdb(self, query, search_type):
        """Search AbuseIPDB"""
        results = []
        
        try:
            if search_type == "ip":
                url = "https://api.abuseipdb.com/api/v2/check"
                params = {
                    'ipAddress': query,
                    'maxAgeInDays': 90
                }
                headers = {
                    'Key': self.api_keys['abuseipdb'],
                    'Accept': 'application/json'
                }
                
                response = requests.get(url, params=params, headers=headers)
                data = response.json()
                
                if response.status_code == 200:
                    results.append({
                        'source': 'AbuseIPDB',
                        'type': search_type,
                        'score': data['data']['abuseConfidenceScore'],
                        'details': f"Total Reports: {data['data']['totalReports']}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        except Exception as e:
            self.logger.error(f"Error searching AbuseIPDB: {str(e)}")
        
        return results
    
    def search_alienvault(self, query, search_type):
        """Search AlienVault OTX"""
        results = []
        
        try:
            headers = {
                'X-OTX-API-KEY': self.api_keys['alienvault']
            }
            
            if search_type == "ip":
                url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{query}/general"
            elif search_type == "domain":
                url = f"https://otx.alienvault.com/api/v1/indicators/domain/{query}/general"
            elif search_type == "hash":
                url = f"https://otx.alienvault.com/api/v1/indicators/file/{query}/general"
            
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if response.status_code == 200:
                pulse_count = data.get('pulse_info', {}).get('count', 0)
                results.append({
                    'source': 'AlienVault OTX',
                    'type': search_type,
                    'score': pulse_count * 10,  # Simple scoring based on pulse count
                    'details': f"Pulse Count: {pulse_count}",
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        except Exception as e:
            self.logger.error(f"Error searching AlienVault: {str(e)}")
        
        return results
    
    def analyze_locally(self, query, search_type):
        """Perform local analysis"""
        results = []
        
        try:
            if search_type == "ip":
                # Check if IP is private
                is_private = self.is_private_ip(query)
                if is_private:
                    results.append({
                        'source': 'Local Analysis',
                        'type': search_type,
                        'score': 0,
                        'details': "Private IP Address",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                # Try reverse DNS
                try:
                    hostname = socket.gethostbyaddr(query)[0]
                    results.append({
                        'source': 'Local Analysis',
                        'type': search_type,
                        'score': 0,
                        'details': f"Reverse DNS: {hostname}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except:
                    pass
            
            elif search_type == "domain":
                # Check DNS records
                try:
                    a_records = dns.resolver.resolve(query, 'A')
                    results.append({
                        'source': 'Local Analysis',
                        'type': search_type,
                        'score': 0,
                        'details': f"A Records: {', '.join(str(r) for r in a_records)}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except:
                    pass
                
                # Check WHOIS
                try:
                    w = whois.whois(query)
                    results.append({
                        'source': 'Local Analysis',
                        'type': search_type,
                        'score': 0,
                        'details': f"Registrar: {w.registrar}, Created: {w.creation_date}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except:
                    pass
            
            elif search_type == "hash":
                # Check if hash is in local database
                # This is a placeholder for actual hash checking logic
                pass
        
        except Exception as e:
            self.logger.error(f"Error in local analysis: {str(e)}")
        
        return results
    
    def update_results(self, query, search_type, results):
        """Update the results view"""
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results
        for result in results:
            self.results_tree.insert('', 'end', values=(
                result['source'],
                result['type'],
                f"{result['score']:.1f}",
                result['details'],
                result['timestamp']
            ))
    
    def add_to_history(self, query, search_type, results):
        """Add search to history"""
        self.history_tree.insert('', 0, values=(
            query,
            search_type,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            len(results)
        ))
    
    def save_settings(self):
        """Save API settings"""
        try:
            # Update API keys
            self.api_keys['virustotal'] = self.vt_key_var.get()
            self.api_keys['abuseipdb'] = self.abuse_key_var.get()
            self.api_keys['alienvault'] = self.alienvault_key_var.get()
            
            # Save to config
            self.config_manager.set_setting("threat_intelligence", "api_keys", self.api_keys)
            
            messagebox.showinfo("Success", "Settings saved successfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def view_details(self, tree):
        """View detailed information"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get selected item
        item = tree.item(selected[0])
        values = item['values']
        
        # Create details dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Details - {values[0]}")
        dialog.geometry("600x400")
        
        # Create details view
        details_frame = ttk.Frame(dialog)
        details_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add information
        ttk.Label(details_frame, text=f"Source: {values[0]}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Type: {values[1]}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Score: {values[2]}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Timestamp: {values[4]}").pack(anchor='w')
        
        ttk.Label(details_frame, text="Details:").pack(anchor='w', pady=(10, 5))
        details_text = tk.Text(details_frame, height=10, wrap='word')
        details_text.insert('1.0', values[3])
        details_text.pack(fill='x', padx=5)
    
    def copy_to_clipboard(self, tree):
        """Copy selected information to clipboard"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get selected item
        item = tree.item(selected[0])
        values = item['values']
        
        # Format information
        text = f"Source: {values[0]}\n"
        text += f"Type: {values[1]}\n"
        text += f"Score: {values[2]}\n"
        text += f"Details: {values[3]}\n"
        text += f"Timestamp: {values[4]}"
        
        # Copy to clipboard
        self.parent.clipboard_clear()
        self.parent.clipboard_append(text)
    
    def export_selection(self, tree):
        """Export selected information"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save As...'
        )
        
        if filename:
            # Get selected items
            data = []
            for item in selected:
                data.append(tree.item(item)['values'])
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=['Source', 'Type', 'Score', 'Details', 'Timestamp'])
            
            # Save to CSV
            df.to_csv(filename, index=False)
    
    def export_results(self):
        """Export all results"""
        # Get filename
        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save Results As...'
        )
        
        if filename:
            # Get all items
            data = []
            for item in self.results_tree.get_children():
                data.append(self.results_tree.item(item)['values'])
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=['Source', 'Type', 'Score', 'Details', 'Timestamp'])
            
            # Save to CSV
            df.to_csv(filename, index=False)
    
    def check_rate_limits(self):
        """Check and enforce API rate limits"""
        current_time = time.time()
        
        # Remove old request times
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # Check if we're over the limit
        if len(self.request_times) >= self.max_requests:
            # Wait until we can make another request
            sleep_time = 60 - (current_time - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Add current request
        self.request_times.append(current_time)
    
    def save_to_cache(self, key, results):
        """Save results to cache file"""
        try:
            cache_file = self.cache_dir / f"{key}.json"
            
            # Save results
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'results': results
                }, f, indent=4)
        
        except Exception as e:
            self.logger.error(f"Error saving to cache: {str(e)}")
    
    def is_valid_ip(self, ip):
        """Check if string is a valid IP address"""
        try:
            socket.inet_aton(ip)
            return True
        except:
            return False
    
    def is_valid_domain(self, domain):
        """Check if string is a valid domain"""
        try:
            result = urlparse(domain)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def is_valid_hash(self, hash_str):
        """Check if string is a valid hash"""
        return len(hash_str) in [32, 40, 64] and all(c in '0123456789abcdef' for c in hash_str.lower())
    
    def is_private_ip(self, ip):
        """Check if IP address is private"""
        try:
            ip_parts = list(map(int, ip.split('.')))
            return (
                ip_parts[0] == 10 or
                (ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31) or
                (ip_parts[0] == 192 and ip_parts[1] == 168)
            )
        except:
            return False
    
    def update_ui(self):
        """Update the UI components"""
        pass  # No real-time updates needed for this module 