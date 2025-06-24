import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import threading
import queue
import logging
from pathlib import Path

# Import our security modules
from modules.network_monitor import NetworkMonitor
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.log_analyzer import LogAnalyzer
from modules.incident_response import IncidentResponse
from modules.security_policy import SecurityPolicy
from modules.patch_manager import PatchManager
from modules.risk_assessor import RiskAssessor
from modules.config_manager import ConfigManager

class SecurityToolkit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Security Toolkit")
        self.root.geometry("1400x800")
        
        # Initialize logging
        self.setup_logging()
        
        # Initialize ConfigManager
        self.config_manager = ConfigManager()
        self.initialize_modules()
        
        # Create UI
        self.create_ui()
        
        # Start periodic updates
        self.root.after(1000, self.update_ui)
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "security_toolkit.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SecurityToolkit")
    
    def initialize_modules(self):
        """Initialize all security modules"""
        try:
            self.network_monitor = NetworkMonitor(self.config_manager)
            self.vulnerability_scanner = VulnerabilityScanner(self.config_manager)
            self.log_analyzer = LogAnalyzer(self.config_manager)
            self.incident_response = IncidentResponse(self.config_manager)
            self.security_policy = SecurityPolicy(self.config_manager)
            self.patch_manager = PatchManager(self.config_manager)
            self.risk_assessor = RiskAssessor(self.config_manager)
            self.logger.info("All modules initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing modules: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize modules: {str(e)}")
    
    def create_ui(self):
        """Create the main UI components"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs for each module
        self.create_network_monitor_tab()
        self.create_vulnerability_scanner_tab()
        self.create_log_analyzer_tab()
        self.create_incident_response_tab()
        self.create_security_policy_tab()
        self.create_patch_manager_tab()
        self.create_risk_assessor_tab()
        
        # Create status bar
        self.create_status_bar()
    
    def create_network_monitor_tab(self):
        """Create the network monitoring tab"""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text='Network Monitor')
        
        # Add network monitoring components
        self.network_monitor.create_ui(network_frame)
    
    def create_vulnerability_scanner_tab(self):
        """Create the vulnerability scanner tab"""
        scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(scanner_frame, text='Vulnerability Scanner')
        
        # Add vulnerability scanning components
        self.vulnerability_scanner.create_ui(scanner_frame)
    
    def create_log_analyzer_tab(self):
        """Create the log analyzer tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text='Log Analyzer')
        
        # Add log analysis components
        self.log_analyzer.create_ui(log_frame)
    
    def create_incident_response_tab(self):
        """Create the incident response tab"""
        incident_frame = ttk.Frame(self.notebook)
        self.notebook.add(incident_frame, text='Incident Response')
        
        # Add incident response components
        self.incident_response.create_ui(incident_frame)
    
    def create_security_policy_tab(self):
        """Create the security policy tab"""
        policy_frame = ttk.Frame(self.notebook)
        self.notebook.add(policy_frame, text='Security Policy')
        
        # Add security policy components
        self.security_policy.create_ui(policy_frame)
    
    def create_patch_manager_tab(self):
        """Create the patch manager tab"""
        patch_frame = ttk.Frame(self.notebook)
        self.notebook.add(patch_frame, text='Patch Manager')
        
        # Add patch management components
        self.patch_manager.create_ui(patch_frame)
    
    def create_risk_assessor_tab(self):
        """Create the risk assessor tab"""
        risk_frame = ttk.Frame(self.notebook)
        self.notebook.add(risk_frame, text='Risk Assessor')
        
        # Add risk assessment components
        self.risk_assessor.create_ui(risk_frame)
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side='bottom', fill='x')
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side='left', padx=5)
        
        self.time_label = ttk.Label(status_frame, text="")
        self.time_label.pack(side='right', padx=5)
    
    def update_ui(self):
        """Update the UI components"""
        try:
            # Update status bar
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.time_label.config(text=current_time)
            
            # Update module UIs
            self.network_monitor.update_ui()
            self.vulnerability_scanner.update_ui()
            self.log_analyzer.update_ui()
            self.incident_response.update_ui()
            self.security_policy.update_ui()
            self.patch_manager.update_ui()
            self.risk_assessor.update_ui()
            
        except Exception as e:
            self.logger.error(f"Error updating UI: {str(e)}")
        
        # Schedule next update
        self.root.after(1000, self.update_ui)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SecurityToolkit()
    app.run() 