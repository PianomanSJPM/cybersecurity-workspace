#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import threading
import time
from datetime import datetime
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Ether, DNS
import pyshark
import queue
import json
import os
from collections import defaultdict
import socket
import re
from mac_vendor_lookup import MacLookup
import hashlib
import csv
import subprocess

# Enhanced service definitions focused on user activities
SERVICES = {
    # Video Streaming
    'streaming': {
        'name': 'Video Streaming',
        'ports': {
            'tcp': [80, 443, 1935],
            'udp': []
        },
        'domains': [
            'netflix.com', 'youtube.com', 'hulu.com', 'disneyplus.com', 'primevideo.com',
            'twitch.tv', 'vimeo.com', 'dailymotion.com', 'hbomax.com', 'peacocktv.com',
            'hbo.com', 'paramountplus.com', 'showtime.com', 'starz.com', 'apple.com/tv',
            'youtube.com/watch', 'youtube.com/shorts', 'youtube.com/live'
        ]
    },
    # Gaming
    'gaming': {
        'name': 'Gaming',
        'ports': {
            'tcp': [3074, 3075, 3478, 3479, 3480, 7777, 7778, 7779, 3659, 3074, 3075, 25565],
            'udp': [3074, 3075, 3478, 3479, 3480, 7777, 7778, 7779, 3659, 3074, 3075]
        },
        'domains': [
            'playstation.net', 'xboxlive.com', 'steam-chat.com', 'ea.com', 'battle.net',
            'playstation.com', 'xbox.com', 'steam.com', 'epicgames.com', 'minecraft.net',
            'roblox.com', 'fortnite.com', 'leagueoflegends.com', 'valorant.com',
            'overwatch.com', 'worldofwarcraft.com', 'diablo.com', 'hearthstone.com'
        ]
    },
    # Social Media
    'social': {
        'name': 'Social Media',
        'ports': {
            'tcp': [80, 443],
            'udp': []
        },
        'domains': [
            'facebook.com', 'twitter.com', 'instagram.com', 'tiktok.com', 'linkedin.com',
            'pinterest.com', 'reddit.com', 'snapchat.com', 'whatsapp.com', 'telegram.org',
            'messenger.com', 'discord.com', 'slack.com', 'teams.microsoft.com',
            'zoom.us', 'meet.google.com', 'webex.com', 'skype.com'
        ]
    },
    # Web Browsing
    'web': {
        'name': 'Web Browsing',
        'ports': {
            'tcp': [80, 443, 8080],
            'udp': []
        },
        'domains': [
            'www.', '.com', '.org', '.net', '.io', 'google.com', 'bing.com',
            'yahoo.com', 'duckduckgo.com', 'brave.com', 'mozilla.org', 'chrome.google.com'
        ]
    },
    # File Sharing
    'filesharing': {
        'name': 'File Sharing',
        'ports': {
            'tcp': [80, 443],
            'udp': []
        },
        'domains': [
            'dropbox.com', 'drive.google.com', 'onedrive.live.com', 'box.com',
            'mega.nz', 'pcloud.com', 'sync.com', 'icloud.com', 'mediafire.com',
            'wetransfer.com', 'sendspace.com', 'rapidshare.com', '4shared.com'
        ]
    },
    # System Updates
    'updates': {
        'name': 'System Updates',
        'ports': {
            'tcp': [80, 443],
            'udp': []
        },
        'domains': [
            'update.', 'download.', 'software-update.', 'windowsupdate.com',
            'apple.com', 'microsoft.com', 'ubuntu.com', 'debian.org', 'redhat.com',
            'nvidia.com', 'amd.com', 'intel.com', 'adobe.com'
        ]
    },
    'youtube': {
        'name': 'YouTube',
        'domains': ['youtube.com', 'googlevideo.com', 'youtube-nocookie.com', 'youtube.googleapis.com'],
        'ports': {
            'tcp': [80, 443],
            'udp': [80, 443]
        }
    },
    'netflix': {
        'name': 'Netflix',
        'domains': ['netflix.com', 'nflxvideo.net', 'nflximg.net', 'nflxext.com'],
        'ports': {
            'tcp': [80, 443],
            'udp': [80, 443]
        }
    },
    'spotify': {
        'name': 'Spotify',
        'domains': ['spotify.com', 'spotifycdn.net', 'spotifycdn.com'],
        'ports': {
            'tcp': [80, 443],
            'udp': [80, 443]
        }
    },
    'amazon': {
        'name': 'Amazon',
        'domains': ['amazon.com', 'amazonaws.com', 'amazonvideo.com'],
        'ports': {
            'tcp': [80, 443],
            'udp': [80, 443]
        }
    }
}

# Common port to service mapping
COMMON_PORT_SERVICES = {
    53: 'DNS',
    80: 'HTTP',
    443: 'HTTPS',
    25: 'SMTP',
    110: 'POP3',
    143: 'IMAP',
    993: 'IMAPS',
    995: 'POP3S',
    22: 'SSH',
    21: 'FTP',
    3074: 'Xbox Live',
    3478: 'PlayStation Network',
    1935: 'Twitch/RTMP',
    8080: 'HTTP-Alt',
    8888: 'Proxy',
    123: 'NTP',
    445: 'SMB',
    3389: 'RDP',
    5353: 'mDNS',
    1900: 'SSDP',
    6667: 'IRC',
    6668: 'IRC',
    25565: 'Minecraft',
    27015: 'Steam',
    27016: 'Steam',
    27017: 'Steam',
    27018: 'Steam',
    27019: 'Steam',
    27020: 'Steam',
    7777: 'Unreal Engine',
    7778: 'Unreal Engine',
    7779: 'Unreal Engine',
    3659: 'Battle.net',
    3478: 'PlayStation Network',
    3479: 'PlayStation Network',
    3480: 'PlayStation Network'
}

