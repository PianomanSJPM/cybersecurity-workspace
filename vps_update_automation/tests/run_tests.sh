#!/bin/bash

# run_tests.sh
# Test runner for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Configuration
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$TEST_DIR/../scripts"
LOG_FILE="/tmp/vps_update_tests.log"
TOTAL_PASSED=0
TOTAL_FAILED=0

# Function to run a test suite
run_test_suite() {
    local test_file="$1"
    local test_name=$(basename "$test_file" .sh)
    
    echo "Running test suite: $test_name"
    echo "--------------------------------"
    
    # Run the test suite
    bash "$test_file"
    local result=$?
    
    # Update totals
    if [ $result -eq 0 ]; then
        echo "PASS: $test_name test suite"
        ((TOTAL_PASSED++))
    else
        echo "FAIL: $test_name test suite"
        ((TOTAL_FAILED++))
    fi
    
    echo "--------------------------------"
    echo
}

# Function to check test dependencies
check_dependencies() {
    local missing_deps=0
    
    # Check for required commands
    local required_commands=(
        "bash"
        "grep"
        "awk"
        "sed"
        "bc"
        "numfmt"
    )
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" > /dev/null; then
            echo "Error: Required command '$cmd' not found"
            missing_deps=1
        fi
    done
    
    # Check for required files
    local required_files=(
        "$SCRIPTS_DIR/security.sh"
        "$SCRIPTS_DIR/monitoring.sh"
        "$SCRIPTS_DIR/logging.sh"
        "$SCRIPTS_DIR/validation.sh"
        "$SCRIPTS_DIR/backup.sh"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo "Error: Required file '$file' not found"
            missing_deps=1
        fi
    done
    
    return $missing_deps
}

# Function to clean up test artifacts
cleanup() {
    # Remove temporary files
    rm -f /tmp/*_test.log
    rm -f /tmp/*_output
    rm -f /tmp/*_report_*.txt
    
    # Remove temporary directories
    rm -rf /tmp/test_*
    rm -rf /tmp/logs
    rm -rf /tmp/sys
}

# Main function
main() {
    # Check dependencies
    if ! check_dependencies; then
        echo "Error: Missing dependencies. Please install required packages and ensure all script files exist."
        exit 1
    fi
    
    # Clean up any existing test artifacts
    cleanup
    
    # Run all test suites
    echo "Starting VPS Update Automation tests..."
    echo "======================================"
    echo
    
    # Find and run all test files
    for test_file in "$TEST_DIR"/test_*.sh; do
        if [ -f "$test_file" ] && [ -x "$test_file" ]; then
            run_test_suite "$test_file"
        fi
    done
    
    # Print final summary
    echo "======================================"
    echo "Test Summary:"
    echo "Total test suites passed: $TOTAL_PASSED"
    echo "Total test suites failed: $TOTAL_FAILED"
    echo "Total test suites: $((TOTAL_PASSED + TOTAL_FAILED))"
    echo "======================================"
    
    # Clean up test artifacts
    cleanup
    
    # Exit with appropriate status
    if [ "$TOTAL_FAILED" -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main 