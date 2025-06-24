import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .config_manager import ConfigManager
import json
from pathlib import Path
import logging

class SettingsUI:
    def __init__(self, parent):
        self.parent = parent
        self.config_manager = ConfigManager()
        self.logger = logging.getLogger("SettingsUI")
        
        # Create main window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("800x600")
        self.window.minsize(800, 600)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create notebook for different settings sections
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill='both')
        
        # Create settings sections
        self.create_general_settings()
        self.create_network_settings()
        self.create_scanner_settings()
        self.create_log_settings()
        self.create_incident_settings()
        self.create_policy_settings()
        self.create_patch_settings()
        self.create_risk_settings()
        
        # Create button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill='x', pady=10)
        
        # Add buttons
        ttk.Button(self.button_frame, text="Save", command=self.save_settings).pack(side='left', padx=5)
        ttk.Button(self.button_frame, text="Reset", command=self.reset_settings).pack(side='left', padx=5)
        ttk.Button(self.button_frame, text="Import", command=self.import_settings).pack(side='left', padx=5)
        ttk.Button(self.button_frame, text="Export", command=self.export_settings).pack(side='left', padx=5)
        ttk.Button(self.button_frame, text="Close", command=self.window.destroy).pack(side='right', padx=5)
    
    def create_general_settings(self):
        """Create general settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='General')
        
        # Create settings grid
        row = 0
        
        # Log level
        ttk.Label(frame, text="Log Level:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.log_level_var = tk.StringVar(value=self.config_manager.get_setting("general", "log_level"))
        log_level_combo = ttk.Combobox(frame, textvariable=self.log_level_var,
                                     values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                     state="readonly")
        log_level_combo.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Auto save
        ttk.Label(frame, text="Auto Save:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.auto_save_var = tk.BooleanVar(value=self.config_manager.get_setting("general", "auto_save"))
        ttk.Checkbutton(frame, variable=self.auto_save_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Save interval
        ttk.Label(frame, text="Save Interval (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.save_interval_var = tk.StringVar(value=str(self.config_manager.get_setting("general", "save_interval")))
        ttk.Entry(frame, textvariable=self.save_interval_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Theme
        ttk.Label(frame, text="Theme:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.theme_var = tk.StringVar(value=self.config_manager.get_setting("general", "theme"))
        theme_combo = ttk.Combobox(frame, textvariable=self.theme_var,
                                 values=["default", "dark", "light"],
                                 state="readonly")
        theme_combo.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
    
    def create_network_settings(self):
        """Create network monitor settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Network Monitor')
        
        # Create settings grid
        row = 0
        
        # Capture interface
        ttk.Label(frame, text="Capture Interface:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.interface_var = tk.StringVar(value=self.config_manager.get_setting("network_monitor", "capture_interface"))
        ttk.Entry(frame, textvariable=self.interface_var, width=20).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Packet buffer size
        ttk.Label(frame, text="Packet Buffer Size:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.buffer_size_var = tk.StringVar(value=str(self.config_manager.get_setting("network_monitor", "packet_buffer_size")))
        ttk.Entry(frame, textvariable=self.buffer_size_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Update interval
        ttk.Label(frame, text="Update Interval (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.update_interval_var = tk.StringVar(value=str(self.config_manager.get_setting("network_monitor", "update_interval")))
        ttk.Entry(frame, textvariable=self.update_interval_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Max devices
        ttk.Label(frame, text="Max Devices:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.max_devices_var = tk.StringVar(value=str(self.config_manager.get_setting("network_monitor", "max_devices")))
        ttk.Entry(frame, textvariable=self.max_devices_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Alert threshold
        ttk.Label(frame, text="Alert Threshold:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.alert_threshold_var = tk.StringVar(value=str(self.config_manager.get_setting("network_monitor", "alert_threshold")))
        ttk.Entry(frame, textvariable=self.alert_threshold_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
    
    def create_scanner_settings(self):
        """Create vulnerability scanner settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Vulnerability Scanner')
        
        # Create settings grid
        row = 0
        
        # Scan timeout
        ttk.Label(frame, text="Scan Timeout (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.scan_timeout_var = tk.StringVar(value=str(self.config_manager.get_setting("vulnerability_scanner", "scan_timeout")))
        ttk.Entry(frame, textvariable=self.scan_timeout_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Max threads
        ttk.Label(frame, text="Max Threads:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.max_threads_var = tk.StringVar(value=str(self.config_manager.get_setting("vulnerability_scanner", "max_threads")))
        ttk.Entry(frame, textvariable=self.max_threads_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Default ports
        ttk.Label(frame, text="Default Ports:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.default_ports_var = tk.StringVar(value=self.config_manager.get_setting("vulnerability_scanner", "default_ports"))
        ttk.Entry(frame, textvariable=self.default_ports_var, width=30).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Alert on high
        ttk.Label(frame, text="Alert on High Severity:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.alert_on_high_var = tk.BooleanVar(value=self.config_manager.get_setting("vulnerability_scanner", "alert_on_high"))
        ttk.Checkbutton(frame, variable=self.alert_on_high_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Save reports
        ttk.Label(frame, text="Save Reports:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.save_reports_var = tk.BooleanVar(value=self.config_manager.get_setting("vulnerability_scanner", "save_reports"))
        ttk.Checkbutton(frame, variable=self.save_reports_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
    
    def create_log_settings(self):
        """Create log analyzer settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Log Analyzer')
        
        # Create settings grid
        row = 0
        
        # Max log size
        ttk.Label(frame, text="Max Log Size (bytes):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.max_log_size_var = tk.StringVar(value=str(self.config_manager.get_setting("log_analyzer", "max_log_size")))
        ttk.Entry(frame, textvariable=self.max_log_size_var, width=15).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Retention days
        ttk.Label(frame, text="Retention Days:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.retention_days_var = tk.StringVar(value=str(self.config_manager.get_setting("log_analyzer", "retention_days")))
        ttk.Entry(frame, textvariable=self.retention_days_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Alert patterns
        ttk.Label(frame, text="Alert Patterns:").grid(row=row, column=0, sticky='nw', padx=5, pady=5)
        self.alert_patterns_text = tk.Text(frame, width=40, height=5)
        self.alert_patterns_text.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        patterns = self.config_manager.get_setting("log_analyzer", "alert_patterns")
        self.alert_patterns_text.insert('1.0', '\n'.join(patterns))
        row += 1
    
    def create_incident_settings(self):
        """Create incident response settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Incident Response')
        
        # Create settings grid
        row = 0
        
        # Notification email
        ttk.Label(frame, text="Notification Email:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.notification_email_var = tk.StringVar(value=self.config_manager.get_setting("incident_response", "notification_email"))
        ttk.Entry(frame, textvariable=self.notification_email_var, width=30).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Notification SMS
        ttk.Label(frame, text="Notification SMS:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.notification_sms_var = tk.StringVar(value=self.config_manager.get_setting("incident_response", "notification_sms"))
        ttk.Entry(frame, textvariable=self.notification_sms_var, width=20).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Auto block
        ttk.Label(frame, text="Auto Block:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.auto_block_var = tk.BooleanVar(value=self.config_manager.get_setting("incident_response", "auto_block"))
        ttk.Checkbutton(frame, variable=self.auto_block_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Block duration
        ttk.Label(frame, text="Block Duration (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.block_duration_var = tk.StringVar(value=str(self.config_manager.get_setting("incident_response", "block_duration")))
        ttk.Entry(frame, textvariable=self.block_duration_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Response actions
        ttk.Label(frame, text="Response Actions:").grid(row=row, column=0, sticky='nw', padx=5, pady=5)
        self.response_actions_text = tk.Text(frame, width=40, height=5)
        self.response_actions_text.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        actions = self.config_manager.get_setting("incident_response", "response_actions")
        self.response_actions_text.insert('1.0', '\n'.join(actions))
        row += 1
    
    def create_policy_settings(self):
        """Create security policy settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Security Policy')
        
        # Create settings grid
        row = 0
        
        # Password policy
        ttk.Label(frame, text="Password Policy", font=('', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        row += 1
        
        # Min length
        ttk.Label(frame, text="Minimum Length:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.min_length_var = tk.StringVar(value=str(self.config_manager.get_setting("security_policy", "password_policy")["min_length"]))
        ttk.Entry(frame, textvariable=self.min_length_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Require uppercase
        ttk.Label(frame, text="Require Uppercase:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.require_uppercase_var = tk.BooleanVar(value=self.config_manager.get_setting("security_policy", "password_policy")["require_uppercase"])
        ttk.Checkbutton(frame, variable=self.require_uppercase_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Require lowercase
        ttk.Label(frame, text="Require Lowercase:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.require_lowercase_var = tk.BooleanVar(value=self.config_manager.get_setting("security_policy", "password_policy")["require_lowercase"])
        ttk.Checkbutton(frame, variable=self.require_lowercase_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Require numbers
        ttk.Label(frame, text="Require Numbers:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.require_numbers_var = tk.BooleanVar(value=self.config_manager.get_setting("security_policy", "password_policy")["require_numbers"])
        ttk.Checkbutton(frame, variable=self.require_numbers_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Require special
        ttk.Label(frame, text="Require Special:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.require_special_var = tk.BooleanVar(value=self.config_manager.get_setting("security_policy", "password_policy")["require_special"])
        ttk.Checkbutton(frame, variable=self.require_special_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Max age
        ttk.Label(frame, text="Max Age (days):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.max_age_var = tk.StringVar(value=str(self.config_manager.get_setting("security_policy", "password_policy")["max_age"]))
        ttk.Entry(frame, textvariable=self.max_age_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Access control
        ttk.Label(frame, text="Access Control", font=('', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        row += 1
        
        # Max failed attempts
        ttk.Label(frame, text="Max Failed Attempts:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.max_failed_attempts_var = tk.StringVar(value=str(self.config_manager.get_setting("security_policy", "access_control")["max_failed_attempts"]))
        ttk.Entry(frame, textvariable=self.max_failed_attempts_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Lockout duration
        ttk.Label(frame, text="Lockout Duration (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.lockout_duration_var = tk.StringVar(value=str(self.config_manager.get_setting("security_policy", "access_control")["lockout_duration"]))
        ttk.Entry(frame, textvariable=self.lockout_duration_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Session timeout
        ttk.Label(frame, text="Session Timeout (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.session_timeout_var = tk.StringVar(value=str(self.config_manager.get_setting("security_policy", "access_control")["session_timeout"]))
        ttk.Entry(frame, textvariable=self.session_timeout_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
    
    def create_patch_settings(self):
        """Create patch management settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Patch Management')
        
        # Create settings grid
        row = 0
        
        # Auto check
        ttk.Label(frame, text="Auto Check:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.auto_check_var = tk.BooleanVar(value=self.config_manager.get_setting("patch_management", "auto_check"))
        ttk.Checkbutton(frame, variable=self.auto_check_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Check interval
        ttk.Label(frame, text="Check Interval (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.check_interval_var = tk.StringVar(value=str(self.config_manager.get_setting("patch_management", "check_interval")))
        ttk.Entry(frame, textvariable=self.check_interval_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Auto install
        ttk.Label(frame, text="Auto Install:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.auto_install_var = tk.BooleanVar(value=self.config_manager.get_setting("patch_management", "auto_install"))
        ttk.Checkbutton(frame, variable=self.auto_install_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Install time
        ttk.Label(frame, text="Install Time:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.install_time_var = tk.StringVar(value=self.config_manager.get_setting("patch_management", "install_time"))
        ttk.Entry(frame, textvariable=self.install_time_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Excluded packages
        ttk.Label(frame, text="Excluded Packages:").grid(row=row, column=0, sticky='nw', padx=5, pady=5)
        self.excluded_packages_text = tk.Text(frame, width=40, height=5)
        self.excluded_packages_text.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        packages = self.config_manager.get_setting("patch_management", "excluded_packages")
        self.excluded_packages_text.insert('1.0', '\n'.join(packages))
        row += 1
    
    def create_risk_settings(self):
        """Create risk assessment settings section"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='Risk Assessment')
        
        # Create settings grid
        row = 0
        
        # Risk levels
        ttk.Label(frame, text="Risk Levels", font=('', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        row += 1
        
        # Critical
        ttk.Label(frame, text="Critical:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.critical_var = tk.StringVar(value=str(self.config_manager.get_setting("risk_assessment", "risk_levels")["critical"]))
        ttk.Entry(frame, textvariable=self.critical_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # High
        ttk.Label(frame, text="High:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.high_var = tk.StringVar(value=str(self.config_manager.get_setting("risk_assessment", "risk_levels")["high"]))
        ttk.Entry(frame, textvariable=self.high_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Medium
        ttk.Label(frame, text="Medium:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.medium_var = tk.StringVar(value=str(self.config_manager.get_setting("risk_assessment", "risk_levels")["medium"]))
        ttk.Entry(frame, textvariable=self.medium_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Low
        ttk.Label(frame, text="Low:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.low_var = tk.StringVar(value=str(self.config_manager.get_setting("risk_assessment", "risk_levels")["low"]))
        ttk.Entry(frame, textvariable=self.low_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Assessment interval
        ttk.Label(frame, text="Assessment Interval (seconds):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.assessment_interval_var = tk.StringVar(value=str(self.config_manager.get_setting("risk_assessment", "assessment_interval")))
        ttk.Entry(frame, textvariable=self.assessment_interval_var, width=10).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # Auto remediate
        ttk.Label(frame, text="Auto Remediate:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.auto_remediate_var = tk.BooleanVar(value=self.config_manager.get_setting("risk_assessment", "auto_remediate"))
        ttk.Checkbutton(frame, variable=self.auto_remediate_var).grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
    
    def save_settings(self):
        """Save all settings"""
        try:
            # General settings
            self.config_manager.set_setting("general", "log_level", self.log_level_var.get())
            self.config_manager.set_setting("general", "auto_save", self.auto_save_var.get())
            self.config_manager.set_setting("general", "save_interval", int(self.save_interval_var.get()))
            self.config_manager.set_setting("general", "theme", self.theme_var.get())
            
            # Network monitor settings
            self.config_manager.set_setting("network_monitor", "capture_interface", self.interface_var.get())
            self.config_manager.set_setting("network_monitor", "packet_buffer_size", int(self.buffer_size_var.get()))
            self.config_manager.set_setting("network_monitor", "update_interval", float(self.update_interval_var.get()))
            self.config_manager.set_setting("network_monitor", "max_devices", int(self.max_devices_var.get()))
            self.config_manager.set_setting("network_monitor", "alert_threshold", int(self.alert_threshold_var.get()))
            
            # Vulnerability scanner settings
            self.config_manager.set_setting("vulnerability_scanner", "scan_timeout", int(self.scan_timeout_var.get()))
            self.config_manager.set_setting("vulnerability_scanner", "max_threads", int(self.max_threads_var.get()))
            self.config_manager.set_setting("vulnerability_scanner", "default_ports", self.default_ports_var.get())
            self.config_manager.set_setting("vulnerability_scanner", "alert_on_high", self.alert_on_high_var.get())
            self.config_manager.set_setting("vulnerability_scanner", "save_reports", self.save_reports_var.get())
            
            # Log analyzer settings
            self.config_manager.set_setting("log_analyzer", "max_log_size", int(self.max_log_size_var.get()))
            self.config_manager.set_setting("log_analyzer", "retention_days", int(self.retention_days_var.get()))
            patterns = self.alert_patterns_text.get('1.0', 'end-1c').split('\n')
            self.config_manager.set_setting("log_analyzer", "alert_patterns", patterns)
            
            # Incident response settings
            self.config_manager.set_setting("incident_response", "notification_email", self.notification_email_var.get())
            self.config_manager.set_setting("incident_response", "notification_sms", self.notification_sms_var.get())
            self.config_manager.set_setting("incident_response", "auto_block", self.auto_block_var.get())
            self.config_manager.set_setting("incident_response", "block_duration", int(self.block_duration_var.get()))
            actions = self.response_actions_text.get('1.0', 'end-1c').split('\n')
            self.config_manager.set_setting("incident_response", "response_actions", actions)
            
            # Security policy settings
            password_policy = {
                "min_length": int(self.min_length_var.get()),
                "require_uppercase": self.require_uppercase_var.get(),
                "require_lowercase": self.require_lowercase_var.get(),
                "require_numbers": self.require_numbers_var.get(),
                "require_special": self.require_special_var.get(),
                "max_age": int(self.max_age_var.get())
            }
            self.config_manager.set_setting("security_policy", "password_policy", password_policy)
            
            access_control = {
                "max_failed_attempts": int(self.max_failed_attempts_var.get()),
                "lockout_duration": int(self.lockout_duration_var.get()),
                "session_timeout": int(self.session_timeout_var.get())
            }
            self.config_manager.set_setting("security_policy", "access_control", access_control)
            
            # Patch management settings
            self.config_manager.set_setting("patch_management", "auto_check", self.auto_check_var.get())
            self.config_manager.set_setting("patch_management", "check_interval", int(self.check_interval_var.get()))
            self.config_manager.set_setting("patch_management", "auto_install", self.auto_install_var.get())
            self.config_manager.set_setting("patch_management", "install_time", self.install_time_var.get())
            packages = self.excluded_packages_text.get('1.0', 'end-1c').split('\n')
            self.config_manager.set_setting("patch_management", "excluded_packages", packages)
            
            # Risk assessment settings
            risk_levels = {
                "critical": int(self.critical_var.get()),
                "high": int(self.high_var.get()),
                "medium": int(self.medium_var.get()),
                "low": int(self.low_var.get())
            }
            self.config_manager.set_setting("risk_assessment", "risk_levels", risk_levels)
            self.config_manager.set_setting("risk_assessment", "assessment_interval", int(self.assessment_interval_var.get()))
            self.config_manager.set_setting("risk_assessment", "auto_remediate", self.auto_remediate_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            self.config_manager.reset_to_defaults()
            self.window.destroy()
            SettingsUI(self.parent)
    
    def import_settings(self):
        """Import settings from file"""
        filename = filedialog.askopenfilename(
            title='Import Settings',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if filename:
            if self.config_manager.import_config(filename):
                messagebox.showinfo("Success", "Settings imported successfully")
                self.window.destroy()
                SettingsUI(self.parent)
            else:
                messagebox.showerror("Error", "Failed to import settings")
    
    def export_settings(self):
        """Export settings to file"""
        filename = filedialog.asksaveasfilename(
            title='Export Settings',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        if filename:
            if self.config_manager.export_config(filename):
                messagebox.showinfo("Success", "Settings exported successfully")
            else:
                messagebox.showerror("Error", "Failed to export settings") 