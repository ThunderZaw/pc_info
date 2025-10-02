# 🖥️ System Information Collector

A comprehensive one-click tool that generates detailed hardware and software reports for Windows systems.

## 📋 Features

### Hardware Report Includes:
- **CPU Information**: Processor details, cores, frequency, cache, usage per core
- **Memory**: Total/available RAM, physical memory modules with specifications
- **Storage**: Disk partitions, physical disks, capacity, usage, I/O statistics
- **Graphics**: GPU details, video memory, driver information, resolution
- **Network**: Network adapters, IP addresses, MAC addresses, statistics
- **Motherboard & BIOS**: Manufacturer, model, version, serial numbers
- **Battery**: Status, percentage, remaining time (for laptops)

### Software Report Includes:
- **Operating System**: Windows version, build, installation date, boot time
- **Installed Software**: Complete list with versions and publishers
- **Startup Programs**: Programs that run at startup
- **Windows Services**: All services with their status
- **Environment Variables**: System and user environment variables
- **Running Processes**: Active processes with memory and CPU usage
- **Windows Updates**: Installed updates and hotfixes
- **User Accounts**: Local user accounts and their status

## 🚀 Quick Start

### Option 1: One-Click Batch File (Easiest)
1. Double-click `Generate_System_Reports.bat`
2. Wait for the scan to complete
3. Reports will open automatically

### Option 2: PowerShell Script
1. Right-click `Generate_System_Reports.ps1`
2. Select "Run with PowerShell"
3. Wait for the scan to complete
4. Reports will open automatically

### Option 3: Direct Python Execution
```bash
python system_info_collector.py
```

## 📦 Requirements

- **Python 3.6 or higher**
- **Required Python packages** (automatically installed):
  - psutil
  - WMI

### Installing Python
If you don't have Python installed:
1. Download from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Complete the installation

## 📄 Reports

Reports are generated in HTML format and saved in the `Reports` folder with timestamps:

- `Hardware_Report_YYYYMMDD_HHMMSS.html`
- `Software_Report_YYYYMMDD_HHMMSS.html`

### Report Features:
- ✨ Beautiful, modern design
- 📱 Responsive layout
- 🖨️ Print-friendly
- 🔍 Easy-to-read tables and grids
- 📊 Organized sections with visual hierarchy
- 🎨 Color-coded information

## 🔧 Manual Installation (if needed)

If the automatic installation doesn't work:

```bash
pip install psutil WMI
```

## 💡 Usage Tips

1. **Run as Administrator** for complete system information (optional but recommended)
2. Reports are timestamped, so you can track changes over time
3. Keep old reports for comparison when troubleshooting
4. Share reports with IT support when seeking help

## 📸 What You'll Get

Each report contains:
- Professional header with generation timestamp
- Organized sections with expandable information
- Color-coded data for easy reading
- Tables for list-based information
- Hover effects for better navigation
- Print-optimized layout

## ⚙️ Technical Details

- **Language**: Python 3
- **Architecture**: Modular design with separate collector and report generator
- **Data Sources**: WMI, psutil, Windows Registry, System APIs
- **Output Format**: HTML5 with embedded CSS
- **Compatibility**: Windows 7, 8, 10, 11, Server editions

## 🛠️ Troubleshooting

### "Python is not installed"
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "Access Denied" errors
- Run the script as Administrator
- Right-click the .bat file and select "Run as administrator"

### Missing information in reports
- Some information requires administrator privileges
- Certain hardware may not expose all details through WMI

### Reports not generating
- Check that you have write permissions in the folder
- Ensure antivirus isn't blocking the script
- Check the console output for specific error messages

## 📝 License

This tool is provided as-is for personal and professional use.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Ensure all requirements are met

## 🔒 Privacy

This tool:
- ✅ Runs completely offline
- ✅ Doesn't send data anywhere
- ✅ Generates reports locally only
- ✅ Doesn't collect personal information
- ✅ Open source - you can review the code

## 📊 Example Use Cases

- **IT Asset Management**: Document hardware inventory
- **Technical Support**: Provide detailed system info to support teams
- **System Upgrades**: Plan hardware upgrades with accurate specifications
- **Troubleshooting**: Identify system issues and conflicts
- **Documentation**: Maintain records of system configurations
- **Compliance**: Track installed software and updates

## 🎯 Future Enhancements

Potential improvements:
- Export to PDF format
- Compare reports feature
- Custom report filtering
- Linux and macOS support
- Email report functionality
- Scheduled automated scans

---

**Made with ❤️ for system administrators and IT professionals**
