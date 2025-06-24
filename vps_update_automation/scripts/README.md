# VPS Update Automation Script

This script automates the process of updating a VPS (Virtual Private Server) running a Debian-based Linux distribution (Ubuntu, Debian, etc.).

## Features

- Updates package lists
- Upgrades installed packages
- Removes unnecessary packages
- Cleans package cache
- Logs all actions
- Checks if reboot is required
- Includes error handling
- Provides detailed system information
- Sends email notifications with update reports
- Sends SMS notifications for important events
- Includes test functions for notifications

## Prerequisites

- A VPS running a Debian-based Linux distribution
- Root or sudo access
- Basic understanding of Linux commands
- Email address for notifications
- (Optional) Twilio account for SMS notifications

## Installation

1. Copy the script to your VPS:
   ```bash
   scp auto_update.sh user@your-vps-ip:/path/to/destination
   ```

2. Make the script executable:
   ```bash
   chmod +x auto_update.sh
   ```

3. Configure email settings:
   - Open the script in a text editor
   - Change `EMAIL_TO="your-email@example.com"` to your email address
   - The script will automatically install `mailutils` if not present

4. (Optional) Configure SMS settings:
   - Sign up for a Twilio account
   - Get your Account SID and Auth Token
   - Update the script with your Twilio credentials:
     ```bash
     TWILIO_ACCOUNT_SID="your_account_sid"
     TWILIO_AUTH_TOKEN="your_auth_token"
     TWILIO_FROM_NUMBER="+1234567890"
     TWILIO_TO_NUMBER="+1234567890"
     ```

## Usage

### Manual Run

To run the script manually:
```bash
sudo ./auto_update.sh
```

### Test Notifications

To test your email and SMS configuration:
```bash
sudo ./auto_update.sh --test
```

### Automated Run with Cron

To automate the updates, add the script to crontab:

1. Open crontab:
   ```bash
   sudo crontab -e
   ```

2. Add a line to run the script weekly (e.g., every Sunday at 2 AM):
   ```bash
   0 2 * * 0 /path/to/auto_update.sh
   ```

## System Information

The script collects and reports detailed system information:

### Basic Information
- OS version and kernel
- Hostname and uptime
- IP address

### Hardware Information
- CPU model and cores
- CPU load
- Memory usage
- Disk usage

### Network Information
- Network interfaces
- IP addresses
- Connection status

### Security Information
- Recent failed login attempts
- Running services
- System status

## Notifications

### Email Notifications
The script sends email notifications in the following cases:
- When updates start
- When updates complete successfully
- If any errors occur during the update process
- If a system reboot is required

The email includes:
- Timestamp of the update
- Success/failure status
- Detailed system information
- Any error messages

### SMS Notifications
The script sends SMS notifications for:
- Start of updates
- Successful completion
- Errors
- Reboot requirements

## Logging

The script creates a log file at `/var/log/system_updates.log` that includes:
- Timestamp of each action
- Success/failure of each step
- Detailed system information
- Any errors encountered

## Security Considerations

1. Always review the updates before applying them
2. Keep backups of important data
3. Monitor the logs for any issues
4. Check email and SMS notifications regularly
5. Ensure your email address and phone number are correct
6. Keep your Twilio credentials secure

## Customization

You can modify the script to:
- Change the log file location
- Modify email and SMS notification settings
- Modify the update schedule
- Add additional system checks
- Enable automatic reboots
- Add more detailed system information

## Troubleshooting

If you encounter issues:
1. Check the log file at `/var/log/system_updates.log`
2. Check your email for error notifications
3. Check your phone for SMS notifications
4. Run the test function: `sudo ./auto_update.sh --test`
5. Ensure you have proper permissions
6. Verify your internet connection
7. Check disk space availability
8. Verify email and SMS configuration

## Best Practices

1. Test the script in a non-production environment first
2. Schedule updates during low-traffic periods
3. Monitor system resources during updates
4. Keep a backup of the script
5. Review logs and notifications regularly
6. Keep your contact information up to date
7. Regularly test your notification settings

## Contributing

Feel free to modify the script to suit your needs. Common modifications include:
- Adding more detailed system information
- Customizing notification formats
- Adding more security checks
- Implementing different logging methods
- Adding support for other SMS providers 