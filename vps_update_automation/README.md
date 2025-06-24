# VPS Update Automation

A comprehensive solution for automating VPS updates with enhanced security monitoring and system health checks.

## Features

### Core Features
- Automated system updates with configurable schedules
- Email and SMS notifications for update events
- Detailed system reporting
- Security monitoring and alerts

### Security Features
- Failed login attempt monitoring
- Suspicious process detection
- Open port monitoring
- File integrity checking
- Critical service monitoring
- Root login attempt detection
- Sudo usage tracking
- System vulnerability scanning

### Monitoring Features
- CPU usage monitoring
- Memory usage tracking
- Disk space monitoring
- Network traffic analysis
- System load monitoring
- Service status checking
- Log file monitoring
- Temperature monitoring (if supported)
- Uptime tracking

### Testing
- Comprehensive test suite for all modules
- Automated test runner
- Dependency checking
- Clean test environment management

## Project Structure

```
vps_update_automation/
├── config/
│   └── config.example.json
├── scripts/
│   ├── auto_update.sh
│   ├── backup.sh
│   ├── logging.sh
│   ├── monitoring.sh
│   ├── security.sh
│   └── validation.sh
├── tests/
│   ├── run_tests.sh
│   ├── test_monitoring.sh
│   └── test_security.sh
├── LICENSE
└── README.md
```

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vps_update_automation.git
   cd vps_update_automation
   ```

2. Copy the example configuration:
   ```bash
   cp config/config.example.json config/config.json
   ```

3. Edit the configuration file:
   ```bash
   nano config/config.json
   ```

4. Make the scripts executable:
   ```bash
   chmod +x scripts/*.sh
   chmod +x tests/*.sh
   ```

5. Run the test suite:
   ```bash
   ./tests/run_tests.sh
   ```

6. Set up the cron job:
   ```bash
   crontab -e
   ```
   Add the following line (adjust the path as needed):
   ```
   0 2 * * * /path/to/vps_update_automation/scripts/auto_update.sh
   ```

## Configuration

The configuration file (`config.json`) supports the following options:

### Email Notifications
```json
{
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender": "your-email@gmail.com",
        "recipient": "admin@example.com",
        "username": "your-email@gmail.com",
        "password": "your-app-password"
    }
}
```

### SMS Notifications (Twilio)
```json
{
    "sms": {
        "enabled": false,
        "twilio_account_sid": "your-account-sid",
        "twilio_auth_token": "your-auth-token",
        "twilio_phone_number": "+1234567890",
        "recipient_phone_number": "+0987654321"
    }
}
```

### Update Schedule
```json
{
    "schedule": {
        "day": "0",
        "hour": "2",
        "minute": "0",
        "auto_reboot": false,
        "include_packages": ["security", "updates"],
        "exclude_packages": []
    }
}
```

### Logging
```json
{
    "logging": {
        "enabled": true,
        "log_file": "/var/log/vps_update.log",
        "max_size": "10M",
        "max_files": 5
    }
}
```

### Security Monitoring
```json
{
    "security": {
        "failed_login_threshold": 5,
        "suspicious_ports": [21, 23, 445, 3389],
        "critical_services": ["sshd", "systemd-journald", "systemd-logind"],
        "check_interval": 300
    }
}
```

### System Monitoring
```json
{
    "monitoring": {
        "cpu_threshold": 80,
        "memory_threshold": 80,
        "disk_threshold": 80,
        "check_interval": 300
    }
}
```

## Security Considerations

- All sensitive information (passwords, tokens) should be stored securely
- The script should be run with appropriate permissions
- Regular security audits should be performed
- Keep the system and all dependencies up to date
- Monitor the logs for any suspicious activity

## Testing

The test suite includes comprehensive tests for all modules:

- Security module tests
- Monitoring module tests
- Logging module tests
- Validation module tests
- Backup module tests

To run the tests:
```bash
./tests/run_tests.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 