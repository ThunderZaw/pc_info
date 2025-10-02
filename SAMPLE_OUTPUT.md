# System Information Collector - Sample Output

This document shows what information is collected in each report.

## 📊 Hardware Report Contents

### System Information
- Operating System name and version
- Architecture (32-bit/64-bit)
- Computer name
- Serial numbers
- Installation date
- Last boot time

### Motherboard & BIOS
- Manufacturer
- Model number
- Version
- Serial number
- BIOS manufacturer
- BIOS version
- BIOS release date

### CPU (Processor)
- Processor name and model
- Manufacturer
- Number of physical cores
- Number of logical cores (threads)
- Current frequency
- Maximum frequency
- Architecture
- Socket type
- L2 cache size
- L3 cache size
- Voltage
- Usage per core (real-time)

### Memory (RAM)
- Total RAM capacity
- Available RAM
- Used RAM
- RAM usage percentage
- **For each memory module:**
  - Capacity
  - Speed (MHz)
  - Manufacturer
  - Part number
  - Serial number
  - Form factor (DIMM, SODIMM)
  - Memory type (DDR3, DDR4, DDR5)
  - Slot location

### Storage (Disks)
- **For each partition:**
  - Drive letter
  - Mountpoint
  - File system type
  - Total size
  - Used space
  - Free space
  - Usage percentage
- **For each physical disk:**
  - Model
  - Total capacity
  - Interface type (SATA, NVMe, etc.)
  - Media type
  - Serial number
  - Number of partitions
  - Status
- **Disk I/O Statistics:**
  - Total bytes read
  - Total bytes written
  - Read count
  - Write count

### Graphics (GPU)
- **For each graphics card:**
  - Name/Model
  - Driver version
  - Driver date
  - Video processor
  - Video architecture
  - Video memory (VRAM)
  - Current resolution
  - Refresh rate
  - Status

### Network
- **For each network interface:**
  - Interface name
  - IP addresses (IPv4 and IPv6)
  - MAC address
  - Netmask
  - Broadcast address
- **For each physical adapter:**
  - Adapter name
  - Manufacturer
  - MAC address
  - Connection speed
  - Connection status
  - Adapter type
- **Network Statistics:**
  - Total bytes sent
  - Total bytes received
  - Packets sent
  - Packets received
  - Hostname
  - Local IP address

### Battery (Laptops)
- Current charge percentage
- Power plugged in status
- Estimated time remaining
- Battery status

---

## 💾 Software Report Contents

### Operating System
- Complete OS information
- Version and build number
- Serial number
- Installation date
- Last boot time
- System directory
- Windows directory
- Registered user
- Organization

### Installed Software
Complete list of all installed programs with:
- Program name
- Version number
- Publisher
- Installation date

Includes:
- Desktop applications
- Microsoft Store apps
- System components
- Development tools
- Everything in Add/Remove Programs

### Startup Programs
Programs that run automatically at startup:
- Program name
- Command/executable path
- Startup location (Registry, Startup folder, etc.)
- User account (All Users or specific user)

### Windows Services
Complete list of all Windows services:
- Service name
- Display name
- Current state (Running, Stopped, etc.)
- Start mode (Automatic, Manual, Disabled)
- Executable path

### Environment Variables
All system and user environment variables:
- PATH
- TEMP
- SystemRoot
- ProgramFiles
- UserProfile
- Custom variables
- And many more...

### Running Processes
All currently running processes:
- Process ID (PID)
- Process name
- User account running the process
- Memory usage percentage
- CPU usage percentage
- Sorted by memory usage

### Windows Updates
All installed Windows updates and hotfixes:
- HotFix ID (KB number)
- Description
- Installation date
- Installed by (user account)
- Sorted by most recent

### User Accounts
All local user accounts:
- Account name
- Full name
- Domain
- Enabled/Disabled status
- Local/Domain account
- Security Identifier (SID)

---

## 📈 Report Features

### Visual Design
- Modern, professional appearance
- Color-coded sections
- Easy-to-read tables
- Responsive grid layout
- Hover effects for interactivity
- Print-optimized styling

### Organization
- Clear section headers
- Logical grouping of information
- Collapsible data where appropriate
- Search-friendly (browser Ctrl+F works great)

### Export & Sharing
- Standard HTML format
- Opens in any web browser
- Can be printed to PDF
- Easy to email or share
- No special software needed to view

---

## 📏 Report Size

Typical report sizes:
- Hardware Report: 50-200 KB
- Software Report: 200-500 KB (varies with installed programs)

---

## 🔄 Update Frequency

Generate new reports:
- Before major system changes
- Monthly for documentation
- When troubleshooting issues
- Before and after upgrades
- For IT asset inventory

---

## 📋 Use Cases

Perfect for:
- IT support tickets
- System documentation
- Hardware inventory
- Software audits
- Troubleshooting
- Upgrade planning
- Asset management
- Compliance reporting

---

**All information is collected from official Windows APIs and WMI (Windows Management Instrumentation)**
