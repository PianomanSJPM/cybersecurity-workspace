#!/bin/bash

# security.sh
# Security functions for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Configuration
SECURITY_LOG="/var/log/vps_security.log"
FAILED_LOGIN_THRESHOLD=5
SUSPICIOUS_PORTS=(21 23 445 3389)  # Common ports to monitor
CRITICAL_SERVICES=("sshd" "systemd-journald" "systemd-logind")

# Function to check for failed login attempts
check_failed_logins() {
    local threshold=$FAILED_LOGIN_THRESHOLD
    local failed_logins=$(grep "Failed password" /var/log/auth.log | wc -l)
    
    if [ "$failed_logins" -gt "$threshold" ]; then
        log_warning "High number of failed login attempts: $failed_logins"
        return 1
    fi
    return 0
}

# Function to check for suspicious processes
check_suspicious_processes() {
    local suspicious_found=0
    
    # Check for common malware indicators
    local suspicious_patterns=(
        "cryptominer"
        "miner"
        "botnet"
        "backdoor"
        "rootkit"
    )
    
    for pattern in "${suspicious_patterns[@]}"; do
        if ps aux | grep -i "$pattern" | grep -v grep > /dev/null; then
            log_warning "Suspicious process found matching pattern: $pattern"
            suspicious_found=1
        fi
    done
    
    # Check for processes with high CPU usage
    ps aux | awk '$3 > 80.0 {print $0}' | while read -r line; do
        log_warning "Process with high CPU usage: $line"
        suspicious_found=1
    done
    
    return $suspicious_found
}

# Function to check for open ports
check_open_ports() {
    local suspicious_found=0
    
    # Check for suspicious ports
    for port in "${SUSPICIOUS_PORTS[@]}"; do
        if netstat -tuln | grep ":$port " > /dev/null; then
            log_warning "Suspicious port $port is open"
            suspicious_found=1
        fi
    done
    
    # Check for unexpected listening ports
    local expected_ports=("22" "80" "443")  # Add your expected ports
    netstat -tuln | grep LISTEN | while read -r line; do
        local port=$(echo "$line" | awk '{print $4}' | cut -d':' -f2)
        if ! [[ " ${expected_ports[@]} " =~ " ${port} " ]]; then
            log_warning "Unexpected port $port is open"
            suspicious_found=1
        fi
    done
    
    return $suspicious_found
}

# Function to check file integrity
check_file_integrity() {
    local critical_files=(
        "/etc/passwd"
        "/etc/shadow"
        "/etc/group"
        "/etc/sudoers"
        "/etc/ssh/sshd_config"
    )
    
    local changes_found=0
    
    for file in "${critical_files[@]}"; do
        if [ -f "$file" ]; then
            # Check file permissions
            local perms=$(stat -c "%a" "$file")
            if [ "$perms" != "644" ] && [ "$perms" != "600" ]; then
                log_warning "Incorrect permissions on $file: $perms"
                changes_found=1
            fi
            
            # Check for recent modifications
            local mtime=$(stat -c "%Y" "$file")
            local now=$(date +%s)
            local age=$((now - mtime))
            
            if [ "$age" -lt 3600 ]; then  # Modified in last hour
                log_warning "Recent modification detected on $file"
                changes_found=1
            fi
        fi
    done
    
    return $changes_found
}

# Function to check system security
check_system_security() {
    local security_issues=0
    
    # Check for failed logins
    if ! check_failed_logins; then
        security_issues=1
    fi
    
    # Check for suspicious processes
    if ! check_suspicious_processes; then
        security_issues=1
    fi
    
    # Check for open ports
    if ! check_open_ports; then
        security_issues=1
    fi
    
    # Check file integrity
    if ! check_file_integrity; then
        security_issues=1
    fi
    
    # Check for critical services
    for service in "${CRITICAL_SERVICES[@]}"; do
        if ! systemctl is-active "$service" > /dev/null; then
            log_warning "Critical service $service is not running"
            security_issues=1
        fi
    done
    
    # Check for root login attempts
    if grep "root" /var/log/auth.log | grep "Failed password" > /dev/null; then
        log_warning "Root login attempts detected"
        security_issues=1
    fi
    
    # Check for sudo usage
    if grep "sudo" /var/log/auth.log | grep "session opened" > /dev/null; then
        log_info "Sudo sessions detected, reviewing..."
        grep "sudo" /var/log/auth.log | grep "session opened" | tail -n 5 >> "$SECURITY_LOG"
    fi
    
    return $security_issues
}

# Function to monitor system resources
monitor_system_resources() {
    # CPU usage
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        log_warning "High CPU usage: $cpu_usage%"
    fi
    
    # Memory usage
    local mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if (( $(echo "$mem_usage > 80" | bc -l) )); then
        log_warning "High memory usage: $mem_usage%"
    fi
    
    # Disk usage
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 80 ]; then
        log_warning "High disk usage: $disk_usage%"
    fi
    
    # Check for large files
    find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null | while read -r line; do
        log_info "Large file found: $line"
    done
}

# Function to check for system updates
check_system_updates() {
    # Check for available security updates
    if apt-get -s upgrade | grep -i security > /dev/null; then
        log_warning "Security updates available"
        return 1
    fi
    
    # Check for available package updates
    if apt-get -s upgrade | grep -i "upgraded" > /dev/null; then
        log_info "Package updates available"
        return 1
    fi
    
    return 0
}

# Function to check for system vulnerabilities
check_vulnerabilities() {
    # Check for known vulnerabilities
    if command -v debian-goodies > /dev/null; then
        checkrestart | grep -i "vulnerable" > /dev/null && {
            log_warning "Vulnerable services detected"
            return 1
        }
    fi
    
    # Check for outdated packages
    apt-get -s upgrade | grep -i "security" > /dev/null && {
        log_warning "Outdated packages with security implications"
        return 1
    }
    
    return 0
}

# Function to generate security report
generate_security_report() {
    local report_file="/tmp/security_report_$$.txt"
    
    {
        echo "=== Security Report ==="
        echo "Generated: $(date)"
        echo -e "\n=== System Information ==="
        uname -a
        echo -e "\n=== Failed Login Attempts ==="
        grep "Failed password" /var/log/auth.log | tail -n 10
        echo -e "\n=== Open Ports ==="
        netstat -tuln
        echo -e "\n=== Running Processes ==="
        ps aux | grep -v grep
        echo -e "\n=== System Resources ==="
        top -bn1 | head -n 5
        free -h
        df -h
        echo -e "\n=== Security Checks ==="
        check_system_security
        echo -e "\n=== Available Updates ==="
        apt-get -s upgrade | grep -i "security"
    } > "$report_file"
    
    echo "$report_file"
}

# Export functions
export -f check_failed_logins
export -f check_suspicious_processes
export -f check_open_ports
export -f check_file_integrity
export -f check_system_security
export -f monitor_system_resources
export -f check_system_updates
export -f check_vulnerabilities
export -f generate_security_report 