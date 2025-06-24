#!/bin/bash

# backup.sh
# Backup functions for VPS Update Automation
# Author: Your Name
# Date: $(date +%Y-%m-%d)

# Configuration
BACKUP_DIR="/var/backups/vps_update"
MAX_BACKUPS=5
COMPRESS_BACKUPS=true

# Function to create backup directory
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR" || {
            echo "Error: Failed to create backup directory"
            return 1
        }
        chmod 700 "$BACKUP_DIR" || {
            echo "Error: Failed to set backup directory permissions"
            return 1
        }
    fi
    return 0
}

# Function to rotate old backups
rotate_backups() {
    local backup_count=$(ls -1 "$BACKUP_DIR" | wc -l)
    if [ "$backup_count" -gt "$MAX_BACKUPS" ]; then
        local to_delete=$((backup_count - MAX_BACKUPS))
        ls -t "$BACKUP_DIR" | tail -n "$to_delete" | while read -r backup; do
            rm -rf "$BACKUP_DIR/$backup" || {
                echo "Warning: Failed to remove old backup: $backup"
            }
        done
    fi
}

# Function to backup package list
backup_package_list() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$BACKUP_DIR/pkg_list_$timestamp"
    
    # Create backup directory if it doesn't exist
    create_backup_dir || return 1
    
    # Backup package list
    dpkg --get-selections > "$backup_path.txt" || {
        echo "Error: Failed to backup package list"
        return 1
    }
    
    # Compress if enabled
    if [ "$COMPRESS_BACKUPS" = true ]; then
        gzip "$backup_path.txt" || {
            echo "Error: Failed to compress package list backup"
            return 1
        }
    fi
    
    # Set proper permissions
    chmod 600 "$backup_path"* || {
        echo "Warning: Failed to set backup permissions"
    }
    
    return 0
}

# Function to backup configuration files
backup_config_files() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$BACKUP_DIR/config_$timestamp"
    
    # Create backup directory if it doesn't exist
    create_backup_dir || return 1
    
    # Create temporary directory for config files
    local temp_dir=$(mktemp -d) || {
        echo "Error: Failed to create temporary directory"
        return 1
    }
    
    # List of important configuration files to backup
    local config_files=(
        "/etc/apt/sources.list"
        "/etc/apt/sources.list.d/"
        "/etc/apt/apt.conf.d/"
        "/etc/vps_update/config.json"
    )
    
    # Copy configuration files
    for file in "${config_files[@]}"; do
        if [ -e "$file" ]; then
            cp -r "$file" "$temp_dir/" || {
                echo "Warning: Failed to backup $file"
            }
        fi
    done
    
    # Create archive
    if [ "$COMPRESS_BACKUPS" = true ]; then
        tar -czf "$backup_path.tar.gz" -C "$temp_dir" . || {
            echo "Error: Failed to create config backup archive"
            rm -rf "$temp_dir"
            return 1
        }
    else
        tar -cf "$backup_path.tar" -C "$temp_dir" . || {
            echo "Error: Failed to create config backup archive"
            rm -rf "$temp_dir"
            return 1
        }
    fi
    
    # Clean up temporary directory
    rm -rf "$temp_dir"
    
    # Set proper permissions
    chmod 600 "$backup_path"* || {
        echo "Warning: Failed to set backup permissions"
    }
    
    return 0
}

# Function to backup system state
backup_system_state() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$BACKUP_DIR/system_state_$timestamp"
    
    # Create backup directory if it doesn't exist
    create_backup_dir || return 1
    
    # Create temporary directory for system state
    local temp_dir=$(mktemp -d) || {
        echo "Error: Failed to create temporary directory"
        return 1
    }
    
    # Backup system information
    {
        echo "=== System Information ==="
        uname -a
        echo -e "\n=== CPU Information ==="
        lscpu
        echo -e "\n=== Memory Information ==="
        free -h
        echo -e "\n=== Disk Information ==="
        df -h
        echo -e "\n=== Network Information ==="
        ip addr
        echo -e "\n=== Service Status ==="
        systemctl list-units --type=service --state=running
    } > "$temp_dir/system_info.txt"
    
    # Create archive
    if [ "$COMPRESS_BACKUPS" = true ]; then
        tar -czf "$backup_path.tar.gz" -C "$temp_dir" . || {
            echo "Error: Failed to create system state backup archive"
            rm -rf "$temp_dir"
            return 1
        }
    else
        tar -cf "$backup_path.tar" -C "$temp_dir" . || {
            echo "Error: Failed to create system state backup archive"
            rm -rf "$temp_dir"
            return 1
        }
    fi
    
    # Clean up temporary directory
    rm -rf "$temp_dir"
    
    # Set proper permissions
    chmod 600 "$backup_path"* || {
        echo "Warning: Failed to set backup permissions"
    }
    
    return 0
}

# Function to restore from backup
restore_from_backup() {
    local backup_type="$1"  # pkg_list, config, or system_state
    local backup_file="$2"
    
    if [ ! -f "$backup_file" ]; then
        echo "Error: Backup file not found: $backup_file"
        return 1
    }
    
    case "$backup_type" in
        "pkg_list")
            # Restore package list
            if [[ "$backup_file" == *.gz ]]; then
                gunzip -c "$backup_file" | dpkg --set-selections || {
                    echo "Error: Failed to restore package list"
                    return 1
                }
            else
                dpkg --set-selections < "$backup_file" || {
                    echo "Error: Failed to restore package list"
                    return 1
                }
            fi
            ;;
            
        "config")
            # Restore configuration files
            local temp_dir=$(mktemp -d) || {
                echo "Error: Failed to create temporary directory"
                return 1
            }
            
            if [[ "$backup_file" == *.gz ]]; then
                tar -xzf "$backup_file" -C "$temp_dir" || {
                    echo "Error: Failed to extract config backup"
                    rm -rf "$temp_dir"
                    return 1
                }
            else
                tar -xf "$backup_file" -C "$temp_dir" || {
                    echo "Error: Failed to extract config backup"
                    rm -rf "$temp_dir"
                    return 1
                }
            fi
            
            # Restore files
            cp -r "$temp_dir"/* / || {
                echo "Error: Failed to restore configuration files"
                rm -rf "$temp_dir"
                return 1
            }
            
            rm -rf "$temp_dir"
            ;;
            
        *)
            echo "Error: Unknown backup type: $backup_type"
            return 1
            ;;
    esac
    
    return 0
}

# Function to list available backups
list_backups() {
    local backup_type="$1"
    
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "No backups found"
        return 1
    fi
    
    case "$backup_type" in
        "pkg_list")
            ls -1 "$BACKUP_DIR"/pkg_list_* 2>/dev/null
            ;;
        "config")
            ls -1 "$BACKUP_DIR"/config_* 2>/dev/null
            ;;
        "system_state")
            ls -1 "$BACKUP_DIR"/system_state_* 2>/dev/null
            ;;
        *)
            ls -1 "$BACKUP_DIR"/* 2>/dev/null
            ;;
    esac
}

# Export functions
export -f create_backup_dir
export -f rotate_backups
export -f backup_package_list
export -f backup_config_files
export -f backup_system_state
export -f restore_from_backup
export -f list_backups 