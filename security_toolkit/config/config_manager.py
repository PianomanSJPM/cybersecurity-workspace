import json
import os
from pathlib import Path
import logging
from typing import Any, Dict, Optional

class ConfigManager:
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        self.logger = logging.getLogger("ConfigManager")
        
        # Default configuration
        self.default_config = {
            "general": {
                "log_level": "INFO",
                "auto_save": True,
                "save_interval": 300,  # 5 minutes
                "theme": "default"
            },
            "network_monitor": {
                "capture_interface": "any",
                "packet_buffer_size": 65535,
                "update_interval": 1.0,
                "max_devices": 100,
                "alert_threshold": 1000
            },
            "vulnerability_scanner": {
                "scan_timeout": 300,
                "max_threads": 10,
                "default_ports": "21-25,53,80,443,3306,3389",
                "alert_on_high": True,
                "save_reports": True
            },
            "log_analyzer": {
                "max_log_size": 10485760,  # 10MB
                "retention_days": 30,
                "alert_patterns": [
                    "Failed password",
                    "Invalid user",
                    "Connection refused"
                ]
            },
            "incident_response": {
                "notification_email": "",
                "notification_sms": "",
                "auto_block": False,
                "block_duration": 3600,  # 1 hour
                "response_actions": [
                    "log_incident",
                    "notify_admin",
                    "block_ip"
                ]
            },
            "security_policy": {
                "password_policy": {
                    "min_length": 12,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_special": True,
                    "max_age": 90  # days
                },
                "access_control": {
                    "max_failed_attempts": 5,
                    "lockout_duration": 900,  # 15 minutes
                    "session_timeout": 1800  # 30 minutes
                }
            },
            "patch_management": {
                "auto_check": True,
                "check_interval": 86400,  # 24 hours
                "auto_install": False,
                "install_time": "02:00",  # 2 AM
                "excluded_packages": []
            },
            "risk_assessment": {
                "risk_levels": {
                    "critical": 9,
                    "high": 7,
                    "medium": 4,
                    "low": 1
                },
                "assessment_interval": 604800,  # 7 days
                "auto_remediate": False
            }
        }
        
        # Load configuration
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with default config to ensure all settings exist
                return self.merge_configs(self.default_config, config)
            else:
                # Create default config file
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get_setting(self, module: str, key: str, default: Any = None) -> Any:
        """Get a specific setting value"""
        try:
            return self.config.get(module, {}).get(key, default)
        except Exception as e:
            self.logger.error(f"Error getting setting {module}.{key}: {str(e)}")
            return default
    
    def set_setting(self, module: str, key: str, value: Any) -> bool:
        """Set a specific setting value"""
        try:
            if module not in self.config:
                self.config[module] = {}
            self.config[module][key] = value
            return self.save_config(self.config)
        except Exception as e:
            self.logger.error(f"Error setting {module}.{key}: {str(e)}")
            return False
    
    def get_module_config(self, module: str) -> Dict[str, Any]:
        """Get all settings for a specific module"""
        try:
            return self.config.get(module, {})
        except Exception as e:
            self.logger.error(f"Error getting module config for {module}: {str(e)}")
            return {}
    
    def set_module_config(self, module: str, config: Dict[str, Any]) -> bool:
        """Set all settings for a specific module"""
        try:
            self.config[module] = config
            return self.save_config(self.config)
        except Exception as e:
            self.logger.error(f"Error setting module config for {module}: {str(e)}")
            return False
    
    def reset_to_defaults(self, module: Optional[str] = None) -> bool:
        """Reset configuration to defaults"""
        try:
            if module:
                if module in self.default_config:
                    self.config[module] = self.default_config[module]
            else:
                self.config = self.default_config
            return self.save_config(self.config)
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {str(e)}")
            return False
    
    def merge_configs(self, default: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        """Merge current configuration with defaults"""
        merged = default.copy()
        for key, value in current.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def validate_config(self) -> bool:
        """Validate configuration values"""
        try:
            # Check required fields
            for module, settings in self.default_config.items():
                if module not in self.config:
                    self.logger.warning(f"Missing module configuration: {module}")
                    return False
                
                for key, default_value in settings.items():
                    if key not in self.config[module]:
                        self.logger.warning(f"Missing setting: {module}.{key}")
                        return False
            
            # Validate specific settings
            if not isinstance(self.get_setting("general", "log_level"), str):
                return False
            
            if not isinstance(self.get_setting("general", "auto_save"), bool):
                return False
            
            if not isinstance(self.get_setting("general", "save_interval"), int):
                return False
            
            # Add more validation as needed
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating configuration: {str(e)}")
            return False
    
    def export_config(self, filename: str) -> bool:
        """Export configuration to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {str(e)}")
            return False
    
    def import_config(self, filename: str) -> bool:
        """Import configuration from a file"""
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
            return self.save_config(config)
        except Exception as e:
            self.logger.error(f"Error importing configuration: {str(e)}")
            return False 