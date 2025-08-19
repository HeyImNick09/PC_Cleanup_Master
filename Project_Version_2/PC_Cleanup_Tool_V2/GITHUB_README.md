# 🖥️ PC Cleanup Tool - Professional System Optimizer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0-green.svg)](https://github.com/yourusername/pc-cleanup-tool)

**Professional-grade Windows system maintenance and optimization tool with modern UI and comprehensive reporting.**

## 🚀 Quick Start

### Version 2 (Recommended) - One-Click Operation
```bash
# Clone repository
git clone https://github.com/HeyImNick09/PC_Cleanup_Master.git
cd PC_Cleanup_Master/Project_Version_2/PC_Cleanup_Tool_V2

# Install dependencies
pip install -r v2_requirements.txt

# Run modern UI
python v2_modern_ui.py
```

### Version 1 - Advanced Features
```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI version
python gui_app.py

# Run CLI version
python main.py
```

## ✨ Features

### 🎯 Version 2 Highlights
- **🚀 One-Click Cleanup** - Complete system optimization in single action
- **📊 Before/After Analysis** - Comprehensive system state comparison
- **🎨 Modern UI** - Professional interface with real-time progress
- **📋 Advanced Reporting** - Detailed tabbed reports with recommendations
- **🌐 Offline/Online Modes** - Flexible operation based on connectivity
- **⚡ Real-time Progress** - Animated progress tracking with status updates

### 🔧 Core Functionality
- **Smart Temporary File Cleanup** - Safely removes temp files with in-use detection
- **Browser Cache Management** - Clears Chrome, Edge, Firefox, Opera, Brave caches
- **Registry Optimization** - Safe registry cleaning with backup mechanisms
- **Startup Program Management** - Analyzes and optimizes startup programs
- **System Health Monitoring** - Windows Update status and diagnostics
- **Memory Optimization** - Advanced memory cleanup and management

### 🏢 Enterprise Features
- **Disk Space Analysis** - Comprehensive drive usage reporting
- **Duplicate File Detection** - Identifies and manages duplicate files
- **Performance Monitoring** - CPU, memory, and system metrics
- **Comprehensive Logging** - Detailed audit trails for compliance
- **White-label Branding** - Customizable for business deployment
- **Professional Packaging** - PyInstaller executable creation

## 📸 Screenshots

### Version 2 Modern Interface
*One-click operation with before/after system analysis*

### Version 1 Professional Interface
*Advanced features with detailed control options*

## 🛠️ Installation

### System Requirements
- **OS**: Windows 10/11 (x64 recommended)
- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 100MB free space
- **Privileges**: Administrator recommended for full functionality

### Dependencies
```bash
# Core dependencies
pip install psutil pywin32 wmi winshell

# For building executables (optional)
pip install pyinstaller

# For development (optional)
pip install pytest black flake8
```

## 🎮 Usage

### Version 2 - One-Click Operation

1. **Launch Application**
   ```bash
   python v2_modern_ui.py
   ```

2. **Select Mode**
   - **Online Mode**: Full functionality with Windows Update checking
   - **Offline Mode**: Core cleanup without network features

3. **One-Click Cleanup**
   - Click the large "🚀 ONE-CLICK CLEANUP" button
   - Watch real-time progress with animated status
   - Review comprehensive before/after report

4. **Individual Operations** (Optional)
   - Clean Temp Files
   - Clear Browser Cache
   - Optimize Registry
   - Manage Startup Programs
   - Analyze System State

### Version 1 - Advanced Control

1. **GUI Interface**
   ```bash
   python gui_app.py
   ```

2. **Command Line Interface**
   ```bash
   python main.py [options]
   ```

3. **Custom Branding**
   ```bash
   python branding_config.py
   ```

4. **Build Executable**
   ```bash
   python build_config.py
   ```

## 📊 What Gets Cleaned

### Temporary Files
- Windows temp directory (`%TEMP%`)
- User temp directory (`%USERPROFILE%\AppData\Local\Temp`)
- System temp directory (`C:\Windows\Temp`)

### Browser Data
- **Chrome**: Cache, cookies, history (optional)
- **Edge**: Cache, temporary files
- **Firefox**: Cache, temporary files
- **Opera**: Cache, temporary files
- **Brave**: Cache, temporary files

### System Optimization
- Registry cleanup (safe entries only)
- Startup program optimization
- Memory cleanup and optimization
- Recycle bin clearing

## 🔒 Safety Features

- **File-in-Use Detection** - Prevents deletion of active files
- **Process Monitoring** - Avoids conflicts with running applications
- **Registry Backup** - Automatic backup before registry modifications
- **Permission Handling** - Graceful handling of access-denied files
- **Error Recovery** - Comprehensive error handling and logging
- **Audit Trail** - Complete operation logging for compliance

