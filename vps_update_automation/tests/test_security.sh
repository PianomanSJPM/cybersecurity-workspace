#!/bin/bash

# test_security.sh
# Test suite for security module
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Source the security module
source ../scripts/security.sh

# Test configuration
TEST_LOG="/tmp/security_test.log"
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo "Running test: $test_name"
    
    # Run the test command
    eval "$test_command"
    local result=$?
    
    # Check the result
    if [ "$result" -eq "$expected_result" ]; then
        echo "PASS: $test_name"
        ((PASSED++))
    else
        echo "FAIL: $test_name"
        ((FAILED++))
    fi
}

# Test check_failed_logins
test_check_failed_logins() {
    # Create a temporary auth.log with failed login attempts
    local temp_auth_log="/tmp/auth.log"
    echo "Failed password for user1" > "$temp_auth_log"
    echo "Failed password for user2" >> "$temp_auth_log"
    echo "Failed password for user3" >> "$temp_auth_log"
    
    # Set the auth log path for testing
    local original_auth_log="/var/log/auth.log"
    export AUTH_LOG="$temp_auth_log"
    
    # Run the test
    run_test "check_failed_logins" "check_failed_logins" 0
    
    # Clean up
    rm "$temp_auth_log"
    export AUTH_LOG="$original_auth_log"
}

# Test check_suspicious_processes
test_check_suspicious_processes() {
    # Create a temporary process list
    local temp_ps_output="/tmp/ps_output"
    echo "user 1000 10.0 0.0 1000 1000 ? S 10:00 0:00 /bin/bash" > "$temp_ps_output"
    
    # Set the ps output for testing
    local original_ps_command="ps aux"
    export PS_COMMAND="cat $temp_ps_output"
    
    # Run the test
    run_test "check_suspicious_processes" "check_suspicious_processes" 0
    
    # Clean up
    rm "$temp_ps_output"
    export PS_COMMAND="$original_ps_command"
}

# Test check_open_ports
test_check_open_ports() {
    # Create a temporary netstat output
    local temp_netstat_output="/tmp/netstat_output"
    echo "tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN" > "$temp_netstat_output"
    
    # Set the netstat output for testing
    local original_netstat_command="netstat -tuln"
    export NETSTAT_COMMAND="cat $temp_netstat_output"
    
    # Run the test
    run_test "check_open_ports" "check_open_ports" 0
    
    # Clean up
    rm "$temp_netstat_output"
    export NETSTAT_COMMAND="$original_netstat_command"
}

# Test check_file_integrity
test_check_file_integrity() {
    # Create temporary test files
    local temp_dir="/tmp/test_files"
    mkdir -p "$temp_dir"
    
    # Create test files with correct permissions
    touch "$temp_dir/passwd"
    chmod 644 "$temp_dir/passwd"
    
    # Set the critical files for testing
    local original_critical_files=("${CRITICAL_FILES[@]}")
    CRITICAL_FILES=("$temp_dir/passwd")
    
    # Run the test
    run_test "check_file_integrity" "check_file_integrity" 0
    
    # Clean up
    rm -rf "$temp_dir"
    CRITICAL_FILES=("${original_critical_files[@]}")
}

# Test check_system_security
test_check_system_security() {
    # Mock the required functions
    function check_failed_logins() { return 0; }
    function check_suspicious_processes() { return 0; }
    function check_open_ports() { return 0; }
    function check_file_integrity() { return 0; }
    
    # Run the test
    run_test "check_system_security" "check_system_security" 0
    
    # Restore original functions
    unset -f check_failed_logins
    unset -f check_suspicious_processes
    unset -f check_open_ports
    unset -f check_file_integrity
}

# Test monitor_system_resources
test_monitor_system_resources() {
    # Create temporary system files
    local temp_proc="/tmp/proc"
    mkdir -p "$temp_proc"
    
    # Create mock CPU info
    echo "cpu 10 20 30 40" > "$temp_proc/stat"
    
    # Set the proc path for testing
    local original_proc_path="/proc"
    export PROC_PATH="$temp_proc"
    
    # Run the test
    run_test "monitor_system_resources" "monitor_system_resources" 0
    
    # Clean up
    rm -rf "$temp_proc"
    export PROC_PATH="$original_proc_path"
}

# Test check_system_updates
test_check_system_updates() {
    # Create temporary apt output
    local temp_apt_output="/tmp/apt_output"
    echo "No packages need to be upgraded" > "$temp_apt_output"
    
    # Set the apt command for testing
    local original_apt_command="apt-get -s upgrade"
    export APT_COMMAND="cat $temp_apt_output"
    
    # Run the test
    run_test "check_system_updates" "check_system_updates" 0
    
    # Clean up
    rm "$temp_apt_output"
    export APT_COMMAND="$original_apt_command"
}

# Test check_vulnerabilities
test_check_vulnerabilities() {
    # Create temporary checkrestart output
    local temp_checkrestart_output="/tmp/checkrestart_output"
    echo "No services need to be restarted" > "$temp_checkrestart_output"
    
    # Set the checkrestart command for testing
    local original_checkrestart_command="checkrestart"
    export CHECKRESTART_COMMAND="cat $temp_checkrestart_output"
    
    # Run the test
    run_test "check_vulnerabilities" "check_vulnerabilities" 0
    
    # Clean up
    rm "$temp_checkrestart_output"
    export CHECKRESTART_COMMAND="$original_checkrestart_command"
}

# Test generate_security_report
test_generate_security_report() {
    # Run the test
    local report_file=$(generate_security_report)
    
    # Check if report file exists
    if [ -f "$report_file" ]; then
        echo "PASS: generate_security_report"
        ((PASSED++))
    else
        echo "FAIL: generate_security_report"
        ((FAILED++))
    fi
    
    # Clean up
    rm "$report_file"
}

# Run all tests
echo "Starting security module tests..."
echo "--------------------------------"

test_check_failed_logins
test_check_suspicious_processes
test_check_open_ports
test_check_file_integrity
test_check_system_security
test_monitor_system_resources
test_check_system_updates
test_check_vulnerabilities
test_generate_security_report

# Print test summary
echo "--------------------------------"
echo "Test Summary:"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total: $((PASSED + FAILED))"

# Exit with appropriate status
if [ "$FAILED" -eq 0 ]; then
    exit 0
else
    exit 1
fi 