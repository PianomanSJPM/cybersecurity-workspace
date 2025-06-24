#!/bin/bash

# monitoring.sh
# Monitoring functions for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Configuration
MONITOR_LOG="/var/log/vps_monitor.log"
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=80
ALERT_THRESHOLD_DISK=80
CHECK_INTERVAL=300  # 5 minutes

# Function to monitor CPU usage
monitor_cpu() {
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    if (( $(echo "$cpu_usage > $ALERT_THRESHOLD_CPU" | bc -l) )); then
        log_warning "High CPU usage: $cpu_usage%"
        return 1
    fi
    return 0
}

# Function to monitor memory usage
monitor_memory() {
    local mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if (( $(echo "$mem_usage > $ALERT_THRESHOLD_MEMORY" | bc -l) )); then
        log_warning "High memory usage: $mem_usage%"
        return 1
    fi
    return 0
}

# Function to monitor disk usage
monitor_disk() {
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt "$ALERT_THRESHOLD_DISK" ]; then
        log_warning "High disk usage: $disk_usage%"
        return 1
    fi
    return 0
}

# Function to monitor network traffic
monitor_network() {
    # Get network interface statistics
    local interface=$(ip route | grep default | awk '{print $5}')
    local rx_bytes=$(cat /sys/class/net/$interface/statistics/rx_bytes)
    local tx_bytes=$(cat /sys/class/net/$interface/statistics/tx_bytes)
    
    # Calculate rates (bytes per second)
    sleep 1
    local rx_bytes_new=$(cat /sys/class/net/$interface/statistics/rx_bytes)
    local tx_bytes_new=$(cat /sys/class/net/$interface/statistics/tx_bytes)
    
    local rx_rate=$((rx_bytes_new - rx_bytes))
    local tx_rate=$((tx_bytes_new - tx_bytes))
    
    # Convert to human-readable format
    local rx_rate_hr=$(numfmt --to=iec-i --suffix=B/s $rx_rate)
    local tx_rate_hr=$(numfmt --to=iec-i --suffix=B/s $tx_rate)
    
    log_info "Network traffic - RX: $rx_rate_hr, TX: $tx_rate_hr"
}

# Function to monitor system load
monitor_load() {
    local load1=$(uptime | awk '{print $10}' | sed 's/,//')
    local load5=$(uptime | awk '{print $11}' | sed 's/,//')
    local load15=$(uptime | awk '{print $12}' | sed 's/,//')
    
    local cpu_cores=$(nproc)
    local load_threshold=$((cpu_cores * 2))
    
    if (( $(echo "$load1 > $load_threshold" | bc -l) )); then
        log_warning "High system load: $load1 (1min), $load5 (5min), $load15 (15min)"
        return 1
    fi
    return 0
}

# Function to monitor service status
monitor_services() {
    local critical_services=(
        "sshd"
        "systemd-journald"
        "systemd-logind"
        "cron"
        "rsyslog"
    )
    
    local failed_services=0
    
    for service in "${critical_services[@]}"; do
        if ! systemctl is-active "$service" > /dev/null; then
            log_warning "Service $service is not running"
            failed_services=1
        fi
    done
    
    return $failed_services
}

# Function to monitor log files
monitor_logs() {
    local log_files=(
        "/var/log/auth.log"
        "/var/log/syslog"
        "/var/log/messages"
    )
    
    local error_patterns=(
        "error"
        "failed"
        "critical"
        "emergency"
        "alert"
    )
    
    for log_file in "${log_files[@]}"; do
        if [ -f "$log_file" ]; then
            for pattern in "${error_patterns[@]}"; do
                if grep -i "$pattern" "$log_file" | tail -n 5 > /dev/null; then
                    log_warning "Errors found in $log_file matching pattern: $pattern"
                fi
            done
        fi
    done
}

# Function to monitor system temperature
monitor_temperature() {
    if command -v sensors > /dev/null; then
        local temp=$(sensors | grep "Core 0" | awk '{print $3}' | sed 's/+//' | sed 's/°C//')
        if (( $(echo "$temp > 80" | bc -l) )); then
            log_warning "High CPU temperature: $temp°C"
            return 1
        fi
    fi
    return 0
}

# Function to monitor system uptime
monitor_uptime() {
    local uptime_seconds=$(cat /proc/uptime | awk '{print $1}')
    local uptime_days=$(echo "scale=2; $uptime_seconds/86400" | bc)
    
    log_info "System uptime: $uptime_days days"
}

# Function to monitor system resources
monitor_resources() {
    local issues_found=0
    
    # Monitor CPU
    if ! monitor_cpu; then
        issues_found=1
    fi
    
    # Monitor memory
    if ! monitor_memory; then
        issues_found=1
    fi
    
    # Monitor disk
    if ! monitor_disk; then
        issues_found=1
    fi
    
    # Monitor network
    monitor_network
    
    # Monitor system load
    if ! monitor_load; then
        issues_found=1
    fi
    
    # Monitor services
    if ! monitor_services; then
        issues_found=1
    fi
    
    # Monitor logs
    monitor_logs
    
    # Monitor temperature
    if ! monitor_temperature; then
        issues_found=1
    fi
    
    # Monitor uptime
    monitor_uptime
    
    return $issues_found
}

# Function to generate monitoring report
generate_monitoring_report() {
    local report_file="/tmp/monitoring_report_$$.txt"
    
    {
        echo "=== Monitoring Report ==="
        echo "Generated: $(date)"
        echo -e "\n=== System Resources ==="
        echo "CPU Usage:"
        top -bn1 | grep "Cpu(s)"
        echo -e "\nMemory Usage:"
        free -h
        echo -e "\nDisk Usage:"
        df -h
        echo -e "\nSystem Load:"
        uptime
        echo -e "\n=== Network Statistics ==="
        netstat -i
        echo -e "\n=== Service Status ==="
        systemctl list-units --state=failed
        echo -e "\n=== Recent Errors ==="
        journalctl -p err -n 10
    } > "$report_file"
    
    echo "$report_file"
}

# Function to start continuous monitoring
start_monitoring() {
    log_info "Starting continuous monitoring..."
    
    while true; do
        monitor_resources
        sleep "$CHECK_INTERVAL"
    done
}

# Export functions
export -f monitor_cpu
export -f monitor_memory
export -f monitor_disk
export -f monitor_network
export -f monitor_load
export -f monitor_services
export -f monitor_logs
export -f monitor_temperature
export -f monitor_uptime
export -f monitor_resources
export -f generate_monitoring_report
export -f start_monitoring 