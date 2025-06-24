#!/bin/bash

# test_monitoring.sh
# Test suite for monitoring module
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Source the monitoring module
source ../scripts/monitoring.sh

# Test configuration
TEST_LOG="/tmp/monitoring_test.log"
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

# Test monitor_cpu
test_monitor_cpu() {
    # Create temporary top output
    local temp_top_output="/tmp/top_output"
    echo "Cpu(s): 10.0 us, 20.0 sy, 0.0 ni, 70.0 id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st" > "$temp_top_output"
    
    # Set the top command for testing
    local original_top_command="top -bn1"
    export TOP_COMMAND="cat $temp_top_output"
    
    # Run the test
    run_test "monitor_cpu" "monitor_cpu" 0
    
    # Clean up
    rm "$temp_top_output"
    export TOP_COMMAND="$original_top_command"
}

# Test monitor_memory
test_monitor_memory() {
    # Create temporary free output
    local temp_free_output="/tmp/free_output"
    echo "Mem: 1000 200 800 0 0 100" > "$temp_free_output"
    
    # Set the free command for testing
    local original_free_command="free"
    export FREE_COMMAND="cat $temp_free_output"
    
    # Run the test
    run_test "monitor_memory" "monitor_memory" 0
    
    # Clean up
    rm "$temp_free_output"
    export FREE_COMMAND="$original_free_command"
}

# Test monitor_disk
test_monitor_disk() {
    # Create temporary df output
    local temp_df_output="/tmp/df_output"
    echo "Filesystem Size Used Avail Use% Mounted on" > "$temp_df_output"
    echo "/dev/sda1 100G 50G 50G 50% /" >> "$temp_df_output"
    
    # Set the df command for testing
    local original_df_command="df -h"
    export DF_COMMAND="cat $temp_df_output"
    
    # Run the test
    run_test "monitor_disk" "monitor_disk" 0
    
    # Clean up
    rm "$temp_df_output"
    export DF_COMMAND="$original_df_command"
}

# Test monitor_network
test_monitor_network() {
    # Create temporary network statistics
    local temp_net_dir="/tmp/sys/class/net/eth0/statistics"
    mkdir -p "$temp_net_dir"
    
    # Create initial statistics
    echo "1000" > "$temp_net_dir/rx_bytes"
    echo "2000" > "$temp_net_dir/tx_bytes"
    
    # Set the network interface for testing
    local original_interface="eth0"
    export NETWORK_INTERFACE="eth0"
    export SYS_NET_PATH="/tmp/sys/class/net"
    
    # Run the test
    run_test "monitor_network" "monitor_network" 0
    
    # Clean up
    rm -rf "/tmp/sys"
    export NETWORK_INTERFACE="$original_interface"
    export SYS_NET_PATH="/sys/class/net"
}

# Test monitor_load
test_monitor_load() {
    # Create temporary uptime output
    local temp_uptime_output="/tmp/uptime_output"
    echo "10:00:00 up 1 day, 2:00, 1 user, load average: 1.00, 1.00, 1.00" > "$temp_uptime_output"
    
    # Set the uptime command for testing
    local original_uptime_command="uptime"
    export UPTIME_COMMAND="cat $temp_uptime_output"
    
    # Set number of CPU cores for testing
    local original_nproc_command="nproc"
    export NPROC_COMMAND="echo 4"
    
    # Run the test
    run_test "monitor_load" "monitor_load" 0
    
    # Clean up
    rm "$temp_uptime_output"
    export UPTIME_COMMAND="$original_uptime_command"
    export NPROC_COMMAND="$original_nproc_command"
}

# Test monitor_services
test_monitor_services() {
    # Create temporary systemctl output
    local temp_systemctl_output="/tmp/systemctl_output"
    echo "active" > "$temp_systemctl_output"
    
    # Set the systemctl command for testing
    local original_systemctl_command="systemctl is-active"
    export SYSTEMCTL_COMMAND="cat $temp_systemctl_output"
    
    # Run the test
    run_test "monitor_services" "monitor_services" 0
    
    # Clean up
    rm "$temp_systemctl_output"
    export SYSTEMCTL_COMMAND="$original_systemctl_command"
}

# Test monitor_logs
test_monitor_logs() {
    # Create temporary log files
    local temp_log_dir="/tmp/logs"
    mkdir -p "$temp_log_dir"
    
    # Create test log files
    echo "Normal log entry" > "$temp_log_dir/auth.log"
    echo "Error: Something went wrong" >> "$temp_log_dir/auth.log"
    
    # Set the log files for testing
    local original_log_files=("${LOG_FILES[@]}")
    LOG_FILES=("$temp_log_dir/auth.log")
    
    # Run the test
    run_test "monitor_logs" "monitor_logs" 0
    
    # Clean up
    rm -rf "$temp_log_dir"
    LOG_FILES=("${original_log_files[@]}")
}

# Test monitor_temperature
test_monitor_temperature() {
    # Create temporary sensors output
    local temp_sensors_output="/tmp/sensors_output"
    echo "Core 0: +50.0°C" > "$temp_sensors_output"
    
    # Set the sensors command for testing
    local original_sensors_command="sensors"
    export SENSORS_COMMAND="cat $temp_sensors_output"
    
    # Run the test
    run_test "monitor_temperature" "monitor_temperature" 0
    
    # Clean up
    rm "$temp_sensors_output"
    export SENSORS_COMMAND="$original_sensors_command"
}

# Test monitor_uptime
test_monitor_uptime() {
    # Create temporary uptime file
    local temp_uptime_file="/tmp/uptime"
    echo "100000.00 200000.00" > "$temp_uptime_file"
    
    # Set the uptime file for testing
    local original_uptime_file="/proc/uptime"
    export UPTIME_FILE="$temp_uptime_file"
    
    # Run the test
    run_test "monitor_uptime" "monitor_uptime" 0
    
    # Clean up
    rm "$temp_uptime_file"
    export UPTIME_FILE="$original_uptime_file"
}

# Test monitor_resources
test_monitor_resources() {
    # Mock the required functions
    function monitor_cpu() { return 0; }
    function monitor_memory() { return 0; }
    function monitor_disk() { return 0; }
    function monitor_network() { return 0; }
    function monitor_load() { return 0; }
    function monitor_services() { return 0; }
    function monitor_logs() { return 0; }
    function monitor_temperature() { return 0; }
    function monitor_uptime() { return 0; }
    
    # Run the test
    run_test "monitor_resources" "monitor_resources" 0
    
    # Restore original functions
    unset -f monitor_cpu
    unset -f monitor_memory
    unset -f monitor_disk
    unset -f monitor_network
    unset -f monitor_load
    unset -f monitor_services
    unset -f monitor_logs
    unset -f monitor_temperature
    unset -f monitor_uptime
}

# Test generate_monitoring_report
test_generate_monitoring_report() {
    # Run the test
    local report_file=$(generate_monitoring_report)
    
    # Check if report file exists
    if [ -f "$report_file" ]; then
        echo "PASS: generate_monitoring_report"
        ((PASSED++))
    else
        echo "FAIL: generate_monitoring_report"
        ((FAILED++))
    fi
    
    # Clean up
    rm "$report_file"
}

# Run all tests
echo "Starting monitoring module tests..."
echo "--------------------------------"

test_monitor_cpu
test_monitor_memory
test_monitor_disk
test_monitor_network
test_monitor_load
test_monitor_services
test_monitor_logs
test_monitor_temperature
test_monitor_uptime
test_monitor_resources
test_generate_monitoring_report

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