## 📋 Reports & Logging

### Version 2 Reports
- **Before/After Comparison** - System state analysis
- **Operation Summary** - Detailed cleanup statistics
- **Recommendations** - System optimization suggestions
- **Export Options** - JSON format for sharing

### Logging Locations
- **V2 Logs**: `~/Desktop/PC_Cleanup_V2_Logs/`
- **V1 Logs**: `~/Desktop/PC_Cleanup_Logs/`
- **Reports**: `~/Desktop/PC_Cleanup_V2_Reports/`

## 🏢 Business Deployment

### White-Label Customization
```bash
# Configure branding
python branding_config.py

# Build custom executable
python build_config.py
```

### Pricing Tiers
- **Basic**: Core cleanup functionality
- **Professional**: Advanced features + reporting
- **Enterprise**: Full feature set + branding

### Installation Methods
1. **Standalone Executable** - Single file deployment
2. **MSI Installer** - Professional Windows installer
3. **Portable Version** - No installation required

## 🔧 Development

### Project Structure
```
PC_Cleanup_Tool/
├── Version 2 (Enhanced)
│   ├── v2_core_engine.py      # Enhanced cleanup engine
│   ├── v2_modern_ui.py        # Modern UI framework
│   └── v2_requirements.txt    # V2 dependencies
│
├── Version 1 (Stable)
│   ├── main.py                # CLI interface
│   ├── gui_app.py             # GUI interface
│   ├── browser_cleaner.py     # Browser cleaning
│   ├── enterprise_features.py # Enterprise tools
│   ├── build_config.py        # Build system
│   └── branding_config.py     # Customization
│
└── Documentation
    ├── README.md              # Project overview
    ├── DEPLOYMENT_GUIDE.md    # Business deployment
    ├── SUMMARY_DOCUMENT_V1.md # V1 documentation
    └── SUMMARY_DOCUMENT_V2.md # V2 documentation
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Testing
```bash
# Run tests (when available)
pytest tests/

# Code formatting
black *.py

# Linting
flake8 *.py
```

## 📈 Performance

### Typical Results
- **Temp Files**: 500MB - 2GB recovered
- **Browser Cache**: 100MB - 1GB recovered
- **Registry**: 50-200 entries optimized
- **Startup**: 5-15 programs analyzed
- **Operation Time**: 30-120 seconds

### System Impact
- **CPU Usage**: Low during operation
- **Memory Usage**: <100MB typical
- **Disk I/O**: Optimized for SSD/HDD
- **Network**: Minimal (update checking only)

## ❓ FAQ

### General Questions

**Q: Is it safe to use?**
A: Yes, the tool includes comprehensive safety features including file-in-use detection, process monitoring, and registry backup.

**Q: Do I need administrator privileges?**
A: Administrator privileges are recommended for full functionality, but the tool can operate with limited privileges.

**Q: Will it delete important files?**
A: No, the tool only targets temporary files, caches, and safe registry entries. System files are protected.

### Technical Questions

**Q: What's the difference between V1 and V2?**
A: V2 features one-click operation, modern UI, before/after analysis, and enhanced reporting. V1 offers more granular control.

**Q: Can I run both versions?**
A: Yes, both versions can coexist and use the same underlying cleanup modules.

**Q: How do I build an executable?**
A: Use `python build_config.py` for V1 or follow the deployment guide for custom builds.

## 🐛 Troubleshooting

### Common Issues

**Issue: "Permission Denied" errors**
- Solution: Run as administrator or close affected applications

**Issue: Browser cache not cleaning**
- Solution: Close all browser instances before running cleanup

**Issue: Windows Update check fails**
- Solution: Check network connection or use offline mode

**Issue: Slow performance**
- Solution: Close unnecessary applications during cleanup

### Getting Help
1. Check the [Issues](https://github.com/yourusername/pc-cleanup-tool/issues) page
2. Review the [Deployment Guide](DEPLOYMENT_GUIDE.md)
3. Check the [Documentation](SUMMARY_DOCUMENT_V2.md)
4. Contact support (for business users)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Uses psutil for system monitoring
- Integrates with Windows APIs via pywin32
- Inspired by professional system maintenance tools

## 📞 Support

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and examples
- **Code Examples**: Sample implementations and customizations

### Business Support
- **Professional Services**: Custom development and deployment
- **Enterprise Licensing**: Volume licensing and support contracts
- **Training**: Implementation and usage training

---

**⭐ Star this repository if you find it helpful!**

*Professional Windows system optimization made simple and safe.*
