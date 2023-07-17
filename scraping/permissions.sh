#!/usr/bin/env bash

# This script must be run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Define directories
log_dir="/var/log/scrapy"
data_dir="/opt/scraped_data"

# Create the directories if they do not exist
mkdir -p "$log_dir"
mkdir -p "$data_dir"

# Change ownership to the current user and group
chown -R "$SUDO_USER":"$SUDO_USER" "$log_dir"
chown -R "$SUDO_USER":"$SUDO_USER" "$data_dir"

# Change permissions
chmod 775 "$log_dir"
chmod 775 "$data_dir"

# Print out the results
echo "Permissions for $log_dir and $data_dir have been updated."
