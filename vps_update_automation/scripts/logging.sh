#!/bin/bash

# logging.sh
# Logging functions for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Configuration
LOG_LEVELS=("DEBUG" "INFO" "WARNING" "ERROR" "CRITICAL")
DEFAULT_LOG_LEVEL="INFO"
LOG_FORMAT="%Y-%m-%d %H:%M:%S"
MAX_LOG_SIZE=10485760  # 10MB in bytes
MAX_LOG_FILES=5

# Function to get current log level
get_log_level() {
    local level="$1"
    for i in "${!LOG_LEVELS[@]}"; do
        if [ "${LOG_LEVELS[$i]}" = "$level" ]; then
            echo $i
            return 0
        fi
    done
    return 1
}

# Function to rotate log files
rotate_logs() {
    local log_file="$1"
    
    if [ ! -f "$log_file" ]; then
        return 0
    fi
    
    # Check if log file needs rotation
    local size=$(stat -c%s "$log_file" 2>/dev/null)
    if [ "$size" -lt "$MAX_LOG_SIZE" ]; then
        return 0
    fi
    
    # Rotate existing log files
    for ((i=MAX_LOG_FILES-1; i>0; i--)); do
        if [ -f "${log_file}.$i" ]; then
            mv "${log_file}.$i" "${log_file}.$((i+1))"
        fi
    done
    
    # Move current log file
    if [ -f "$log_file" ]; then
        mv "$log_file" "${log_file}.1"
    fi
    
    # Create new log file
    touch "$log_file"
    chmod 644 "$log_file"
}

# Function to write log message
write_log() {
    local level="$1"
    local message="$2"
    local log_file="$3"
    local timestamp=$(date +"$LOG_FORMAT")
    
    # Get numeric log levels
    local msg_level=$(get_log_level "$level")
    local current_level=$(get_log_level "${LOG_LEVEL:-$DEFAULT_LOG_LEVEL}")
    
    # Check if message should be logged based on level
    if [ "$msg_level" -lt "$current_level" ]; then
        return 0
    fi
    
    # Rotate logs if necessary
    rotate_logs "$log_file"
    
    # Write log message
    echo "[$timestamp] [$level] $message" >> "$log_file"
    
    # Also write to system log if level is WARNING or higher
    if [ "$msg_level" -ge $(get_log_level "WARNING") ]; then
        logger -t "vps_update" -p "user.$level" "$message"
    fi
}

# Function to log debug message
log_debug() {
    write_log "DEBUG" "$1" "${LOG_FILE:-/var/log/vps_updates.log}"
}

# Function to log info message
log_info() {
    write_log "INFO" "$1" "${LOG_FILE:-/var/log/vps_updates.log}"
}

# Function to log warning message
log_warning() {
    write_log "WARNING" "$1" "${LOG_FILE:-/var/log/vps_updates.log}"
}

# Function to log error message
log_error() {
    write_log "ERROR" "$1" "${LOG_FILE:-/var/log/vps_updates.log}"
}

# Function to log critical message
log_critical() {
    write_log "CRITICAL" "$1" "${LOG_FILE:-/var/log/vps_updates.log}"
}

# Function to set log level
set_log_level() {
    local level="$1"
    if get_log_level "$level" >/dev/null; then
        LOG_LEVEL="$level"
        return 0
    else
        echo "Error: Invalid log level: $level"
        return 1
    fi
}

# Function to get log statistics
get_log_stats() {
    local log_file="$1"
    local period="$2"  # daily, weekly, monthly
    
    if [ ! -f "$log_file" ]; then
        echo "Error: Log file not found: $log_file"
        return 1
    fi
    
    case "$period" in
        "daily")
            local date_filter=$(date +%Y-%m-%d)
            ;;
        "weekly")
            local date_filter=$(date +%Y-%W)
            ;;
        "monthly")
            local date_filter=$(date +%Y-%m)
            ;;
        *)
            echo "Error: Invalid period: $period"
            return 1
            ;;
    esac
    
    # Count messages by level
    echo "=== Log Statistics for $period ==="
    echo "Total messages: $(grep -c "\[$date_filter" "$log_file")"
    echo "By level:"
    for level in "${LOG_LEVELS[@]}"; do
        local count=$(grep -c "\[$date_filter.*\[$level\]" "$log_file")
        echo "  $level: $count"
    done
    
    # Get most common messages
    echo -e "\nMost common messages:"
    grep "\[$date_filter" "$log_file" | cut -d']' -f3- | sort | uniq -c | sort -nr | head -n 5
    
    return 0
}

# Function to clean old log files
clean_logs() {
    local log_dir="$1"
    local max_age="$2"  # in days
    
    if [ ! -d "$log_dir" ]; then
        echo "Error: Log directory not found: $log_dir"
        return 1
    fi
    
    # Find and remove old log files
    find "$log_dir" -name "*.log.*" -type f -mtime +"$max_age" -delete
    
    return 0
}

# Export functions
export -f get_log_level
export -f rotate_logs
export -f write_log
export -f log_debug
export -f log_info
export -f log_warning
export -f log_error
export -f log_critical
export -f set_log_level
export -f get_log_stats
export -f clean_logs 