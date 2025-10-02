"""
System Information Collector
Generates comprehensive hardware and software reports for Windows systems
"""

import platform
import psutil
import subprocess
import json
import socket
import datetime
import os
import sys
from pathlib import Path
import wmi
import winreg
import ctypes
from collections import defaultdict

class SystemInfoCollector:
    def __init__(self):
        self.wmi = wmi.WMI()
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def get_size(self, bytes_size):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    def get_cpu_info(self):
        """Collect detailed CPU information"""
        cpu_info = {}
        try:
            # Basic CPU info
            cpu_info['Processor Name'] = platform.processor()
            cpu_info['Physical Cores'] = psutil.cpu_count(logical=False)
            cpu_info['Logical Cores'] = psutil.cpu_count(logical=True)
            cpu_info['Max Frequency'] = f"{psutil.cpu_freq().max:.2f} MHz"
            cpu_info['Current Frequency'] = f"{psutil.cpu_freq().current:.2f} MHz"
            cpu_info['Architecture'] = platform.machine()
            
            # WMI CPU details
            for processor in self.wmi.Win32_Processor():
                cpu_info['Manufacturer'] = processor.Manufacturer
                cpu_info['Model'] = processor.Name
                cpu_info['Socket'] = processor.SocketDesignation
                cpu_info['L2 Cache Size'] = f"{processor.L2CacheSize} KB" if processor.L2CacheSize else "N/A"
                cpu_info['L3 Cache Size'] = f"{processor.L3CacheSize} KB" if processor.L3CacheSize else "N/A"
                cpu_info['Voltage'] = f"{processor.CurrentVoltage / 10:.2f} V" if processor.CurrentVoltage else "N/A"
                cpu_info['Status'] = processor.Status
                
            # CPU usage per core
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            for i, percentage in enumerate(cpu_percent):
                cpu_info[f'Core {i} Usage'] = f"{percentage}%"
                
        except Exception as e:
            cpu_info['Error'] = str(e)
        
        return cpu_info
    
    def get_memory_info(self):
        """Collect detailed memory information"""
        memory_info = {}
        try:
            # Virtual memory
            vm = psutil.virtual_memory()
            memory_info['Total RAM'] = self.get_size(vm.total)
            memory_info['Available RAM'] = self.get_size(vm.available)
            memory_info['Used RAM'] = self.get_size(vm.used)
            memory_info['RAM Usage'] = f"{vm.percent}%"
            
            # Physical memory modules
            physical_memory = []
            for mem in self.wmi.Win32_PhysicalMemory():
                mem_details = {
                    'Capacity': self.get_size(int(mem.Capacity)) if mem.Capacity else "N/A",
                    'Speed': f"{mem.Speed} MHz" if mem.Speed else "N/A",
                    'Manufacturer': mem.Manufacturer if mem.Manufacturer else "Unknown",
                    'Part Number': mem.PartNumber.strip() if mem.PartNumber else "N/A",
                    'Serial Number': mem.SerialNumber.strip() if mem.SerialNumber else "N/A",
                    'Form Factor': self.get_form_factor(mem.FormFactor),
                    'Memory Type': self.get_memory_type(mem.MemoryType),
                    'Device Locator': mem.DeviceLocator if mem.DeviceLocator else "N/A"
                }
                physical_memory.append(mem_details)
            
            memory_info['Physical Memory Modules'] = physical_memory
            
        except Exception as e:
            memory_info['Error'] = str(e)
        
        return memory_info
    
    def get_form_factor(self, code):
        """Convert memory form factor code to string"""
        factors = {
            0: "Unknown", 8: "DIMM", 12: "SODIMM"
        }
        return factors.get(code, f"Code {code}")
    
    def get_memory_type(self, code):
        """Convert memory type code to string"""
        types = {
            0: "Unknown", 20: "DDR", 21: "DDR2", 24: "DDR3", 26: "DDR4", 34: "DDR5"
        }
        return types.get(code, f"Type {code}")
    
    def get_disk_info(self):
        """Collect detailed disk information"""
        disk_info = {}
        try:
            # Disk partitions
            partitions = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    part_info = {
                        'Device': partition.device,
                        'Mountpoint': partition.mountpoint,
                        'File System': partition.fstype,
                        'Total Size': self.get_size(usage.total),
                        'Used': self.get_size(usage.used),
                        'Free': self.get_size(usage.free),
                        'Usage': f"{usage.percent}%"
                    }
                    partitions.append(part_info)
                except PermissionError:
                    continue
            
            disk_info['Partitions'] = partitions
            
            # Physical disks
            physical_disks = []
            for disk in self.wmi.Win32_DiskDrive():
                disk_details = {
                    'Model': disk.Model,
                    'Size': self.get_size(int(disk.Size)) if disk.Size else "N/A",
                    'Interface': disk.InterfaceType,
                    'Media Type': disk.MediaType,
                    'Serial Number': disk.SerialNumber.strip() if disk.SerialNumber else "N/A",
                    'Partitions': disk.Partitions,
                    'Status': disk.Status
                }
                physical_disks.append(disk_details)
            
            disk_info['Physical Disks'] = physical_disks
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                disk_info['Total Read'] = self.get_size(disk_io.read_bytes)
                disk_info['Total Write'] = self.get_size(disk_io.write_bytes)
                disk_info['Read Count'] = disk_io.read_count
                disk_info['Write Count'] = disk_io.write_count
            
        except Exception as e:
            disk_info['Error'] = str(e)
        
        return disk_info
    
    def get_gpu_info(self):
        """Collect GPU information"""
        gpu_info = []
        try:
            for gpu in self.wmi.Win32_VideoController():
                gpu_details = {
                    'Name': gpu.Name,
                    'Driver Version': gpu.DriverVersion,
                    'Driver Date': gpu.DriverDate[:8] if gpu.DriverDate else "N/A",
                    'Video Processor': gpu.VideoProcessor if gpu.VideoProcessor else "N/A",
                    'Video Architecture': gpu.VideoArchitecture,
                    'Video Memory': self.get_size(int(gpu.AdapterRAM)) if gpu.AdapterRAM else "N/A",
                    'Current Resolution': f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}" if gpu.CurrentHorizontalResolution else "N/A",
                    'Refresh Rate': f"{gpu.CurrentRefreshRate} Hz" if gpu.CurrentRefreshRate else "N/A",
                    'Status': gpu.Status
                }
                gpu_info.append(gpu_details)
        except Exception as e:
            gpu_info.append({'Error': str(e)})
        
        return gpu_info
    
    def get_network_info(self):
        """Collect network information"""
        network_info = {}
        try:
            # Network interfaces
            interfaces = []
            for interface_name, addresses in psutil.net_if_addrs().items():
                interface_details = {'Interface': interface_name, 'Addresses': []}
                for addr in addresses:
                    addr_info = {
                        'Family': str(addr.family),
                        'Address': addr.address,
                        'Netmask': addr.netmask if addr.netmask else "N/A",
                        'Broadcast': addr.broadcast if addr.broadcast else "N/A"
                    }
                    interface_details['Addresses'].append(addr_info)
                interfaces.append(interface_details)
            
            network_info['Interfaces'] = interfaces
            
            # Network adapters from WMI
            adapters = []
            for adapter in self.wmi.Win32_NetworkAdapter():
                if adapter.PhysicalAdapter:
                    adapter_info = {
                        'Name': adapter.Name,
                        'Manufacturer': adapter.Manufacturer if adapter.Manufacturer else "N/A",
                        'MAC Address': adapter.MACAddress if adapter.MACAddress else "N/A",
                        'Speed': f"{int(adapter.Speed) / 1000000} Mbps" if adapter.Speed else "N/A",
                        'Connection Status': adapter.NetConnectionStatus,
                        'Adapter Type': adapter.AdapterType if adapter.AdapterType else "N/A"
                    }
                    adapters.append(adapter_info)
            
            network_info['Physical Adapters'] = adapters
            
            # Network statistics
            net_io = psutil.net_io_counters()
            network_info['Total Bytes Sent'] = self.get_size(net_io.bytes_sent)
            network_info['Total Bytes Received'] = self.get_size(net_io.bytes_recv)
            network_info['Packets Sent'] = net_io.packets_sent
            network_info['Packets Received'] = net_io.packets_recv
            
            # Hostname and IP
            network_info['Hostname'] = socket.gethostname()
            try:
                network_info['Local IP'] = socket.gethostbyname(socket.gethostname())
            except:
                network_info['Local IP'] = "Unable to determine"
            
        except Exception as e:
            network_info['Error'] = str(e)
        
        return network_info
    
    def get_motherboard_info(self):
        """Collect motherboard information"""
        mb_info = {}
        try:
            for board in self.wmi.Win32_BaseBoard():
                mb_info['Manufacturer'] = board.Manufacturer
                mb_info['Product'] = board.Product
                mb_info['Version'] = board.Version
                mb_info['Serial Number'] = board.SerialNumber.strip() if board.SerialNumber else "N/A"
                
            for bios in self.wmi.Win32_BIOS():
                mb_info['BIOS Manufacturer'] = bios.Manufacturer
                mb_info['BIOS Version'] = bios.Version
                mb_info['BIOS Release Date'] = bios.ReleaseDate[:8] if bios.ReleaseDate else "N/A"
                mb_info['BIOS Serial Number'] = bios.SerialNumber.strip() if bios.SerialNumber else "N/A"
                
        except Exception as e:
            mb_info['Error'] = str(e)
        
        return mb_info
    
    def get_battery_info(self):
        """Collect battery information (for laptops)"""
        battery_info = {}
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_info['Percentage'] = f"{battery.percent}%"
                battery_info['Power Plugged'] = "Yes" if battery.power_plugged else "No"
                if battery.secsleft != -1:
                    hours, remainder = divmod(battery.secsleft, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    battery_info['Time Remaining'] = f"{int(hours)}h {int(minutes)}m"
                else:
                    battery_info['Time Remaining'] = "Calculating..." if not battery.power_plugged else "N/A (Plugged In)"
            else:
                battery_info['Status'] = "No battery detected (Desktop PC)"
                
        except Exception as e:
            battery_info['Error'] = str(e)
        
        return battery_info
    
    def get_os_info(self):
        """Collect operating system information"""
        os_info = {}
        try:
            os_info['Operating System'] = f"{platform.system()} {platform.release()}"
            os_info['Version'] = platform.version()
            os_info['Architecture'] = platform.architecture()[0]
            os_info['Machine'] = platform.machine()
            os_info['Node Name'] = platform.node()
            
            # Windows specific info
            for os_item in self.wmi.Win32_OperatingSystem():
                os_info['Caption'] = os_item.Caption
                os_info['Build Number'] = os_item.BuildNumber
                os_info['Serial Number'] = os_item.SerialNumber
                os_info['Install Date'] = os_item.InstallDate[:8] if os_item.InstallDate else "N/A"
                os_info['Last Boot'] = os_item.LastBootUpTime[:14] if os_item.LastBootUpTime else "N/A"
                os_info['System Directory'] = os_item.SystemDirectory
                os_info['Windows Directory'] = os_item.WindowsDirectory
                os_info['Registered User'] = os_item.RegisteredUser
                os_info['Organization'] = os_item.Organization if os_item.Organization else "N/A"
            
            # Boot time
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            os_info['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            os_info['Error'] = str(e)
        
        return os_info
    
    def get_installed_software(self):
        """Collect installed software information"""
        software_list = []
        try:
            # Check multiple registry locations
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            
            for hkey, path in registry_paths:
                try:
                    registry = winreg.OpenKey(hkey, path)
                    for i in range(winreg.QueryInfoKey(registry)[0]):
                        try:
                            subkey_name = winreg.EnumKey(registry, i)
                            subkey = winreg.OpenKey(registry, subkey_name)
                            
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                version = "N/A"
                                publisher = "N/A"
                                install_date = "N/A"
                                
                                try:
                                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                except:
                                    pass
                                
                                try:
                                    publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                                except:
                                    pass
                                
                                try:
                                    install_date = winreg.QueryValueEx(subkey, "InstallDate")[0]
                                except:
                                    pass
                                
                                software_list.append({
                                    'Name': name,
                                    'Version': version,
                                    'Publisher': publisher,
                                    'Install Date': install_date
                                })
                            except:
                                pass
                            
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    
                    winreg.CloseKey(registry)
                except:
                    continue
            
            # Remove duplicates based on name and version
            unique_software = []
            seen = set()
            for sw in software_list:
                key = (sw['Name'], sw['Version'])
                if key not in seen:
                    seen.add(key)
                    unique_software.append(sw)
            
            # Sort by name
            unique_software.sort(key=lambda x: x['Name'].lower())
            
        except Exception as e:
            unique_software = [{'Error': str(e)}]
        
        return unique_software
    
    def get_startup_programs(self):
        """Collect startup programs"""
        startup_list = []
        try:
            for startup in self.wmi.Win32_StartupCommand():
                startup_list.append({
                    'Name': startup.Name,
                    'Command': startup.Command,
                    'Location': startup.Location,
                    'User': startup.User if startup.User else "All Users"
                })
        except Exception as e:
            startup_list.append({'Error': str(e)})
        
        return startup_list
    
    def get_services(self):
        """Collect Windows services"""
        services_list = []
        try:
            for service in self.wmi.Win32_Service():
                services_list.append({
                    'Name': service.Name,
                    'Display Name': service.DisplayName,
                    'State': service.State,
                    'Start Mode': service.StartMode,
                    'Path': service.PathName if service.PathName else "N/A"
                })
            
            # Sort by name
            services_list.sort(key=lambda x: x['Name'].lower())
            
        except Exception as e:
            services_list.append({'Error': str(e)})
        
        return services_list
    
    def get_environment_variables(self):
        """Collect environment variables"""
        env_vars = {}
        try:
            for key, value in os.environ.items():
                env_vars[key] = value
        except Exception as e:
            env_vars['Error'] = str(e)
        
        return env_vars
    
    def get_running_processes(self):
        """Collect running processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append({
                        'PID': proc.info['pid'],
                        'Name': proc.info['name'],
                        'User': proc.info['username'] if proc.info['username'] else "N/A",
                        'Memory %': f"{proc.info['memory_percent']:.2f}%",
                        'CPU %': f"{proc.info['cpu_percent']:.2f}%"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by memory usage
            processes.sort(key=lambda x: float(x['Memory %'].rstrip('%')), reverse=True)
            
        except Exception as e:
            processes.append({'Error': str(e)})
        
        return processes
    
    def get_windows_updates(self):
        """Collect Windows Update information"""
        updates_list = []
        try:
            for update in self.wmi.Win32_QuickFixEngineering():
                updates_list.append({
                    'HotFix ID': update.HotFixID,
                    'Description': update.Description if update.Description else "N/A",
                    'Installed On': update.InstalledOn if update.InstalledOn else "N/A",
                    'Installed By': update.InstalledBy if update.InstalledBy else "N/A"
                })
            
            # Sort by HotFix ID
            updates_list.sort(key=lambda x: x['HotFix ID'], reverse=True)
            
        except Exception as e:
            updates_list.append({'Error': str(e)})
        
        return updates_list
    
    def get_user_accounts(self):
        """Collect user account information"""
        users_list = []
        try:
            for user in self.wmi.Win32_UserAccount():
                users_list.append({
                    'Name': user.Name,
                    'Full Name': user.FullName if user.FullName else "N/A",
                    'Domain': user.Domain,
                    'Disabled': "Yes" if user.Disabled else "No",
                    'Local Account': "Yes" if user.LocalAccount else "No",
                    'SID': user.SID
                })
        except Exception as e:
            users_list.append({'Error': str(e)})
        
        return users_list
    
    def collect_hardware_info(self):
        """Collect all hardware information"""
        print("Collecting hardware information...")
        hardware_data = {
            'Report Generated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'System Information': self.get_os_info(),
            'Motherboard & BIOS': self.get_motherboard_info(),
            'CPU': self.get_cpu_info(),
            'Memory': self.get_memory_info(),
            'Storage': self.get_disk_info(),
            'Graphics': self.get_gpu_info(),
            'Network': self.get_network_info(),
            'Battery': self.get_battery_info()
        }
        return hardware_data
    
    def collect_software_info(self):
        """Collect all software information"""
        print("Collecting software information...")
        software_data = {
            'Report Generated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Operating System': self.get_os_info(),
            'Installed Software': self.get_installed_software(),
            'Startup Programs': self.get_startup_programs(),
            'Windows Services': self.get_services(),
            'Environment Variables': self.get_environment_variables(),
            'Running Processes': self.get_running_processes(),
            'Windows Updates': self.get_windows_updates(),
            'User Accounts': self.get_user_accounts()
        }
        return software_data


class ReportGenerator:
    def __init__(self, output_dir="Reports"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_html_report(self, data, report_type):
        """Generate HTML report"""
        filename = f"{self.output_dir}/{report_type}_Report_{self.timestamp}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_type} Report - {data['Report Generated']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}
        
        .section-title::before {{
            content: "▶";
            color: #667eea;
            margin-right: 10px;
            font-size: 0.8em;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .info-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .info-label {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .info-value {{
            color: #333;
            font-size: 1.1em;
            word-break: break-word;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-top: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr:hover {{
            background-color: #f5f5f5;
        }}
        
        tbody tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        
        .card {{
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .card-title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.2em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 5px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 5px;
        }}
        
        .badge-success {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .badge-warning {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .badge-info {{
            background-color: #d1ecf1;
            color: #0c5460;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 3px solid #667eea;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
            }}
            
            .info-item:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ {report_type} Report</h1>
            <p>Generated on {data['Report Generated']}</p>
        </div>
        
        <div class="content">
"""
        
        for section_name, section_data in data.items():
            if section_name == 'Report Generated':
                continue
            
            html_content += f'<div class="section">\n'
            html_content += f'<h2 class="section-title">{section_name}</h2>\n'
            
            html_content += self._generate_section_html(section_data)
            
            html_content += '</div>\n'
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>System Information Report - Generated automatically</p>
            <p>For technical support and inquiries, please contact your IT department</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def _generate_section_html(self, data):
        """Generate HTML for a section based on data type"""
        html = ""
        
        if isinstance(data, dict):
            # Check if it's a special case with nested lists
            has_list = any(isinstance(v, list) for v in data.values())
            
            if has_list:
                for key, value in data.items():
                    if isinstance(value, list):
                        html += f'<h3 style="color: #667eea; margin-top: 20px; margin-bottom: 10px;">{key}</h3>\n'
                        html += self._generate_section_html(value)
                    else:
                        html += f'<div class="info-grid">\n'
                        html += f'<div class="info-item">\n'
                        html += f'<div class="info-label">{key}</div>\n'
                        html += f'<div class="info-value">{value}</div>\n'
                        html += f'</div>\n'
                        html += f'</div>\n'
            else:
                html += '<div class="info-grid">\n'
                for key, value in data.items():
                    if not isinstance(value, (list, dict)):
                        html += f'<div class="info-item">\n'
                        html += f'<div class="info-label">{key}</div>\n'
                        html += f'<div class="info-value">{value}</div>\n'
                        html += f'</div>\n'
                html += '</div>\n'
                
                # Handle nested dicts/lists
                for key, value in data.items():
                    if isinstance(value, (list, dict)):
                        html += f'<h3 style="color: #667eea; margin-top: 20px; margin-bottom: 10px;">{key}</h3>\n'
                        html += self._generate_section_html(value)
        
        elif isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                # Create table
                html += '<div class="table-container">\n'
                html += '<table>\n'
                html += '<thead><tr>\n'
                
                # Table headers
                for key in data[0].keys():
                    html += f'<th>{key}</th>\n'
                
                html += '</tr></thead>\n<tbody>\n'
                
                # Table rows
                for item in data:
                    html += '<tr>\n'
                    for value in item.values():
                        if isinstance(value, list):
                            html += f'<td>{self._format_nested_list(value)}</td>\n'
                        else:
                            html += f'<td>{value}</td>\n'
                    html += '</tr>\n'
                
                html += '</tbody>\n</table>\n'
                html += '</div>\n'
            else:
                # Simple list
                html += '<ul style="list-style-position: inside; padding-left: 20px;">\n'
                for item in data:
                    html += f'<li style="margin-bottom: 5px;">{item}</li>\n'
                html += '</ul>\n'
        
        return html
    
    def _format_nested_list(self, data):
        """Format nested list for table cell"""
        if isinstance(data, list):
            return '<br>'.join([str(item) for item in data])
        return str(data)


def main():
    print("=" * 70)
    print(" " * 15 + "SYSTEM INFORMATION COLLECTOR")
    print("=" * 70)
    print()
    
    try:
        # Initialize collector
        collector = SystemInfoCollector()
        
        # Collect hardware information
        print("\n[1/2] Collecting Hardware Information...")
        hardware_data = collector.collect_hardware_info()
        print("✓ Hardware information collected successfully")
        
        # Collect software information
        print("\n[2/2] Collecting Software Information...")
        software_data = collector.collect_software_info()
        print("✓ Software information collected successfully")
        
        # Generate reports
        print("\n" + "=" * 70)
        print("Generating Reports...")
        print("=" * 70)
        
        report_gen = ReportGenerator()
        
        hardware_file = report_gen.generate_html_report(hardware_data, "Hardware")
        print(f"\n✓ Hardware Report: {hardware_file}")
        
        software_file = report_gen.generate_html_report(software_data, "Software")
        print(f"✓ Software Report: {software_file}")
        
        print("\n" + "=" * 70)
        print("SUCCESS! Reports generated successfully!")
        print("=" * 70)
        print(f"\nReports saved in: {os.path.abspath('Reports')}")
        print("\nPress Enter to exit...")
        input()
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()