class ServiceDetector:
    @staticmethod
    def extract_ports(info):
        try:
            if 'Port:' in info:
                ports_str = info.split('Port:')[1].strip()
                if '->' in ports_str:
                    src_port, dst_port = ports_str.split('->')
                    return int(src_port.strip()), int(dst_port.strip())
        except:
            pass
        return None, None

    @staticmethod
    def detect_service(packet_info):
        protocol = packet_info['protocol'].lower()
        info = packet_info['info']
        destination = packet_info.get('destination', '')
        src_port, dst_port = ServiceDetector.extract_ports(info)

        # Try to resolve destination IP to hostname
        hostname = None
        if destination:
            try:
                hostname = socket.gethostbyaddr(destination)[0]
            except Exception:
                hostname = None

        # First check for specific services by domain or hostname
        for service_id, service in SERVICES.items():
            # Check domains first (more reliable)
            if hostname and any(domain in hostname.lower() for domain in service['domains']):
                return f"{service['name']} ({hostname})"
            if destination and any(domain in destination.lower() for domain in service['domains']):
                return f"{service['name']} ({destination})"
            # Then check ports
            if protocol in service['ports']:
                if any(port in service['ports'][protocol] for port in [src_port, dst_port]):
                    return f"{service['name']} (Port {dst_port or src_port})"

        # For unknown services, show destination IP or hostname
        if hostname:
            return f"Network Activity ({hostname})"
        elif destination:
            return f"Network Activity ({destination})"
        else:
            return "Network Activity"

