import os
import json
import logging
import psutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupMonitor:
    def __init__(self, config_path: str = 'config/config.json'):
        """Initialize the backup monitoring module."""
        self.config_path = config_path
        self.config = self._load_config()
        self.backup_dir = Path(self.config.get('backup_location', 'backups'))
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in config file: {self.config_path}")
            return {}
    
    def check_storage_usage(self) -> Dict[str, Any]:
        """Check storage usage and return status."""
        try:
            # Get disk usage for backup directory
            usage = psutil.disk_usage(str(self.backup_dir))
            
            # Calculate usage percentage
            usage_percent = (usage.used / usage.total) * 100
            
            # Get backup directory size
            backup_size = sum(f.stat().st_size for f in self.backup_dir.rglob('*') if f.is_file())
            
            return {
                'total_space': usage.total,
                'used_space': usage.used,
                'free_space': usage.free,
                'usage_percent': usage_percent,
                'backup_size': backup_size,
                'status': 'warning' if usage_percent > 80 else 'ok'
            }
        except Exception as e:
            logger.error(f"Error checking storage usage: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_backup_health(self) -> Dict[str, Any]:
        """Check the health of all backups."""
        try:
            results = {
                'total_backups': 0,
                'healthy_backups': 0,
                'corrupted_backups': 0,
                'missing_backups': 0,
                'backups': []
            }
            
            # Get expected backup schedule
            schedule = self.config.get('backup_schedule', {})
            frequency = schedule.get('frequency', 'daily')
            retention = schedule.get('retention_period', 7)
            
            # Calculate expected backup dates
            now = datetime.now()
            if frequency == 'daily':
                expected_dates = [now - timedelta(days=i) for i in range(retention)]
            elif frequency == 'weekly':
                expected_dates = [now - timedelta(weeks=i) for i in range(retention)]
            else:
                expected_dates = [now - timedelta(days=i) for i in range(retention)]
            
            # Check each expected backup
            for date in expected_dates:
                backup_path = self._get_backup_path(date)
                backup_info = self._check_backup(backup_path, date)
                results['backups'].append(backup_info)
                
                if backup_info['status'] == 'healthy':
                    results['healthy_backups'] += 1
                elif backup_info['status'] == 'corrupted':
                    results['corrupted_backups'] += 1
                elif backup_info['status'] == 'missing':
                    results['missing_backups'] += 1
                
                results['total_backups'] += 1
            
            # Calculate overall health
            if results['corrupted_backups'] > 0:
                results['overall_status'] = 'critical'
            elif results['missing_backups'] > 0:
                results['overall_status'] = 'warning'
            else:
                results['overall_status'] = 'healthy'
            
            return results
        except Exception as e:
            logger.error(f"Error checking backup health: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_backup_path(self, date: datetime) -> Path:
        """Get the expected path for a backup on a given date."""
        date_str = date.strftime('%Y%m%d')
        return self.backup_dir / f'backup_{date_str}.enc'
    
    def _check_backup(self, backup_path: Path, expected_date: datetime) -> Dict[str, Any]:
        """Check a single backup file."""
        try:
            if not backup_path.exists():
                return {
                    'date': expected_date.isoformat(),
                    'path': str(backup_path),
                    'status': 'missing',
                    'size': 0,
                    'last_modified': None
                }
            
            # Check file integrity
            try:
                with open(backup_path, 'rb') as f:
                    # Read first 1MB for hash
                    data = f.read(1024 * 1024)
                    file_hash = hashlib.sha256(data).hexdigest()
                
                # Get file stats
                stats = backup_path.stat()
                
                return {
                    'date': expected_date.isoformat(),
                    'path': str(backup_path),
                    'status': 'healthy',
                    'size': stats.st_size,
                    'last_modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    'hash': file_hash
                }
            except Exception as e:
                return {
                    'date': expected_date.isoformat(),
                    'path': str(backup_path),
                    'status': 'corrupted',
                    'error': str(e)
                }
        except Exception as e:
            logger.error(f"Error checking backup {backup_path}: {e}")
            return {
                'date': expected_date.isoformat(),
                'path': str(backup_path),
                'status': 'error',
                'error': str(e)
            }
    
    def send_alert(self, subject: str, message: str) -> bool:
        """Send an alert via email."""
        try:
            email_config = self.config.get('email_notifications', {})
            if not email_config.get('enabled', False):
                logger.info("Email notifications are disabled")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = email_config.get('sender_email')
            msg['To'] = email_config.get('recipient_email')
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port', 587)) as server:
                if email_config.get('use_tls', True):
                    server.starttls()
                if email_config.get('username'):
                    server.login(email_config.get('username'), email_config.get('password'))
                server.send_message(msg)
            
            logger.info(f"Alert sent: {subject}")
            return True
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
            return False
    
    def check_and_alert(self) -> None:
        """Check backup health and storage usage, send alerts if needed."""
        # Check storage usage
        storage_status = self.check_storage_usage()
        if storage_status['status'] == 'warning':
            self.send_alert(
                'Backup Storage Warning',
                f"Backup storage usage is at {storage_status['usage_percent']:.1f}%.\n"
                f"Free space: {storage_status['free_space'] / (1024**3):.1f} GB"
            )
        
        # Check backup health
        health_status = self.check_backup_health()
        if health_status['overall_status'] in ['warning', 'critical']:
            self.send_alert(
                'Backup Health Warning',
                f"Backup health check failed:\n"
                f"Status: {health_status['overall_status']}\n"
                f"Healthy backups: {health_status['healthy_backups']}\n"
                f"Corrupted backups: {health_status['corrupted_backups']}\n"
                f"Missing backups: {health_status['missing_backups']}"
            )

if __name__ == '__main__':
    # Example usage
    monitor = BackupMonitor()
    
    # Check storage usage
    storage_status = monitor.check_storage_usage()
    print("Storage Status:", storage_status)
    
    # Check backup health
    health_status = monitor.check_backup_health()
    print("Backup Health:", health_status)
    
    # Send test alert
    monitor.send_alert(
        'Test Alert',
        'This is a test alert from the backup monitoring system.'
    ) 