"""Platform Utilities Module for Arthashila

This module provides platform-independent functions for accessing system information.
It abstracts away platform-specific implementations and provides a consistent interface
for the rest of the application to use.
"""

import platform
import psutil
import os
import sys

# Constants for platform identification
PLATFORM_WINDOWS = "windows"
PLATFORM_LINUX = "linux"
PLATFORM_MACOS = "darwin"

def get_platform_type():
    """
    Determine the current platform type.
    
    Returns:
        str: One of the platform constants (PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_MACOS)
    """
    system = platform.system().lower()
    if system == "windows":
        return PLATFORM_WINDOWS
    elif system == "linux":
        return PLATFORM_LINUX
    elif system == "darwin":
        return PLATFORM_MACOS
    else:
        return "unknown"

def get_system_info():
    """
    Get platform-independent system information.
    
    Returns:
        dict: Dictionary containing system information
    """
    uname = platform.uname()
    system_info = {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "python_version": platform.python_version(),
        "platform": platform.platform()
    }
    
    return system_info

def get_cpu_info():
    """
    Get platform-independent CPU information.
    
    Returns:
        dict: Dictionary containing CPU information
    """
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "total_cores": psutil.cpu_count(logical=True) or 0,
            "max_frequency": cpu_freq.max if cpu_freq and hasattr(cpu_freq, 'max') else None,
            "min_frequency": cpu_freq.min if cpu_freq and hasattr(cpu_freq, 'min') else None,
            "current_frequency": cpu_freq.current if cpu_freq and hasattr(cpu_freq, 'current') else None,
            "per_core_usage": psutil.cpu_percent(percpu=True)
        }
        return cpu_info
    except Exception as e:
        # Fallback with minimal information if detailed info isn't available
        return {
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "total_cores": psutil.cpu_count(logical=True) or 0,
            "per_core_usage": []
        }

def get_memory_info():
    """
    Get platform-independent memory information.
    
    Returns:
        dict: Dictionary containing memory information
    """
    try:
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        
        memory_info = {
            "virtual": {
                "total": virtual_memory.total,
                "available": virtual_memory.available,
                "used": virtual_memory.used,
                "percent": virtual_memory.percent
            },
            "swap": {
                "total": swap_memory.total,
                "free": swap_memory.free,
                "used": swap_memory.used,
                "percent": swap_memory.percent
            }
        }
        
        return memory_info
    except Exception as e:
        # Fallback with minimal information
        return {
            "virtual": {"percent": 0},
            "swap": {"percent": 0}
        }

def get_disk_info():
    """
    Get platform-independent disk information.
    
    Returns:
        list: List of dictionaries containing disk partition information
    """
    partitions_info = []
    
    try:
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info = {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
                partitions_info.append(partition_info)
            except (PermissionError, OSError):
                # Skip partitions that can't be accessed
                continue
                
        # If no partitions were found or accessible, add at least the root partition
        if not partitions_info:
            try:
                root_usage = psutil.disk_usage(os.path.abspath(os.sep))
                partitions_info.append({
                    "device": "Unknown",
                    "mountpoint": os.path.abspath(os.sep),
                    "fstype": "Unknown",
                    "total": root_usage.total,
                    "used": root_usage.used,
                    "free": root_usage.free,
                    "percent": root_usage.percent
                })
            except Exception:
                pass
                
        return partitions_info
    except Exception as e:
        # Return empty list if we can't get disk information
        return []

def get_battery_info():
    """
    Get platform-independent battery information.
    
    Returns:
        dict or None: Dictionary containing battery information if available,
                      None if battery is not detected or an error occurs
    """
    try:
        battery = psutil.sensors_battery()
        
        if battery is None:
            return None
        
        # Extract battery information
        status_info = {
            "percent": battery.percent,
            "power_plugged": battery.power_plugged,
            "status": "Charging" if battery.power_plugged else "Discharging",
            "secsleft": battery.secsleft
        }
        
        return status_info
    except Exception as e:
        # Return None if we can't get battery information
        return None

def get_process_list(sort_by="cpu_percent", search_term=None):
    """
    Get platform-independent process list.
    
    Args:
        sort_by (str): Field to sort processes by (cpu_percent, memory_mb, pid, name)
        search_term (str): Optional term to filter process names
        
    Returns:
        list: List of dictionaries containing process information
    """
    processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'status', 'create_time']):
            try:
                # Get process information
                proc_info = proc.info
                if search_term and search_term.lower() not in proc_info['name'].lower():
                    continue
                    
                # Get memory in MB
                memory_mb = proc_info['memory_info'].rss / (1024 * 1024) if proc_info['memory_info'] else 0
                
                # Get process create time
                create_time = "Unknown"
                if proc_info['create_time']:
                    try:
                        from datetime import datetime
                        create_time = datetime.fromtimestamp(proc_info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        pass
                
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'username': proc_info['username'] or "Unknown",
                    'cpu_percent': proc_info['cpu_percent'] or 0,
                    'memory_mb': memory_mb,
                    'status': proc_info['status'] or "Unknown",
                    'create_time': create_time
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort processes
        if sort_by == "cpu_percent":
            processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
        elif sort_by == "memory_mb":
            processes = sorted(processes, key=lambda x: x['memory_mb'], reverse=True)
        elif sort_by == "pid":
            processes = sorted(processes, key=lambda x: x['pid'])
        else:  # Process Name
            processes = sorted(processes, key=lambda x: x['name'].lower())
            
        return processes
    except Exception as e:
        # Return empty list if we can't get process information
        return []