class DeviceManager:
    def __init__(self):
        self.devices = {}  # MAC -> {nickname, type, last_seen, connections}
        self.mac_to_ip = {}  # MAC -> IP
        self.ip_to_mac = {}  # IP -> MAC
        self.mac_lookup = MacLookup()
        self.load_devices()
    
    def load_devices(self):
        try:
            if os.path.exists('devices.json'):
                with open('devices.json', 'r') as f:
                    saved_devices = json.load(f)
                    self.devices = saved_devices
        except Exception as e:
            print(f"Error loading devices: {e}")
    
    def save_devices(self):
        try:
            with open('devices.json', 'w') as f:
                json.dump(self.devices, f)
        except Exception as e:
            print(f"Error saving devices: {e}")
    
    def get_manufacturer(self, mac):
        """Get manufacturer name from MAC address"""
        try:
            # Clean MAC address format
            mac = mac.replace(':', '').replace('-', '').upper()[:6]
            return self.mac_lookup.lookup(mac)
        except:
            return "Unknown Manufacturer"
    
    def get_oui_vendor(self, mac_address):
        """Return the OUI vendor for a MAC address, or lookup based on OUI prefix if not found."""
        try:
            return MacLookup().lookup(mac_address)
        except Exception:
            # Fallback to OUI prefix lookup
            oui_prefix = mac_address[:8].upper()
            oui_vendors = {
                '80:DA:13': 'Hon Hai Precision Ind. Co., Ltd.',
                '1C:57:DC': 'Apple Inc.',
                '9E:74:BA': 'Apple Inc.',
                '6C:4A:85': 'Apple Inc.',
                '86:D4:76': 'Apple Inc.',
                'E2:E0:5D': 'Apple Inc.',
                '7E:67:F9': 'Apple Inc.',
                '48:5F:2D': 'Apple Inc.',
                '76:D1:B0': 'Apple Inc.',
                'BE:08:92': 'Apple Inc.',
                'FF:FF:FF': 'Broadcast Address',
                '01:00:5E': 'Multicast Address'
            }
            return oui_vendors.get(oui_prefix, 'Unknown Manufacturer')
    
    def detect_device_type(self, mac_address, manufacturer):
        """Detect device type based on MAC address and manufacturer, with OUI fallback."""
        mac = mac_address.lower()
        manufacturer = manufacturer.lower()
        
        # Handle special addresses
        if mac.startswith('ff:ff:ff'):
            return 'Broadcast Address'
        if mac.startswith('01:00:5e'):
            return 'Multicast Address'
        
        # Get OUI vendor if manufacturer is unknown
        if manufacturer == 'unknown' or manufacturer == '':
            manufacturer = self.get_oui_vendor(mac_address).lower()
        
        # Apple devices
        if 'apple' in manufacturer:
            # Try to detect specific Apple device types based on OUI prefix
            oui_prefix = mac[:8].upper()
            apple_devices = {
                '1C:57:DC': 'iPhone',
                '9E:74:BA': 'iPad',
                '6C:4A:85': 'MacBook',
                '86:D4:76': 'Apple TV',
                'E2:E0:5D': 'HomePod',
                '7E:67:F9': 'Apple Watch',
                '48:5F:2D': 'AirPods',
                '76:D1:B0': 'Apple Device',
                'BE:08:92': 'Apple Device'
            }
            return apple_devices.get(oui_prefix, 'Apple Device')
        
        # Foxconn devices (manufactures for many companies)
        if 'hon hai' in manufacturer or 'foxconn' in manufacturer:
            return 'Network Device'
        
        # Default to manufacturer name if no specific type is detected
        return f"{manufacturer.title()} Device"
    
    def update_device(self, mac, ip, info=None):
        """Update device information"""
        try:
            if mac not in self.devices:
                self.devices[mac] = {
                    'mac': mac,
                    'ip': ip,
                    'first_seen': datetime.now(),
                    'last_seen': datetime.now(),
                    'type': 'Unknown',
                    'manufacturer': 'Unknown',
                    'services': set(),
                    'info': {}  # Always initialize 'info' key
                }
            else:
                device = self.devices[mac]
                device['last_seen'] = datetime.now()
                if ip and ip != device.get('ip'):
                    device['ip'] = ip
                # Ensure 'info' key exists
                if 'info' not in device:
                    device['info'] = {}
            
            if info:
                self.devices[mac]['info'].update(info)
            
            # Update device type and manufacturer
            try:
                vendor = self.mac_lookup.lookup(mac)
                if vendor:
                    self.devices[mac]['manufacturer'] = vendor
                    # Try to determine device type based on manufacturer
                    if 'apple' in vendor.lower():
                        self.devices[mac]['type'] = 'Apple Device'
                    elif 'eero' in vendor.lower():
                        self.devices[mac]['type'] = 'Eero Device'
                    else:
                        self.devices[mac]['type'] = 'Network Device'
                else:
                    self.devices[mac]['manufacturer'] = 'Unknown'
                    self.devices[mac]['type'] = 'Unknown'
            except Exception as e:
                print(f"Error looking up MAC vendor: {str(e)}")
                self.devices[mac]['manufacturer'] = 'Unknown'
                self.devices[mac]['type'] = 'Unknown'
            
            print(f"\nUpdating device:")
            print(f"MAC: {mac}")
            print(f"IP: {ip}")
            print(f"Updated device info:")
            print(f"Type: {self.devices[mac]['type']}")
            print(f"Manufacturer: {self.devices[mac]['manufacturer']}")
            
        except Exception as e:
            print(f"Error updating device: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def set_nickname(self, mac, nickname):
        if mac in self.devices:
            self.devices[mac]['nickname'] = nickname
            self.save_devices()
    
    def set_type(self, mac, device_type):
        if mac in self.devices:
            self.devices[mac]['type'] = device_type
            self.save_devices()
    
    def get_most_used_service(self, mac):
        if mac in self.devices:
            services = self.devices[mac]['services']
            if services:
                return max(services.items(), key=lambda x: x[1])[0]
        return "Unknown"

class NetworkMonitor:
    def __init__(self):
        """Initialize the network monitor"""
        self.root = tk.Tk()
        self.root.title("Network Monitor")
        self.root.geometry("1200x800")
        
        # Initialize device tracking
        self.device_manager = DeviceManager()
        self.known_devices = self.load_known_devices()
        self.unknown_devices = set()
        self.device_last_seen = {}
        self.device_history = {}  # Track connection history
        self.device_categories = self.load_device_categories()
        self.device_notes = self.load_device_notes()
        
        # Initialize network data
        self.network_data = []
        self.mac_lookup = MacLookup()
        
        # Create UI
        self.create_ui()
        
        # Start packet capture in a separate thread
        self.selected_interface = self.prompt_for_interface()
        self.data_queue = queue.Queue()
        self.last_history_count = 0
        self.capturing = False
        self.capture_thread = None
        
        # Start periodic updates
        self.root.after(1000, self.update_ui)
        self.root.after(1000, self.periodic_update_history_view)
    
    def load_known_devices(self):
        """Load known devices from file"""
        try:
            with open('known_devices.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_known_devices(self):
        """Save known devices to file"""
        with open('known_devices.json', 'w') as f:
            json.dump(self.known_devices, f, indent=4)

    def add_known_device(self, mac, name):
        """Add a device to known devices"""
        self.known_devices[mac] = name
        self.save_known_devices()
        self.update_device_list()

    def check_unknown_device(self, mac, ip, device_type, manufacturer):
        """Check if a device is unknown and alert if it is"""
        if mac not in self.known_devices and mac not in self.unknown_devices:
            self.unknown_devices.add(mac)
            # Add to device history
            if mac not in self.device_history:
                self.device_history[mac] = []
            self.device_history[mac].append({
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'event': 'First Seen',
                'details': f"IP: {ip}, Type: {device_type}, Manufacturer: {manufacturer}"
            })
            # Automatically name the device based on its type
            if device_type == 'Apple Device':
                self.add_known_device(mac, 'Apple Device')
            elif device_type == 'Eero Device':
                self.add_known_device(mac, 'Eero Device')
            else:
                self.add_known_device(mac, device_type)
            # Update device list
            self.update_device_list()

    def load_device_categories(self):
        """Load device categories from file"""
        try:
            with open('device_categories.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_device_categories(self):
        """Save device categories to file"""
        with open('device_categories.json', 'w') as f:
            json.dump(self.device_categories, f, indent=4)

    def load_device_notes(self):
        """Load device notes from file"""
        try:
            with open('device_notes.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_device_notes(self):
        """Save device notes to file"""
        with open('device_notes.json', 'w') as f:
            json.dump(self.device_notes, f, indent=4)

    def create_ui(self):
        """Create the main UI components"""
        print("[DEBUG] Creating UI components...")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.devices_tab = ttk.Frame(self.notebook)
        self.activity_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.devices_tab, text='Devices')
        self.notebook.add(self.activity_tab, text='Activity')
        self.notebook.add(self.history_tab, text='History')
        
        # Create device list
        print("[DEBUG] Creating device tree...")
        self.device_tree = ttk.Treeview(self.devices_tab, columns=(
            'name', 'category', 'mac', 'ip', 'type', 'manufacturer', 'oui_vendor', 'last_seen', 'status'
        ), show='headings')
        
        # Set column headings
        self.device_tree.heading('name', text='Device Name')
        self.device_tree.heading('category', text='Category')
        self.device_tree.heading('mac', text='MAC Address')
        self.device_tree.heading('ip', text='IP Address')
        self.device_tree.heading('type', text='Device Type')
        self.device_tree.heading('manufacturer', text='Manufacturer')
        self.device_tree.heading('oui_vendor', text='OUI Vendor')
        self.device_tree.heading('last_seen', text='Last Seen')
        self.device_tree.heading('status', text='Status')
        
        # Set column widths
        self.device_tree.column('name', width=100)
        self.device_tree.column('category', width=80)
        self.device_tree.column('mac', width=150)
        self.device_tree.column('ip', width=120)
        self.device_tree.column('type', width=100)
        self.device_tree.column('manufacturer', width=150)
        self.device_tree.column('oui_vendor', width=150)
        self.device_tree.column('last_seen', width=150)
        self.device_tree.column('status', width=80)
        
        # Add scrollbar
        device_scrollbar = ttk.Scrollbar(self.devices_tab, orient='vertical', command=self.device_tree.yview)
        self.device_tree.configure(yscrollcommand=device_scrollbar.set)
        
        # Pack device tree
        self.device_tree.pack(side='left', fill='both', expand=True)
        device_scrollbar.pack(side='right', fill='y')
        
        # Add right-click menu for devices
        self.device_menu = tk.Menu(self.root, tearoff=0)
        self.device_menu.add_command(label="Set Device Name", command=self.set_device_name)
        self.device_menu.add_command(label="Set Category", command=self.set_device_category)
        self.device_menu.add_command(label="Add Note", command=self.add_device_note)
        self.device_menu.add_command(label="Show Device Details", command=self.show_device_details)
        self.device_menu.add_command(label="Show Connection History", command=self.show_connection_history)
        self.device_tree.bind("<Button-3>", self.create_device_context_menu)
        self.device_tree.bind("<Double-1>", lambda e: self.show_device_details())
        
        # Create history view
        self.history_tree = ttk.Treeview(self.history_tab, columns=(
            'device', 'category', 'event', 'time', 'details'
        ), show='headings')
        
        # Set history column headings
        self.history_tree.heading('device', text='Device')
        self.history_tree.heading('category', text='Category')
        self.history_tree.heading('event', text='Event')
        self.history_tree.heading('time', text='Time')
        self.history_tree.heading('details', text='Details')
        
        # Set history column widths
        self.history_tree.column('device', width=150)
        self.history_tree.column('category', width=100)
        self.history_tree.column('event', width=100)
        self.history_tree.column('time', width=150)
        self.history_tree.column('details', width=400)
        
        # Add history scrollbar
        history_scrollbar = ttk.Scrollbar(self.history_tab, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        # Pack history tree
        self.history_tree.pack(side='left', fill='both', expand=True)
        history_scrollbar.pack(side='right', fill='y')
        
        # Add Export Devices button
        export_btn = ttk.Button(self.devices_tab, text="Export Devices", command=self.export_devices_to_csv)
        export_btn.pack(pady=5, anchor='ne')

        # Add Export Activity button
        export_activity_btn = ttk.Button(self.activity_tab, text="Export Activity", command=self.export_activity)
        export_activity_btn.pack(pady=5, anchor='ne')

        # Add Export History button
        export_history_btn = ttk.Button(self.history_tab, text="Export History", command=self.export_history)
        export_history_btn.pack(pady=5, anchor='ne')

        # Add Save Data button at the bottom
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        save_btn = ttk.Button(button_frame, text="Save Data", command=self.save_data)
        save_btn.pack(side='right', padx=5)

        # Add Start and Stop buttons
        start_btn = ttk.Button(button_frame, text="Start", command=self.start_capture)
        start_btn.pack(side='left', padx=5)
        stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_capture)
        stop_btn.pack(side='left', padx=5)

        # Create activity view
        self.activity_tree = ttk.Treeview(self.activity_tab, columns=(
            'time', 'protocol', 'source', 'destination', 'hostname', 'length', 'info'
        ), show='headings')
        
        # Set activity column headings
        self.activity_tree.heading('time', text='Time')
        self.activity_tree.heading('protocol', text='Protocol')
        self.activity_tree.heading('source', text='Source')
        self.activity_tree.heading('destination', text='Destination')
        self.activity_tree.heading('hostname', text='Hostname')
        self.activity_tree.heading('length', text='Length')
        self.activity_tree.heading('info', text='Info')
        
        # Set activity column widths
        self.activity_tree.column('time', width=150)
        self.activity_tree.column('protocol', width=80)
        self.activity_tree.column('source', width=150)
        self.activity_tree.column('destination', width=150)
        self.activity_tree.column('hostname', width=200)
        self.activity_tree.column('length', width=80)
        self.activity_tree.column('info', width=300)
        
        # Add activity scrollbar
        activity_scrollbar = ttk.Scrollbar(self.activity_tab, orient='vertical', command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=activity_scrollbar.set)
        
        # Pack activity tree
        self.activity_tree.pack(side='left', fill='both', expand=True)
        activity_scrollbar.pack(side='right', fill='y')

        # Add export limit options
        export_limit_frame = ttk.Frame(self.activity_tab)
        export_limit_frame.pack(pady=5, anchor='ne')
        ttk.Label(export_limit_frame, text="Export Limit:").pack(side='left', padx=5)
        self.export_limit = ttk.Combobox(export_limit_frame, values=['All', 'Last 50 Events', 'Last 20 Events'], state='readonly')
        self.export_limit.current(0)
        self.export_limit.pack(side='left', padx=5)

        # Add export limit options for history
        export_limit_frame_history = ttk.Frame(self.history_tab)
        export_limit_frame_history.pack(pady=5, anchor='ne')
        ttk.Label(export_limit_frame_history, text="Export Limit:").pack(side='left', padx=5)
        self.export_limit_history = ttk.Combobox(export_limit_frame_history, values=['All', 'Last 50 Events', 'Last 20 Events'], state='readonly')
        self.export_limit_history.current(0)
        self.export_limit_history.pack(side='left', padx=5)

    def set_device_category(self):
        """Set a category for the selected device"""
        selected = self.device_tree.selection()
        if not selected:
            return
            
        item = self.device_tree.item(selected[0])
        mac = item['values'][2]  # MAC address is in the third column
        
        # Create a dialog to get the category
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Device Category")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Select category:").pack(pady=5)
        category_var = tk.StringVar()
        categories = ['Family', 'Guest', 'IoT', 'Other']
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=categories)
        category_combo.pack(pady=5)
        
        def save_category():
            category = category_var.get().strip()
            if category:
                self.device_categories[mac] = category
                self.save_device_categories()
                self.update_device_list()
                dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_category).pack(pady=5)
        category_combo.focus()

    def add_device_note(self):
        """Add a note to the selected device"""
        selected = self.device_tree.selection()
        if not selected:
            return
            
        item = self.device_tree.item(selected[0])
        mac = item['values'][2]  # MAC address is in the third column
        
        # Create a dialog to get the note
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Device Note")
        dialog.geometry("400x200")
        
        ttk.Label(dialog, text="Enter note:").pack(pady=5)
        note_text = tk.Text(dialog, height=5, width=40)
        note_text.pack(pady=5)
        
        def save_note():
            note = note_text.get("1.0", tk.END).strip()
            if note:
                if mac not in self.device_notes:
                    self.device_notes[mac] = []
                self.device_notes[mac].append({
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'note': note
                })
                self.save_device_notes()
                dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_note).pack(pady=5)
        note_text.focus()

    def show_connection_history(self):
        """Show connection history for the selected device"""
        selected = self.device_tree.selection()
        if not selected:
            return
            
        item = self.device_tree.item(selected[0])
        mac = item['values'][2]  # MAC address is in the third column
        
        # Create a dialog to show history
        dialog = tk.Toplevel(self.root)
        dialog.title("Connection History")
        dialog.geometry("600x400")
        
        # Create treeview for history
        history_tree = ttk.Treeview(dialog, columns=('time', 'event', 'details'), show='headings')
        history_tree.heading('time', text='Time')
        history_tree.heading('event', text='Event')
        history_tree.heading('details', text='Details')
        
        history_tree.column('time', width=150)
        history_tree.column('event', width=100)
        history_tree.column('details', width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=history_tree.yview)
        history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview
        history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add history entries
        if mac in self.device_history:
            for entry in self.device_history[mac]:
                history_tree.insert('', 'end', values=(
                    entry['time'],
                    entry['event'],
                    entry['details']
                ))

    def update_device_list(self):
        """Update the device list with current information"""
        # Clear existing items
        for item in self.device_tree.get_children():
            self.device_tree.delete(item)
            
        # Add devices
        for mac, device in self.device_manager.devices.items():
            # Get current activity
            current_activity = ""
            if device.get('last_service'):
                current_activity = f"Accessing {device['last_service']}"
            elif device.get('status') == 'active':
                current_activity = 'Active'
            else:
                current_activity = 'Inactive'
            
            values = (
                self.known_devices.get(mac, "Unknown"),  # Device name
                self.device_categories.get(mac, "Uncategorized"),  # Category
                mac,
                device.get('ip', 'N/A'),
                device.get('type', 'Unknown'),
                device.get('manufacturer', 'Unknown'),
                device.get('oui_vendor', 'Unknown'),
                device.get('last_seen', 'N/A'),
                current_activity
            )
            self.device_tree.insert('', 'end', values=values)

    def update_device_info(self, mac, ip, vendor):
        """Update device information and track history"""
        if mac not in self.device_manager.devices:
            self.device_manager.devices[mac] = {}
        
        # Update basic info
        self.device_manager.devices[mac].update({
            'ip': ip,
            'manufacturer': vendor,
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active'
        })
        
        # Track connection history
        if mac not in self.device_history:
            self.device_history[mac] = []
        
        # Add to history if it's a new connection or IP change
        if not self.device_history[mac] or self.device_history[mac][-1]['event'] != 'Connected' or self.device_history[mac][-1]['details'] != f"IP: {ip}, Manufacturer: {vendor}":
            self.device_history[mac].append({
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'event': 'Connected',
                'details': f"IP: {ip}, Manufacturer: {vendor}"
            })

    def update_ui(self):
        """Update the UI with new packet data"""
        try:
            while True:
                try:
                    # Get all available items from queue
                    while True:
                        packet_data = self.data_queue.get_nowait()
                        if packet_data:
                            # Insert at the top of the table
                            self.activity_tree.insert('', 0, values=(
                                packet_data['time'],
                                packet_data['protocol'],
                                packet_data['source'],
                                packet_data['destination'],
                                packet_data.get('hostname', ''),
                                packet_data['length'],
                                packet_data['info']
                            ))
                            # Keep only last 1000 entries
                            if len(self.activity_tree.get_children()) > 1000:
                                self.activity_tree.delete(self.activity_tree.get_children()[-1])
                except queue.Empty:
                    break
                
                # Update device list and filter periodically
                current_time = time.time()
                if current_time - self.last_device_update >= 1.0:  # Update every second
                    self.update_device_list()
                    self.update_device_filter()
                    self.last_device_update = current_time
                
        except Exception as e:
            print(f"Error in update_ui: {e}")
        finally:
            # Schedule next update
            self.root.after(100, self.update_ui)
    
    def save_data(self):
        if not self.network_data:
            messagebox.showwarning("No Data", "No network data to save.")
            return
        
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(self.network_data)
        filename = f"network_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Data saved to {filename}")
        
        # Save device information
        self.device_manager.save_devices()
    
    def get_protocol_name(self, packet):
        """Get the protocol name from a packet"""
        if TCP in packet:
            return 'tcp'
        elif UDP in packet:
            return 'udp'
        elif ICMP in packet:
            return 'icmp'
        else:
            return 'other'

    def get_packet_info(self, packet):
        """Get additional packet information"""
        info = []
        try:
            if TCP in packet:
                info.append(f"Port: {packet[TCP].sport} -> {packet[TCP].dport}")
            elif UDP in packet:
                info.append(f"Port: {packet[UDP].sport} -> {packet[UDP].dport}")
            elif ARP in packet:
                info.append(f"ARP: {packet[ARP].op}")
            elif ICMP in packet:
                info.append(f"ICMP Type: {packet[ICMP].type}")
            elif DNS in packet:
                info.append(f"DNS: {packet[DNS].qd.qname.decode() if packet[DNS].qd else 'Unknown'}")
        except Exception as e:
            info.append(f"Error getting packet info: {str(e)}")
        return " ".join(info)
    
    def create_device_context_menu(self, event):
        """Create context menu for device tree"""
        selected = self.device_tree.selection()
        if not selected:
            return
            
        item = selected[0]
        mac = self.device_tree.item(item)['values'][2]  # MAC is in third column
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Set Device Name", command=lambda: self.set_device_name(mac))
        menu.add_command(label="Set Category", command=lambda: self.set_device_category(mac))
        menu.add_command(label="Add Note", command=lambda: self.add_device_note(mac))
        menu.add_command(label="Show Device Details", command=lambda: self.show_device_details(mac))
        menu.add_command(label="Show Connection History", command=lambda: self.show_connection_history(mac))
        menu.add_separator()
        menu.add_command(label="Copy MAC Address", command=lambda: self.copy_to_clipboard(mac))
        menu.add_command(label="Copy IP Address", command=lambda: self.copy_to_clipboard(self.device_manager.mac_to_ip.get(mac, "")))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def set_device_name(self, mac):
        """Set a name for the selected device"""
        selected = self.device_tree.selection()
        if not selected:
            return
            
        item = self.device_tree.item(selected[0])
        mac = item['values'][2]  # MAC address is in the third column
        
        # Create a dialog to get the device name
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Device Name")
        dialog.geometry("300x100")
        
        ttk.Label(dialog, text="Enter device name:").pack(pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(dialog, textvariable=name_var)
        name_entry.pack(pady=5)
        
        def save_name():
            name = name_var.get().strip()
            if name:
                self.add_known_device(mac, name)
                dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_name).pack(pady=5)
        name_entry.focus()

    def show_device_details(self, mac_address):
        """Show detailed information about a device"""
        if mac_address in self.device_manager.devices:
            device = self.device_manager.devices[mac_address]
            
            # Create a new window for device details
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Device Details - {device.get('nickname', 'Unknown Device')}")
            details_window.geometry("400x300")
            
            # Create main frame with padding
            main_frame = ttk.Frame(details_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Device information
            info_text = f"""
Device Name: {device.get('nickname', 'Not Set')}
MAC Address: {mac_address}
IP Address: {self.device_manager.mac_to_ip.get(mac_address, 'Unknown')}
Device Type: {device.get('type', 'Unknown')}
Manufacturer: {device.get('manufacturer', 'Unknown')}
First Seen: {device.get('first_seen', 'Unknown')}
Last Seen: {device.get('last_seen', 'Unknown')}
Status: {'Online' if device.get('online', False) else 'Offline'}
            """
            
            # Create text widget with scrollbar
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, height=10)
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insert device information
            text_widget.insert(tk.END, info_text)
            text_widget.configure(state='disabled')  # Make text read-only
            
            # Add close button
            ttk.Button(main_frame, text="Close", command=details_window.destroy).pack(pady=10)

    def show_activity_menu(self, event):
        """Show context menu for activity items"""
        item = self.activity_tree.identify_row(event.y)
        if item:
            self.activity_tree.selection_set(item)
            self.activity_menu.post(event.x_root, event.y_root)

    def show_connection_details(self):
        """Show detailed information about a connection"""
        item = self.activity_tree.selection()[0]
        values = self.activity_tree.item(item)['values']
        
        details = [
            ("Timestamp", values[0]),
            ("Protocol", values[1]),
            ("Source", values[2]),
            ("Destination", values[3]),
            ("Length", values[4]),
            ("Info", values[5])
        ]
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Connection Details")
        details_window.geometry("400x300")
        
        # Add details
        for label, value in details:
            frame = ttk.Frame(details_window)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=f"{label}:").pack(side=tk.LEFT)
            ttk.Label(frame, text=value).pack(side=tk.LEFT, padx=5)

    def export_devices_to_csv(self):
        """Export the device list to a CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save Devices As...'
        )
        if not file_path:
            return
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow([
                'MAC Address', 'IP Address', 'Nickname', 'Type', 'Manufacturer', 'OUI Vendor', 'Last Seen', 'Status', 'OUI Prefix'
            ])
            for mac, device in self.device_manager.devices.items():
                ip = self.device_manager.mac_to_ip.get(mac, '')
                nickname = device.get('nickname', mac)
                device_type = device.get('type', 'Unknown')
                manufacturer = device.get('manufacturer', 'Unknown')
                oui_vendor = device.get('oui_vendor', 'Unknown')
                last_seen = device.get('last_seen', 'Never')
                status = 'Online' if device.get('online', False) else 'Offline'
                oui_prefix = mac[:8].upper()
                writer.writerow([
                    mac, ip, nickname, device_type, manufacturer, oui_vendor, last_seen, status, oui_prefix
                ])

    def export_activity(self):
        """Export the activity list to a document."""
        if not self.network_data:
            messagebox.showwarning("No Data", "No activity data to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[
                ('Text files', '*.txt'),
                ('CSV files', '*.csv'),
                ('All files', '*.*')
            ],
            title='Save Activity As...'
        )
        
        if not file_path:
            return
            
        try:
            # Get the export limit
            export_limit = self.export_limit.get()
            
            # Get filtered activities
            filtered_activities = self.network_data.copy()
            
            # Apply export limit
            if export_limit == 'Last 50 Events':
                filtered_activities = filtered_activities[-50:]
            elif export_limit == 'Last 20 Events':
                filtered_activities = filtered_activities[-20:]
            
            # Write to file
            with open(file_path, 'w', newline='') as f:
                if file_path.endswith('.csv'):
                    # Write as CSV
                    writer = csv.writer(f)
                    writer.writerow(['Time', 'Protocol', 'Source', 'Destination', 'Hostname', 'Length', 'Info'])
                    for activity in filtered_activities:
                        writer.writerow([
                            activity['time'],
                            activity['protocol'],
                            activity['source'],
                            activity['destination'],
                            activity.get('hostname', ''),
                            activity['length'],
                            activity['info']
                        ])
                else:
                    # Write as formatted text
                    f.write("Network Activity Report\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(f"Export Limit: {export_limit}\n")
                    f.write(f"Total Events: {len(filtered_activities)}\n")
                    f.write("\n")
                    
                    for activity in filtered_activities:
                        f.write(f"Time: {activity['time']}\n")
                        f.write(f"Protocol: {activity['protocol']}\n")
                        f.write(f"Source: {activity['source']}\n")
                        f.write(f"Destination: {activity['destination']}\n")
                        if activity.get('hostname'):
                            f.write(f"Hostname: {activity['hostname']}\n")
                        f.write(f"Length: {activity['length']}\n")
                        f.write(f"Info: {activity['info']}\n")
                        f.write("-" * 80 + "\n\n")
            
            messagebox.showinfo("Success", f"Activity data exported successfully to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting activity data:\n{str(e)}")

    def get_available_interfaces(self):
        """Get a list of available network interfaces"""
        try:
            result = subprocess.run(['ifconfig', '-l'], capture_output=True, text=True)
            interfaces = result.stdout.strip().split()
            return interfaces
        except Exception as e:
            print(f"[ERROR] Could not list interfaces: {e}")
            return []

    def prompt_for_interface(self):
        """Prompt the user to select a network interface"""
        interfaces = self.get_available_interfaces()
        if not interfaces:
            messagebox.showerror("Error", "No network interfaces found.")
            self.root.quit()
            return None
        interface_var = tk.StringVar()
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Network Interface")
        dialog.geometry("350x150")
        ttk.Label(dialog, text="Select the network interface to monitor:").pack(pady=10)
        combo = ttk.Combobox(dialog, textvariable=interface_var, values=interfaces, state='readonly')
        combo.pack(pady=10)
        combo.current(0)
        selected = {'iface': None}
        def select():
            selected['iface'] = interface_var.get()
            dialog.destroy()
        ttk.Button(dialog, text="OK", command=select).pack(pady=10)
        dialog.grab_set()
        dialog.wait_window()
        return selected['iface']

    def start_capture(self):
        """Start packet capture"""
        if not self.capturing:
            self.capturing = True
            self.capture_thread = threading.Thread(target=self.capture_packets, daemon=True)
            self.capture_thread.start()
            print("[DEBUG] Packet capture started.")

    def stop_capture(self):
        """Stop packet capture"""
        if self.capturing:
            self.capturing = False
            # Wait for the capture thread to finish
            if self.capture_thread and self.capture_thread.is_alive():
                self.capture_thread.join(timeout=1.0)
            print("[DEBUG] Packet capture stopped.")

    def capture_packets(self):
        """Capture network packets and process them"""
        print("[DEBUG] Starting packet capture...")
        try:
            sniff(iface=self.selected_interface, prn=self.process_packet, store=0, stop_filter=lambda p: not self.capturing)
        except Exception as e:
            print(f"[ERROR] Failed to capture packets: {e}")

    def process_packet(self, packet):
        """Process a captured packet"""
        try:
            # Get basic packet info
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                protocol = self.get_protocol_name(packet)
                length = len(packet)
                # Get MAC addresses
                src_mac = packet[Ether].src
                dst_mac = packet[Ether].dst
                # Get packet info
                info = self.get_packet_info(packet)
                
                # Try to resolve hostname and detect service
                hostname = ''
                service = None
                try:
                    hostname = socket.gethostbyaddr(dst_ip)[0]
                    # Check if the hostname matches any known services
                    for service_id, service_info in SERVICES.items():
                        if any(domain in hostname.lower() for domain in service_info['domains']):
                            service = service_info['name']
                            # Update device's last service
                            if src_mac in self.device_manager.devices:
                                self.device_manager.devices[src_mac]['last_service'] = service
                                self.device_manager.devices[src_mac]['last_seen'] = datetime.now()
                                self.device_manager.devices[src_mac]['status'] = 'active'
                                
                                # Add service access to history
                                if src_mac not in self.device_history:
                                    self.device_history[src_mac] = []
                                self.device_history[src_mac].append({
                                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'event': 'Service Access',
                                    'details': f"Accessed {service} ({hostname})"
                                })
                            break
                except Exception:
                    pass
                
                # Prepare data for Activity tab with correct timestamp
                current_time = datetime.now()
                packet_data = {
                    'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'protocol': protocol,
                    'source': src_ip,
                    'destination': dst_ip,
                    'hostname': hostname,
                    'length': length,
                    'info': info,
                    'service': service
                }
                self.data_queue.put(packet_data)
                self.network_data.append(packet_data)  # Add to network_data for export
                
                # Update device information and track history
                if src_mac not in self.device_manager.devices:
                    self.device_manager.update_device(src_mac, src_ip)
                    # Add first seen to history
                    if src_mac not in self.device_history:
                        self.device_history[src_mac] = []
                    self.device_history[src_mac].append({
                        'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'event': 'First Seen',
                        'details': f"IP: {src_ip}, Protocol: {protocol}"
                    })
                else:
                    # Update last seen and track connection
                    device = self.device_manager.devices[src_mac]
                    if device.get('ip') != src_ip:
                        device['ip'] = src_ip
                        # Add IP change to history
                        if src_mac not in self.device_history:
                            self.device_history[src_mac] = []
                        self.device_history[src_mac].append({
                            'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'event': 'IP Change',
                            'details': f"New IP: {src_ip}"
                        })
                
                if dst_mac not in self.device_manager.devices:
                    self.device_manager.update_device(dst_mac, dst_ip)
                    # Add first seen to history for destination device
                    if dst_mac not in self.device_history:
                        self.device_history[dst_mac] = []
                    self.device_history[dst_mac].append({
                        'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'event': 'First Seen',
                        'details': f"IP: {dst_ip}, Protocol: {protocol}"
                    })
                
                # Update device list and history view
                self.update_device_list()
                self.update_history_view()
                
        except Exception as e:
            print(f"Error processing packet: {str(e)}")

    def update_history_view(self):
        """Update the history tree view with device history data"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Add history entries
        for mac, history in self.device_history.items():
            device_name = self.known_devices.get(mac, "Unknown")
            category = self.device_categories.get(mac, "Uncategorized")
            
            for entry in history:
                self.history_tree.insert('', 'end', values=(
                    device_name,
                    category,
                    entry['event'],
                    entry['time'],
                    entry['details']
                ))

    def periodic_update_history_view(self):
        """Update the history view at a fixed interval to reduce flicker."""
        self.update_history_view()
        self.root.after(1000, self.periodic_update_history_view)

    def export_history(self):
        """Export the history list to a CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save History As...'
        )
        if not file_path:
            return
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Device', 'Category', 'Event', 'Time', 'Details'])
            for mac, history in self.device_history.items():
                device_name = self.known_devices.get(mac, "Unknown")
                category = self.device_categories.get(mac, "Uncategorized")
                for entry in history:
                    writer.writerow([
                        device_name,
                        category,
                        entry['event'],
                        entry['time'],
                        entry['details']
                    ])
        messagebox.showinfo("Success", f"History data exported successfully to:\n{file_path}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.run() 