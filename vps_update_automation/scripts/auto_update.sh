#!/bin/bash

# auto_update.sh
# Script to automate system updates on a VPS
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Source modules
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/validation.sh"
source "$SCRIPT_DIR/backup.sh"
source "$SCRIPT_DIR/logging.sh"

# Configuration
CONFIG_FILE="/etc/vps_update/config.json"
CONFIG_EXAMPLE="/path/to/config.example.json"
LOCK_FILE="/var/run/vps_update.lock"
MAX_RETRIES=3
RETRY_DELAY=60  # seconds

# Function to acquire lock
acquire_lock() {
    if [ -e "$LOCK_FILE" ]; then
        local pid=$(cat "$LOCK_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log_error "Another update process is already running (PID: $pid)"
            return 1
        else
            log_warning "Removing stale lock file"
            rm -f "$LOCK_FILE"
        fi
    fi
    echo $$ > "$LOCK_FILE"
    return 0
}

# Function to release lock
release_lock() {
    rm -f "$LOCK_FILE"
}

# Function to handle cleanup
cleanup() {
    local exit_code=$?
    release_lock
    if [ -f "$TEMP_LOG" ]; then
        rm -f "$TEMP_LOG"
    fi
    exit $exit_code
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Function to load configuration
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        # Validate configuration
        if ! validate_config "$CONFIG_FILE"; then
            log_error "Configuration validation failed"
            return 1
        fi
        
        # Load configuration from file
        EMAIL_TO=$(jq -r '.email.to' "$CONFIG_FILE")
        EMAIL_FROM=$(jq -r '.email.from' "$CONFIG_FILE")
        EMAIL_SUBJECT_PREFIX=$(jq -r '.email.subject_prefix' "$CONFIG_FILE")
        
        # SMS configuration
        if [ "$(jq -r '.sms.enabled' "$CONFIG_FILE")" = "true" ]; then
            TWILIO_ACCOUNT_SID=$(jq -r '.sms.twilio.account_sid' "$CONFIG_FILE")
            TWILIO_AUTH_TOKEN=$(jq -r '.sms.twilio.auth_token' "$CONFIG_FILE")
            TWILIO_FROM_NUMBER=$(jq -r '.sms.twilio.from_number' "$CONFIG_FILE")
            TWILIO_TO_NUMBER=$(jq -r '.sms.twilio.to_number' "$CONFIG_FILE")
        fi
        
        # Logging configuration
        LOG_FILE=$(jq -r '.logging.file' "$CONFIG_FILE")
        LOG_LEVEL=$(jq -r '.logging.level' "$CONFIG_FILE")
        set_log_level "$LOG_LEVEL"
        
        # Update schedule configuration
        UPDATE_FREQUENCY=$(jq -r '.update_schedule.frequency' "$CONFIG_FILE")
        UPDATE_DAY=$(jq -r '.update_schedule.day' "$CONFIG_FILE")
        UPDATE_TIME=$(jq -r '.update_schedule.time' "$CONFIG_FILE")
        AUTO_REBOOT=$(jq -r '.update_schedule.auto_reboot' "$CONFIG_FILE")
        
        # Package configuration
        mapfile -t INCLUDE_PACKAGES < <(jq -r '.update_schedule.packages.include[]' "$CONFIG_FILE")
        mapfile -t EXCLUDE_PACKAGES < <(jq -r '.update_schedule.packages.exclude[]' "$CONFIG_FILE")
    else
        # Use default configuration
        log_warning "Configuration file not found. Using default settings."
        log_info "Please copy $CONFIG_EXAMPLE to $CONFIG_FILE and update the settings."
        EMAIL_TO="your-email@example.com"
        EMAIL_FROM="vps-updates@$(hostname)"
        EMAIL_SUBJECT_PREFIX="VPS Update Report"
        LOG_FILE="/var/log/vps_updates.log"
        LOG_LEVEL="info"
        set_log_level "$LOG_LEVEL"
    fi
}

# Function to retry commands
retry_command() {
    local cmd="$1"
    local max_attempts=$MAX_RETRIES
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if eval "$cmd"; then
            return 0
        fi
        
        log_warning "Command failed (attempt $attempt/$max_attempts): $cmd"
        if [ $attempt -lt $max_attempts ]; then
            sleep $RETRY_DELAY
        fi
        ((attempt++))
    done
    
    return 1
}

# Function to send SMS using Twilio
send_sms() {
    if [ -n "$TWILIO_ACCOUNT_SID" ] && [ -n "$TWILIO_AUTH_TOKEN" ]; then
        if curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
            --data-urlencode "Body=$1" \
            --data-urlencode "From=$TWILIO_FROM_NUMBER" \
            --data-urlencode "To=$TWILIO_TO_NUMBER" \
            -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"; then
            log_info "SMS sent successfully"
            return 0
        else
            log_error "Failed to send SMS"
            return 1
        fi
    fi
    return 0
}

# Function to send email
send_email() {
    if [ -f "$TEMP_LOG" ]; then
        if mail -s "$EMAIL_SUBJECT_PREFIX - $(hostname)" -r "$EMAIL_FROM" "$EMAIL_TO" < "$TEMP_LOG"; then
            log_info "Email sent successfully"
            return 0
        else
            log_error "Failed to send email"
            return 1
        fi
    fi
    return 0
}

# Function to handle errors
handle_error() {
    log_error "$1"
    send_email
    send_sms "VPS Update ERROR on $(hostname): $1"
    exit 1
}

# Main execution
main() {
    # Acquire lock
    if ! acquire_lock; then
        exit 1
    fi
    
    # Check system requirements
    if ! check_system_requirements; then
        handle_error "System requirements check failed"
    fi
    
    # Validate network connectivity
    if ! validate_network; then
        handle_error "Network connectivity check failed"
    fi
    
    # Load and validate configuration
    if ! load_config; then
        handle_error "Failed to load configuration"
    fi
    
    # Create log file if it doesn't exist
    touch "$LOG_FILE" || handle_error "Could not create log file"
    touch "$TEMP_LOG" || handle_error "Could not create temporary log file"
    
    # Backup system state
    log_info "Creating system backup"
    if ! backup_system_state; then
        log_warning "Failed to create system backup"
    fi
    
    # Backup package list
    log_info "Creating package list backup"
    if ! backup_package_list; then
        log_warning "Failed to create package list backup"
    fi
    
    # Backup configuration files
    log_info "Creating configuration backup"
    if ! backup_config_files; then
        log_warning "Failed to create configuration backup"
    fi
    
    log_info "Starting system update process"
    log_info "Sending notifications to: $EMAIL_TO"
    send_sms "VPS Update started on $(hostname)"
    
    # Verify package integrity
    log_info "Verifying package integrity"
    if ! verify_package_integrity; then
        handle_error "Package integrity check failed"
    fi
    
    # Update package lists with retry
    log_info "Updating package lists"
    if ! retry_command "apt-get update"; then
        handle_error "Failed to update package lists after $MAX_RETRIES attempts"
    fi
    
    # Upgrade installed packages with retry
    log_info "Upgrading installed packages"
    if ! retry_command "apt-get upgrade -y"; then
        handle_error "Failed to upgrade packages after $MAX_RETRIES attempts"
    fi
    
    # Remove unnecessary packages
    log_info "Cleaning up unnecessary packages"
    if ! retry_command "apt-get autoremove -y"; then
        handle_error "Failed to remove unnecessary packages after $MAX_RETRIES attempts"
    fi
    
    # Clean package cache
    log_info "Cleaning package cache"
    if ! retry_command "apt-get clean"; then
        handle_error "Failed to clean package cache after $MAX_RETRIES attempts"
    fi
    
    # Get detailed system information
    log_info "Collecting system information"
    get_system_info
    
    # Check if reboot is required
    if [ -f /var/run/reboot-required ]; then
        log_info "System reboot required"
        if [ "$AUTO_REBOOT" = "true" ]; then
            log_info "Auto-reboot enabled. System will reboot in 5 minutes."
            send_sms "VPS Update completed on $(hostname). System will reboot in 5 minutes."
            shutdown -r +5
        else
            send_sms "VPS Update completed on $(hostname). Reboot required."
        fi
    else
        log_info "No reboot required"
        send_sms "VPS Update completed successfully on $(hostname). No reboot required."
    fi
    
    log_info "Update process completed successfully"
    
    # Send email with update report
    send_email
    
    # Clean old logs
    clean_logs "$(dirname "$LOG_FILE")" 30  # Keep logs for 30 days
}

# Execute main function
main

exit 0 