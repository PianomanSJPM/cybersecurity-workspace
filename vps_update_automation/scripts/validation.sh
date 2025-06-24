#!/bin/bash

# validation.sh
# Validation functions for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Function to validate JSON format
validate_json() {
    local json_file="$1"
    if ! jq empty "$json_file" 2>/dev/null; then
        echo "Error: Invalid JSON format in $json_file"
        return 1
    fi
    return 0
}

# Function to validate email format
validate_email() {
    local email="$1"
    if ! [[ "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        echo "Error: Invalid email format: $email"
        return 1
    fi
    return 0
}

# Function to validate phone number format
validate_phone() {
    local phone="$1"
    if ! [[ "$phone" =~ ^\+[0-9]{10,15}$ ]]; then
        echo "Error: Invalid phone number format: $phone"
        return 1
    fi
    return 0
}

# Function to validate configuration file
validate_config() {
    local config_file="$1"
    
    # Check if file exists and is readable
    if [ ! -f "$config_file" ]; then
        echo "Error: Configuration file not found at $config_file"
        return 1
    fi
    
    if [ ! -r "$config_file" ]; then
        echo "Error: Configuration file is not readable"
        return 1
    fi
    
    # Validate JSON format
    if ! validate_json "$config_file"; then
        return 1
    fi
    
    # Validate required fields
    local required_fields=(
        ".email.enabled"
        ".email.to"
        ".email.from"
        ".logging.enabled"
        ".logging.file"
        ".update_schedule.enabled"
        ".update_schedule.frequency"
    )
    
    for field in "${required_fields[@]}"; do
        if ! jq -e "$field" "$config_file" >/dev/null 2>&1; then
            echo "Error: Missing required field: $field"
            return 1
        fi
    done
    
    # Validate email if enabled
    if [ "$(jq -r '.email.enabled' "$config_file")" = "true" ]; then
        local email_to=$(jq -r '.email.to' "$config_file")
        if ! validate_email "$email_to"; then
            return 1
        fi
    fi
    
    # Validate SMS configuration if enabled
    if [ "$(jq -r '.sms.enabled' "$config_file")" = "true" ]; then
        local required_sms_fields=(
            ".sms.twilio.account_sid"
            ".sms.twilio.auth_token"
            ".sms.twilio.from_number"
            ".sms.twilio.to_number"
        )
        
        for field in "${required_sms_fields[@]}"; do
            if ! jq -e "$field" "$config_file" >/dev/null 2>&1; then
                echo "Error: Missing required SMS field: $field"
                return 1
            fi
        done
        
        # Validate phone numbers
        local from_number=$(jq -r '.sms.twilio.from_number' "$config_file")
        local to_number=$(jq -r '.sms.twilio.to_number' "$config_file")
        
        if ! validate_phone "$from_number"; then
            return 1
        fi
        
        if ! validate_phone "$to_number"; then
            return 1
        fi
    fi
    
    # Validate update schedule
    local frequency=$(jq -r '.update_schedule.frequency' "$config_file")
    if ! [[ "$frequency" =~ ^(daily|weekly|monthly)$ ]]; then
        echo "Error: Invalid update frequency: $frequency"
        return 1
    fi
    
    if [ "$frequency" = "weekly" ]; then
        local day=$(jq -r '.update_schedule.day' "$config_file")
        if ! [[ "$day" =~ ^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$ ]]; then
            echo "Error: Invalid update day: $day"
            return 1
        fi
    fi
    
    # Validate time format
    local time=$(jq -r '.update_schedule.time' "$config_file")
    if ! [[ "$time" =~ ^([01]?[0-9]|2[0-3]):[0-5][0-9]$ ]]; then
        echo "Error: Invalid time format: $time"
        return 1
    fi
    
    return 0
}

# Function to check system requirements
check_system_requirements() {
    # Check required commands
    local required_commands=(
        "apt-get"
        "mail"
        "curl"
        "jq"
        "systemctl"
        "dpkg"
    )
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: Required command not found: $cmd"
            return 1
        fi
    done
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        echo "Error: Script must be run as root"
        return 1
    fi
    
    # Check disk space
    local required_space=1024  # 1GB in MB
    local available_space=$(df -m / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt "$required_space" ]; then
        echo "Error: Insufficient disk space. Required: ${required_space}MB, Available: ${available_space}MB"
        return 1
    fi
    
    # Check memory
    local required_memory=512  # 512MB in MB
    local available_memory=$(free -m | awk '/^Mem:/{print $7}')
    if [ "$available_memory" -lt "$required_memory" ]; then
        echo "Error: Insufficient memory. Required: ${required_memory}MB, Available: ${available_memory}MB"
        return 1
    fi
    
    # Check if system is in a good state
    if ! systemctl is-system-running &> /dev/null; then
        echo "Error: System is not in a good state"
        return 1
    fi
    
    return 0
}

# Function to verify package integrity
verify_package_integrity() {
    # Check for broken packages
    if ! apt-get check &> /dev/null; then
        echo "Error: Package integrity check failed"
        return 1
    fi
    
    # Check for held packages
    if dpkg --get-selections | grep -q "^.*hold$"; then
        echo "Warning: Some packages are held back"
    fi
    
    # Check for broken dependencies
    if ! apt-get -s check &> /dev/null; then
        echo "Error: Broken dependencies found"
        return 1
    fi
    
    return 0
}

# Function to validate system state
validate_system_state() {
    # Check if system is in maintenance mode
    if [ -f /var/run/systemd/maintenance ]; then
        echo "Error: System is in maintenance mode"
        return 1
    fi
    
    # Check if system is in emergency mode
    if systemctl is-system-running | grep -q "emergency"; then
        echo "Error: System is in emergency mode"
        return 1
    fi
    
    # Check if critical services are running
    local critical_services=(
        "sshd"
        "systemd-journald"
        "systemd-logind"
    )
    
    for service in "${critical_services[@]}"; do
        if ! systemctl is-active "$service" &> /dev/null; then
            echo "Error: Critical service $service is not running"
            return 1
        fi
    done
    
    return 0
}

# Function to validate file permissions
validate_file_permissions() {
    local config_file="$1"
    local log_file="$2"
    
    # Check config file permissions
    if [ -f "$config_file" ]; then
        local perms=$(stat -c "%a" "$config_file")
        if [ "$perms" != "644" ]; then
            echo "Error: Invalid permissions on config file: $perms"
            return 1
        fi
    fi
    
    # Check log file permissions
    if [ -f "$log_file" ]; then
        local perms=$(stat -c "%a" "$log_file")
        if [ "$perms" != "644" ]; then
            echo "Error: Invalid permissions on log file: $perms"
            return 1
        fi
    fi
    
    return 0
}

# Function to validate network connectivity
validate_network() {
    # Check if we can reach the package repositories
    if ! ping -c 1 -W 5 security.ubuntu.com &> /dev/null; then
        echo "Error: Cannot reach Ubuntu security repository"
        return 1
    fi
    
    # Check if we can reach the DNS servers
    if ! ping -c 1 -W 5 8.8.8.8 &> /dev/null; then
        echo "Error: Cannot reach external network"
        return 1
    fi
    
    return 0
}

# Export functions
export -f validate_json
export -f validate_email
export -f validate_phone
export -f validate_config
export -f check_system_requirements
export -f verify_package_integrity
export -f validate_system_state
export -f validate_file_permissions
export -f validate_network 