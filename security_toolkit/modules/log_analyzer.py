import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import json
import threading
import queue
from datetime import datetime
import pandas as pd
from pathlib import Path
import logging

class LogAnalyzer:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.log_patterns = self.load_log_patterns()
        self.alert_rules = self.load_alert_rules()
        self.analysis_queue = queue.Queue()
        self.analyzing = False
        self.analysis_thread = None
        self.log_data = []
        self.alerts = []
        
        # Initialize logging
        self.logger = logging.getLogger("LogAnalyzer")
    
    def load_log_patterns(self):
        """Load log pattern definitions"""
        try:
            pattern_path = Path("config/log_patterns.json")
            if pattern_path.exists():
                with open(pattern_path, 'r') as f:
                    return json.load(f)
            return {
                "ssh": {
                    "pattern": r"sshd.*Failed password for (\S+) from (\S+)",
                    "type": "authentication",
                    "severity": "high"
                },
                "apache": {
                    "pattern": r"(\S+) - - \[(.*?)\] \"(\S+) (\S+) (\S+)\" (\d+) (\d+)",
                    "type": "web_access",
                    "severity": "medium"
                },
                "system": {
                    "pattern": r"kernel: (.*?)",
                    "type": "system",
                    "severity": "low"
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading log patterns: {str(e)}")
            return {}
    
    def load_alert_rules(self):
        """Load alert rules"""
        try:
            rules_path = Path("config/alert_rules.json")
            if rules_path.exists():
                with open(rules_path, 'r') as f:
                    return json.load(f)
            return {
                "multiple_failures": {
                    "condition": "count > 5",
                    "timeframe": "5m",
                    "severity": "high",
                    "message": "Multiple authentication failures detected"
                },
                "suspicious_ip": {
                    "condition": "ip in blacklist",
                    "severity": "high",
                    "message": "Suspicious IP address detected"
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading alert rules: {str(e)}")
            return {}
    
    def create_ui(self, parent):
        """Create the log analyzer UI"""
        # Create main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create control frame
        control_frame = ttk.LabelFrame(main_frame, text="Log Analysis Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # File selection
        ttk.Label(control_frame, text="Log File:").pack(side='left', padx=5)
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(control_frame, textvariable=self.file_var, width=50)
        self.file_entry.pack(side='left', padx=5)
        ttk.Button(control_frame, text="Browse", command=self.browse_file).pack(side='left', padx=5)
        
        # Analysis type selection
        ttk.Label(control_frame, text="Analysis Type:").pack(side='left', padx=5)
        self.analysis_type_var = tk.StringVar(value="all")
        analysis_types = ttk.Combobox(control_frame, textvariable=self.analysis_type_var,
                                    values=["all", "authentication", "web_access", "system"],
                                    state="readonly")
        analysis_types.pack(side='left', padx=5)
        
        # Start analysis button
        self.start_button = ttk.Button(control_frame, text="Start Analysis", command=self.start_analysis)
        self.start_button.pack(side='left', padx=5)
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create log view tab
        self.create_log_view_tab()
        
        # Create alerts tab
        self.create_alerts_tab()
        
        # Create statistics tab
        self.create_statistics_tab()
        
        # Add export button
        export_btn = ttk.Button(main_frame, text="Export Analysis", command=self.export_analysis)
        export_btn.pack(pady=5, anchor='ne')
    
    def create_log_view_tab(self):
        """Create the log view tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text='Log View')
        
        # Create log tree
        self.log_tree = ttk.Treeview(log_frame, columns=(
            'timestamp', 'type', 'source', 'message', 'severity'
        ), show='headings')
        
        # Set column headings
        self.log_tree.heading('timestamp', text='Timestamp')
        self.log_tree.heading('type', text='Type')
        self.log_tree.heading('source', text='Source')
        self.log_tree.heading('message', text='Message')
        self.log_tree.heading('severity', text='Severity')
        
        # Set column widths
        self.log_tree.column('timestamp', width=150)
        self.log_tree.column('type', width=100)
        self.log_tree.column('source', width=150)
        self.log_tree.column('message', width=400)
        self.log_tree.column('severity', width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack log tree
        self.log_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_alerts_tab(self):
        """Create the alerts tab"""
        alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(alerts_frame, text='Alerts')
        
        # Create alerts tree
        self.alerts_tree = ttk.Treeview(alerts_frame, columns=(
            'timestamp', 'severity', 'rule', 'message', 'details'
        ), show='headings')
        
        # Set column headings
        self.alerts_tree.heading('timestamp', text='Timestamp')
        self.alerts_tree.heading('severity', text='Severity')
        self.alerts_tree.heading('rule', text='Rule')
        self.alerts_tree.heading('message', text='Message')
        self.alerts_tree.heading('details', text='Details')
        
        # Set column widths
        self.alerts_tree.column('timestamp', width=150)
        self.alerts_tree.column('severity', width=80)
        self.alerts_tree.column('rule', width=150)
        self.alerts_tree.column('message', width=200)
        self.alerts_tree.column('details', width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(alerts_frame, orient='vertical', command=self.alerts_tree.yview)
        self.alerts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack alerts tree
        self.alerts_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_statistics_tab(self):
        """Create the statistics tab"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text='Statistics')
        
        # Create statistics tree
        self.stats_tree = ttk.Treeview(stats_frame, columns=(
            'metric', 'value', 'trend'
        ), show='headings')
        
        # Set column headings
        self.stats_tree.heading('metric', text='Metric')
        self.stats_tree.heading('value', text='Value')
        self.stats_tree.heading('trend', text='Trend')
        
        # Set column widths
        self.stats_tree.column('metric', width=200)
        self.stats_tree.column('value', width=100)
        self.stats_tree.column('trend', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack statistics tree
        self.stats_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def browse_file(self):
        """Browse for log file"""
        filename = filedialog.askopenfilename(
            title='Select Log File',
            filetypes=[
                ('Log files', '*.log'),
                ('Text files', '*.txt'),
                ('All files', '*.*')
            ]
        )
        if filename:
            self.file_var.set(filename)
    
    def start_analysis(self):
        """Start log analysis"""
        filename = self.file_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please select a log file")
            return
        
        analysis_type = self.analysis_type_var.get()
        
        # Start analysis in a separate thread
        self.analyzing = True
        self.start_button.config(state='disabled')
        
        self.analysis_thread = threading.Thread(
            target=self.run_analysis,
            args=(filename, analysis_type)
        )
        self.analysis_thread.start()
    
    def run_analysis(self, filename, analysis_type):
        """Run the log analysis"""
        try:
            # Clear previous results
            self.log_tree.delete(*self.log_tree.get_children())
            self.alerts_tree.delete(*self.alerts_tree.get_children())
            self.stats_tree.delete(*self.stats_tree.get_children())
            
            # Read and analyze log file
            with open(filename, 'r') as f:
                for line in f:
                    if not self.analyzing:
                        break
                    
                    # Parse log line
                    log_entry = self.parse_log_line(line)
                    if log_entry:
                        # Add to log view
                        self.log_tree.insert('', 'end', values=(
                            log_entry['timestamp'],
                            log_entry['type'],
                            log_entry['source'],
                            log_entry['message'],
                            log_entry['severity']
                        ))
                        
                        # Check for alerts
                        self.check_alerts(log_entry)
            
            # Calculate statistics
            self.calculate_statistics()
            
            # Save analysis results
            self.save_analysis_results()
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
        finally:
            self.analyzing = False
            self.start_button.config(state='normal')
    
    def parse_log_line(self, line):
        """Parse a log line and extract relevant information"""
        for pattern_name, pattern_info in self.log_patterns.items():
            match = re.search(pattern_info['pattern'], line)
            if match:
                return {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': pattern_info['type'],
                    'source': match.group(1) if len(match.groups()) > 0 else 'Unknown',
                    'message': line.strip(),
                    'severity': pattern_info['severity']
                }
        return None
    
    def check_alerts(self, log_entry):
        """Check log entry against alert rules"""
        for rule_name, rule in self.alert_rules.items():
            if self.evaluate_rule(rule, log_entry):
                self.alerts.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'severity': rule['severity'],
                    'rule': rule_name,
                    'message': rule['message'],
                    'details': str(log_entry)
                })
                
                # Add to alerts view
                self.alerts_tree.insert('', 'end', values=(
                    self.alerts[-1]['timestamp'],
                    self.alerts[-1]['severity'],
                    self.alerts[-1]['rule'],
                    self.alerts[-1]['message'],
                    self.alerts[-1]['details']
                ))
    
    def evaluate_rule(self, rule, log_entry):
        """Evaluate an alert rule against a log entry"""
        try:
            if rule['condition'] == "count > 5":
                # Count similar entries in the last 5 minutes
                recent_entries = [e for e in self.log_data if e['type'] == log_entry['type']]
                return len(recent_entries) > 5
            elif rule['condition'] == "ip in blacklist":
                # Check if source IP is in blacklist
                return log_entry['source'] in self.get_blacklisted_ips()
            return False
        except Exception as e:
            self.logger.error(f"Error evaluating rule: {str(e)}")
            return False
    
    def get_blacklisted_ips(self):
        """Get list of blacklisted IPs"""
        try:
            blacklist_path = Path("config/blacklist.json")
            if blacklist_path.exists():
                with open(blacklist_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.logger.error(f"Error loading blacklist: {str(e)}")
            return []
    
    def calculate_statistics(self):
        """Calculate and display statistics"""
        try:
            # Convert log data to DataFrame
            df = pd.DataFrame(self.log_data)
            
            # Calculate statistics
            stats = {
                'Total Log Entries': len(df),
                'High Severity Events': len(df[df['severity'] == 'high']),
                'Medium Severity Events': len(df[df['severity'] == 'medium']),
                'Low Severity Events': len(df[df['severity'] == 'low']),
                'Unique Sources': df['source'].nunique(),
                'Most Common Type': df['type'].mode().iloc[0] if not df.empty else 'N/A'
            }
            
            # Add to statistics view
            for metric, value in stats.items():
                self.stats_tree.insert('', 'end', values=(
                    metric,
                    value,
                    'N/A'  # Trend would require historical data
                ))
            
        except Exception as e:
            self.logger.error(f"Error calculating statistics: {str(e)}")
    
    def save_analysis_results(self):
        """Save analysis results to file"""
        try:
            results_dir = Path("reports/log_analysis")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = results_dir / f"analysis_results_{timestamp}.json"
            
            results = {
                'log_entries': self.log_data,
                'alerts': self.alerts,
                'statistics': {
                    'total_entries': len(self.log_data),
                    'total_alerts': len(self.alerts),
                    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
            
        except Exception as e:
            self.logger.error(f"Error saving analysis results: {str(e)}")
    
    def export_analysis(self):
        """Export analysis results to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
                title='Save Analysis Results As...'
            )
            
            if filename:
                # Export log entries
                log_df = pd.DataFrame(self.log_data)
                log_df.to_csv(f"{filename}_logs.csv", index=False)
                
                # Export alerts
                alerts_df = pd.DataFrame(self.alerts)
                alerts_df.to_csv(f"{filename}_alerts.csv", index=False)
                
                messagebox.showinfo("Success", f"Analysis results exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")
    
    def update_ui(self):
        pass 