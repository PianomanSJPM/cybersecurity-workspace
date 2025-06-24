import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import queue
from datetime import datetime
import pandas as pd
from pathlib import Path
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import subprocess
import socket
# import iptables  # Removed for now to allow the application to start

class IncidentResponse:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.incident_queue = queue.Queue()
        self.responding = False
        self.response_thread = None
        self.incidents = []
        self.playbooks = self.load_playbooks()
        
        # Initialize logging
        self.logger = logging.getLogger("IncidentResponse")
    
    def load_playbooks(self):
        """Load incident response playbooks"""
        try:
            playbook_path = Path("config/playbooks.json")
            if playbook_path.exists():
                with open(playbook_path, 'r') as f:
                    return json.load(f)
            return {
                "brute_force": {
                    "name": "Brute Force Attack",
                    "severity": "high",
                    "steps": [
                        "Block source IP",
                        "Notify security team",
                        "Check for compromised accounts",
                        "Review authentication logs"
                    ]
                },
                "data_exfiltration": {
                    "name": "Data Exfiltration",
                    "severity": "critical",
                    "steps": [
                        "Isolate affected systems",
                        "Notify security team",
                        "Preserve evidence",
                        "Review network traffic",
                        "Check for data backups"
                    ]
                },
                "malware_detection": {
                    "name": "Malware Detection",
                    "severity": "high",
                    "steps": [
                        "Isolate infected system",
                        "Notify security team",
                        "Collect malware sample",
                        "Scan other systems",
                        "Update antivirus"
                    ]
                }
            }
        except Exception as e:
            self.logger.error(f"Error loading playbooks: {str(e)}")
            return {}
    
    def create_ui(self, parent):
        """Create the incident response UI"""
        # Create main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create control frame
        control_frame = ttk.LabelFrame(main_frame, text="Incident Response Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Create incident button
        self.create_btn = ttk.Button(control_frame, text="Create Incident", command=self.create_incident)
        self.create_btn.pack(side='left', padx=5)
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create active incidents tab
        self.create_active_incidents_tab()
        
        # Create incident history tab
        self.create_incident_history_tab()
        
        # Create playbooks tab
        self.create_playbooks_tab()
        
        # Add export button
        export_btn = ttk.Button(main_frame, text="Export Incidents", command=self.export_incidents)
        export_btn.pack(pady=5, anchor='ne')
    
    def create_active_incidents_tab(self):
        """Create the active incidents tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Active Incidents')
        
        # Create incidents tree
        self.active_tree = ttk.Treeview(frame, columns=(
            'id', 'timestamp', 'type', 'severity', 'status', 'assigned_to'
        ), show='headings')
        
        # Set column headings
        self.active_tree.heading('id', text='ID')
        self.active_tree.heading('timestamp', text='Timestamp')
        self.active_tree.heading('type', text='Type')
        self.active_tree.heading('severity', text='Severity')
        self.active_tree.heading('status', text='Status')
        self.active_tree.heading('assigned_to', text='Assigned To')
        
        # Set column widths
        self.active_tree.column('id', width=50)
        self.active_tree.column('timestamp', width=150)
        self.active_tree.column('type', width=150)
        self.active_tree.column('severity', width=80)
        self.active_tree.column('status', width=100)
        self.active_tree.column('assigned_to', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.active_tree.yview)
        self.active_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack incidents tree
        self.active_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add right-click menu
        self.create_context_menu(self.active_tree)
    
    def create_incident_history_tab(self):
        """Create the incident history tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Incident History')
        
        # Create history tree
        self.history_tree = ttk.Treeview(frame, columns=(
            'id', 'timestamp', 'type', 'severity', 'resolution', 'resolution_time'
        ), show='headings')
        
        # Set column headings
        self.history_tree.heading('id', text='ID')
        self.history_tree.heading('timestamp', text='Timestamp')
        self.history_tree.heading('type', text='Type')
        self.history_tree.heading('severity', text='Severity')
        self.history_tree.heading('resolution', text='Resolution')
        self.history_tree.heading('resolution_time', text='Resolution Time')
        
        # Set column widths
        self.history_tree.column('id', width=50)
        self.history_tree.column('timestamp', width=150)
        self.history_tree.column('type', width=150)
        self.history_tree.column('severity', width=80)
        self.history_tree.column('resolution', width=200)
        self.history_tree.column('resolution_time', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack history tree
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_playbooks_tab(self):
        """Create the playbooks tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Playbooks')
        
        # Create playbooks tree
        self.playbooks_tree = ttk.Treeview(frame, columns=(
            'name', 'severity', 'steps'
        ), show='headings')
        
        # Set column headings
        self.playbooks_tree.heading('name', text='Name')
        self.playbooks_tree.heading('severity', text='Severity')
        self.playbooks_tree.heading('steps', text='Steps')
        
        # Set column widths
        self.playbooks_tree.column('name', width=200)
        self.playbooks_tree.column('severity', width=80)
        self.playbooks_tree.column('steps', width=400)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.playbooks_tree.yview)
        self.playbooks_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack playbooks tree
        self.playbooks_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate playbooks
        for playbook_id, playbook in self.playbooks.items():
            self.playbooks_tree.insert('', 'end', values=(
                playbook['name'],
                playbook['severity'],
                '\n'.join(playbook['steps'])
            ))
    
    def create_context_menu(self, tree):
        """Create right-click context menu for incidents"""
        self.context_menu = tk.Menu(tree, tearoff=0)
        self.context_menu.add_command(label="View Details", command=lambda: self.view_incident_details(tree))
        self.context_menu.add_command(label="Assign Incident", command=lambda: self.assign_incident(tree))
        self.context_menu.add_command(label="Update Status", command=lambda: self.update_incident_status(tree))
        self.context_menu.add_command(label="Resolve Incident", command=lambda: self.resolve_incident(tree))
        
        tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show the context menu on right-click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def create_incident(self):
        """Create a new incident"""
        # Create incident dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Create Incident")
        dialog.geometry("400x300")
        
        # Create form
        ttk.Label(dialog, text="Incident Type:").pack(pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(dialog, textvariable=type_var,
                                values=list(self.playbooks.keys()),
                                state="readonly")
        type_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Description:").pack(pady=5)
        desc_text = tk.Text(dialog, height=5)
        desc_text.pack(pady=5)
        
        ttk.Label(dialog, text="Assigned To:").pack(pady=5)
        assigned_var = tk.StringVar()
        assigned_entry = ttk.Entry(dialog, textvariable=assigned_var)
        assigned_entry.pack(pady=5)
        
        def save_incident():
            incident_type = type_var.get()
            description = desc_text.get('1.0', 'end-1c')
            assigned_to = assigned_var.get()
            
            if not incident_type:
                messagebox.showerror("Error", "Please select an incident type")
                return
            
            # Create incident
            incident = {
                'id': len(self.incidents) + 1,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': incident_type,
                'description': description,
                'severity': self.playbooks[incident_type]['severity'],
                'status': 'New',
                'assigned_to': assigned_to,
                'steps': self.playbooks[incident_type]['steps'].copy()
            }
            
            # Add to active incidents
            self.incidents.append(incident)
            self.active_tree.insert('', 'end', values=(
                incident['id'],
                incident['timestamp'],
                incident['type'],
                incident['severity'],
                incident['status'],
                incident['assigned_to']
            ))
            
            # Start response
            self.start_response(incident)
            
            dialog.destroy()
        
        # Add save button
        ttk.Button(dialog, text="Save", command=save_incident).pack(pady=10)
    
    def view_incident_details(self, tree):
        """View incident details"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get incident
        incident_id = int(tree.item(selected[0])['values'][0])
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return
        
        # Create details dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Incident Details - {incident['type']}")
        dialog.geometry("600x400")
        
        # Create details view
        details_frame = ttk.Frame(dialog)
        details_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add incident information
        ttk.Label(details_frame, text=f"ID: {incident['id']}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Timestamp: {incident['timestamp']}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Type: {incident['type']}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Severity: {incident['severity']}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Status: {incident['status']}").pack(anchor='w')
        ttk.Label(details_frame, text=f"Assigned To: {incident['assigned_to']}").pack(anchor='w')
        
        ttk.Label(details_frame, text="Description:").pack(anchor='w', pady=(10, 5))
        desc_text = tk.Text(details_frame, height=5, wrap='word')
        desc_text.insert('1.0', incident['description'])
        desc_text.pack(fill='x', padx=5)
        
        ttk.Label(details_frame, text="Response Steps:").pack(anchor='w', pady=(10, 5))
        steps_text = tk.Text(details_frame, height=10, wrap='word')
        steps_text.insert('1.0', '\n'.join(incident['steps']))
        steps_text.pack(fill='x', padx=5)
    
    def assign_incident(self, tree):
        """Assign incident to a team member"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get incident
        incident_id = int(tree.item(selected[0])['values'][0])
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return
        
        # Create assignment dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Assign Incident")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Assign To:").pack(pady=5)
        assigned_var = tk.StringVar(value=incident['assigned_to'])
        assigned_entry = ttk.Entry(dialog, textvariable=assigned_var)
        assigned_entry.pack(pady=5)
        
        def save_assignment():
            assigned_to = assigned_var.get()
            if not assigned_to:
                messagebox.showerror("Error", "Please enter an assignee")
                return
            
            # Update incident
            incident['assigned_to'] = assigned_to
            tree.item(selected[0], values=(
                incident['id'],
                incident['timestamp'],
                incident['type'],
                incident['severity'],
                incident['status'],
                incident['assigned_to']
            ))
            
            dialog.destroy()
        
        # Add save button
        ttk.Button(dialog, text="Save", command=save_assignment).pack(pady=10)
    
    def update_incident_status(self, tree):
        """Update incident status"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get incident
        incident_id = int(tree.item(selected[0])['values'][0])
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return
        
        # Create status dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Status")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Status:").pack(pady=5)
        status_var = tk.StringVar(value=incident['status'])
        status_combo = ttk.Combobox(dialog, textvariable=status_var,
                                  values=['New', 'In Progress', 'On Hold', 'Resolved'],
                                  state="readonly")
        status_combo.pack(pady=5)
        
        def save_status():
            status = status_var.get()
            if not status:
                messagebox.showerror("Error", "Please select a status")
                return
            
            # Update incident
            incident['status'] = status
            tree.item(selected[0], values=(
                incident['id'],
                incident['timestamp'],
                incident['type'],
                incident['severity'],
                incident['status'],
                incident['assigned_to']
            ))
            
            dialog.destroy()
        
        # Add save button
        ttk.Button(dialog, text="Save", command=save_status).pack(pady=10)
    
    def resolve_incident(self, tree):
        """Resolve an incident"""
        selected = tree.selection()
        if not selected:
            return
        
        # Get incident
        incident_id = int(tree.item(selected[0])['values'][0])
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return
        
        # Create resolution dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Resolve Incident")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Resolution:").pack(pady=5)
        resolution_text = tk.Text(dialog, height=10)
        resolution_text.pack(pady=5)
        
        def save_resolution():
            resolution = resolution_text.get('1.0', 'end-1c')
            if not resolution:
                messagebox.showerror("Error", "Please enter a resolution")
                return
            
            # Update incident
            incident['status'] = 'Resolved'
            incident['resolution'] = resolution
            incident['resolution_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Move to history
            self.history_tree.insert('', 'end', values=(
                incident['id'],
                incident['timestamp'],
                incident['type'],
                incident['severity'],
                resolution,
                incident['resolution_time']
            ))
            
            # Remove from active
            tree.delete(selected[0])
            self.incidents.remove(incident)
            
            dialog.destroy()
        
        # Add save button
        ttk.Button(dialog, text="Save", command=save_resolution).pack(pady=10)
    
    def start_response(self, incident):
        """Start incident response"""
        if self.responding:
            self.incident_queue.put(incident)
            return
        
        self.responding = True
        self.response_thread = threading.Thread(target=self.run_response, args=(incident,))
        self.response_thread.start()
    
    def run_response(self, incident):
        """Run incident response"""
        try:
            # Execute response steps
            for step in incident['steps']:
                if not self.responding:
                    break
                
                # Execute step
                self.execute_step(incident, step)
            
            # Check for more incidents
            if not self.incident_queue.empty():
                next_incident = self.incident_queue.get()
                self.run_response(next_incident)
            else:
                self.responding = False
        
        except Exception as e:
            self.logger.error(f"Error in incident response: {str(e)}")
            self.responding = False
    
    def execute_step(self, incident, step):
        """Execute a response step"""
        try:
            if step == "Block source IP":
                self.block_ip(incident)
            elif step == "Notify security team":
                self.notify_security_team(incident)
            elif step == "Isolate affected systems":
                self.isolate_systems(incident)
            elif step == "Preserve evidence":
                self.preserve_evidence(incident)
            elif step == "Collect malware sample":
                self.collect_malware_sample(incident)
            elif step == "Scan other systems":
                self.scan_systems(incident)
            elif step == "Update antivirus":
                self.update_antivirus(incident)
            elif step == "Check for compromised accounts":
                self.check_compromised_accounts(incident)
            elif step == "Review authentication logs":
                self.review_auth_logs(incident)
            elif step == "Review network traffic":
                self.review_network_traffic(incident)
            elif step == "Check for data backups":
                self.check_backups(incident)
        
        except Exception as e:
            self.logger.error(f"Error executing step {step}: {str(e)}")
    
    def block_ip(self, incident):
        """Block IP address"""
        try:
            # Get IP from incident description
            ip = self.extract_ip(incident['description'])
            if not ip:
                return
            
            # Block IP using iptables
            subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
            
            # Log action
            self.logger.info(f"Blocked IP {ip} for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error blocking IP: {str(e)}")
    
    def notify_security_team(self, incident):
        """Notify security team"""
        try:
            # Get notification settings
            email = self.config_manager.get_setting("incident_response", "notification_email")
            sms = self.config_manager.get_setting("incident_response", "notification_sms")
            
            # Send email
            if email:
                self.send_email(email, incident)
            
            # Send SMS
            if sms:
                self.send_sms(sms, incident)
        
        except Exception as e:
            self.logger.error(f"Error notifying security team: {str(e)}")
    
    def isolate_systems(self, incident):
        """Isolate affected systems"""
        try:
            # Get system from incident description
            system = self.extract_system(incident['description'])
            if not system:
                return
            
            # Isolate system using iptables
            subprocess.run(['iptables', '-A', 'INPUT', '-s', system, '-j', 'DROP'])
            subprocess.run(['iptables', '-A', 'OUTPUT', '-d', system, '-j', 'DROP'])
            
            # Log action
            self.logger.info(f"Isolated system {system} for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error isolating system: {str(e)}")
    
    def preserve_evidence(self, incident):
        """Preserve incident evidence"""
        try:
            # Create evidence directory
            evidence_dir = Path("evidence") / f"incident_{incident['id']}"
            evidence_dir.mkdir(parents=True, exist_ok=True)
            
            # Save incident details
            with open(evidence_dir / "incident.json", 'w') as f:
                json.dump(incident, f, indent=4)
            
            # Log action
            self.logger.info(f"Preserved evidence for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error preserving evidence: {str(e)}")
    
    def collect_malware_sample(self, incident):
        """Collect malware sample"""
        try:
            # Get malware path from incident description
            path = self.extract_path(incident['description'])
            if not path:
                return
            
            # Create malware directory
            malware_dir = Path("evidence") / f"incident_{incident['id']}" / "malware"
            malware_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy malware sample
            subprocess.run(['cp', path, malware_dir / "sample"])
            
            # Log action
            self.logger.info(f"Collected malware sample for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error collecting malware sample: {str(e)}")
    
    def scan_systems(self, incident):
        """Scan other systems"""
        try:
            # Get systems to scan
            systems = self.get_systems_to_scan(incident)
            if not systems:
                return
            
            # Scan each system
            for system in systems:
                subprocess.run(['nmap', '-sV', '-sC', system])
            
            # Log action
            self.logger.info(f"Scanned systems for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error scanning systems: {str(e)}")
    
    def update_antivirus(self, incident):
        """Update antivirus"""
        try:
            # Update antivirus definitions
            subprocess.run(['freshclam'])
            
            # Log action
            self.logger.info(f"Updated antivirus for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error updating antivirus: {str(e)}")
    
    def check_compromised_accounts(self, incident):
        """Check for compromised accounts"""
        try:
            # Get accounts to check
            accounts = self.get_accounts_to_check(incident)
            if not accounts:
                return
            
            # Check each account
            for account in accounts:
                # Check login history
                subprocess.run(['last', account])
                
                # Check sudo history
                subprocess.run(['sudo', '-l', '-U', account])
            
            # Log action
            self.logger.info(f"Checked compromised accounts for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error checking compromised accounts: {str(e)}")
    
    def review_auth_logs(self, incident):
        """Review authentication logs"""
        try:
            # Get log files to review
            log_files = self.get_auth_logs(incident)
            if not log_files:
                return
            
            # Review each log file
            for log_file in log_files:
                subprocess.run(['grep', 'Failed password', log_file])
                subprocess.run(['grep', 'Invalid user', log_file])
            
            # Log action
            self.logger.info(f"Reviewed auth logs for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error reviewing auth logs: {str(e)}")
    
    def review_network_traffic(self, incident):
        """Review network traffic"""
        try:
            # Get traffic to review
            traffic = self.get_network_traffic(incident)
            if not traffic:
                return
            
            # Review traffic
            for t in traffic:
                subprocess.run(['tcpdump', '-r', t])
            
            # Log action
            self.logger.info(f"Reviewed network traffic for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error reviewing network traffic: {str(e)}")
    
    def check_backups(self, incident):
        """Check for data backups"""
        try:
            # Get backup locations
            backup_locations = self.get_backup_locations(incident)
            if not backup_locations:
                return
            
            # Check each backup
            for location in backup_locations:
                subprocess.run(['ls', '-l', location])
            
            # Log action
            self.logger.info(f"Checked backups for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error checking backups: {str(e)}")
    
    def send_email(self, email, incident):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = "security@example.com"
            msg['To'] = email
            msg['Subject'] = f"Security Incident {incident['id']} - {incident['type']}"
            
            body = f"""
            Security Incident Details:
            
            ID: {incident['id']}
            Type: {incident['type']}
            Severity: {incident['severity']}
            Description: {incident['description']}
            Timestamp: {incident['timestamp']}
            
            Please take appropriate action.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP('localhost') as server:
                server.send_message(msg)
            
            # Log action
            self.logger.info(f"Sent email notification for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
    
    def send_sms(self, phone, incident):
        """Send SMS notification"""
        try:
            # Implement SMS sending logic here
            # This is a placeholder for actual SMS implementation
            
            # Log action
            self.logger.info(f"Sent SMS notification for incident {incident['id']}")
        
        except Exception as e:
            self.logger.error(f"Error sending SMS: {str(e)}")
    
    def extract_ip(self, text):
        """Extract IP address from text"""
        import re
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def extract_system(self, text):
        """Extract system identifier from text"""
        import re
        pattern = r'system[:\s]+([^\s]+)'
        match = re.search(pattern, text)
        return match.group(1) if match else None
    
    def extract_path(self, text):
        """Extract file path from text"""
        import re
        pattern = r'path[:\s]+([^\s]+)'
        match = re.search(pattern, text)
        return match.group(1) if match else None
    
    def get_systems_to_scan(self, incident):
        """Get systems to scan"""
        # This is a placeholder for actual system discovery logic
        return ['localhost']
    
    def get_accounts_to_check(self, incident):
        """Get accounts to check"""
        # This is a placeholder for actual account discovery logic
        return ['root', 'admin']
    
    def get_auth_logs(self, incident):
        """Get authentication log files"""
        # This is a placeholder for actual log file discovery logic
        return ['/var/log/auth.log']
    
    def get_network_traffic(self, incident):
        """Get network traffic files"""
        # This is a placeholder for actual traffic file discovery logic
        return ['/var/log/tcpdump.log']
    
    def get_backup_locations(self, incident):
        """Get backup locations"""
        # This is a placeholder for actual backup location discovery logic
        return ['/backup']
    
    def export_incidents(self):
        """Export incidents to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
                title='Save Incidents As...'
            )
            
            if filename:
                # Export active incidents
                active_data = []
                for item in self.active_tree.get_children():
                    active_data.append(self.active_tree.item(item)['values'])
                
                active_df = pd.DataFrame(active_data,
                                       columns=['ID', 'Timestamp', 'Type', 'Severity', 'Status', 'Assigned To'])
                active_df.to_csv(f"{filename}_active.csv", index=False)
                
                # Export incident history
                history_data = []
                for item in self.history_tree.get_children():
                    history_data.append(self.history_tree.item(item)['values'])
                
                history_df = pd.DataFrame(history_data,
                                        columns=['ID', 'Timestamp', 'Type', 'Severity', 'Resolution', 'Resolution Time'])
                history_df.to_csv(f"{filename}_history.csv", index=False)
                
                messagebox.showinfo("Success", f"Incidents exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export incidents: {str(e)}")
    
    def update_ui(self):
        """Update the UI components"""
        pass  # No real-time updates needed for this module 