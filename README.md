# 🔍 W8 Camera Scanner V1

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Termux-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Advanced IP Range Scanner & Camera Detector with Multi-Threading**

*Developed by W8Team/W8SOJIB*

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Support](#support)

</div>

---

## 📋 Description

W8 Camera Scanner is a powerful network scanning tool designed to detect cameras and web services across IP ranges. It features multi-threaded scanning for maximum performance, automatic camera detection, and network route tracing capabilities.

## ✨ Features

### 🚀 Super Fast Scan Mode
- **Multi-threaded scanning** (up to 500 threads)
- **Auto CPU detection** - Scales threads based on your CPU cores
- **Smart camera detection** - Identifies cameras by title and content
- **Real-time results** - Live display of found devices
- **Auto-save results** - Saves to `SuperFastScan_Results.txt`

### 🔍 Trace Route Mode
- **Network path tracing** to any domain/IP
- **Color-coded output** for easy reading
- **Fast execution** with optimized timeouts
- **Auto-traces to google.com** by default

### 📷 Neighbours Camera Scanner
- **Local network scanning** - Auto-detects your subnet
- **RTSP camera detection** - Finds cameras on port 554
- **Brand identification** - Detects Dahua and Hikvision cameras
- **Multi-threaded** - 80 threads for fast scanning
- **RTSP URL generation** - Ready-to-use camera URLs
- **Auto-save results** - Saves to `NeighboursCameras_Results.txt`

### 🎯 Camera Detection
Automatically detects:
- ✅ **WEB SERVICE** cameras (Dahua/Anjhua)
- ✅ **HIK Vision** cameras
- ✅ **DVR** systems
- ✅ **IP Cameras**
- ✅ **Login pages** (potential cameras)

### 🌐 Network Information
- Displays your **Local IP address**
- Shows **Router Gateway** IP
- **Cross-platform** gateway detection

### 💻 Platform Support
- ✅ Windows (7, 8, 10, 11)
- ✅ Linux (Ubuntu, Debian, Kali, etc.)
- ✅ macOS
- ✅ **Termux** (Android) - Full support!

---

## 📦 Installation

### Windows / Linux / macOS

#### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/W8SOJIB/W8CameraScannerV1.git
cd W8CameraScannerV1
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Run the Scanner
```bash
python W8CameraScanner.py
```

### 📱 Termux (Android)

#### Step 1: Install Required Packages

**Update packages:**
```bash
pkg update && pkg upgrade -y
```

**Install Python:**
```bash
pkg install python -y
```

**Install git:**
```bash
pkg install git -y
```

**Install traceroute (optional, for trace route feature):**
```bash
pkg install traceroute -y
```

#### Step 2: Clone and Install
# Clone repository
```
git clone https://github.com/W8SOJIB/W8CameraScannerV1.git
```

```
cd W8CameraScannerV1
```

# Install dependencies

```
pip install -r requirements.txt
```

#### Step 3: Run
```bash
python W8CameraScanner.py
```

---

## 🎮 Usage

### Main Menu
When you run the tool, you'll see:

```
╔═══════════════════════════════════════╗
║   IP Range Camera Scanner             ║
║   W8Team - IP Scanner                 ║
║   Credit: W8Team/W8SOJIB              ║
╚═══════════════════════════════════════╝
[*] Developed by: W8Team/W8SOJIB
[*] GitHub: github.com/W8SOJIB
[*] Termux Supported ✓

[i] Time: 2025-12-23 02:52:49 PM
[i] Your Local IP: 192.168.1.100
[i] Router Gateway: 192.168.1.1

==================================================
Select Mode:
==================================================
1. 🔍 Trace Route
2. ⚡ SUPER FAST SCAN (Camera Scanner)
3. 📷 Neighbours Camera Scanner
4. Exit
==================================================
```

### Option 1: Trace Route 🔍
- Automatically traces route to **google.com**
- Shows all network hops
- Color-coded results (Green = Success, Red = Timeout)
- Displays total hop count

### Option 2: Super Fast Scan ⚡
- Enter **Start IP** and **End IP** (or press Enter for single IP)
- Scans ports **80** and **8080**
- **Multi-threaded** for maximum speed
- Shows only **cameras** (filters out regular web servers)
- Saves results to `SuperFastScan_Results.txt`

### Option 3: Neighbours Camera Scanner 📷
- **Auto-detects** your local network subnet
- Scans all 254 IPs in your subnet automatically
- Finds **RTSP cameras** on port 554
- Identifies **Dahua** and **Hikvision** cameras
- Generates **RTSP URLs** for easy access
- Saves results to `NeighboursCameras_Results.txt`

---

## 📸 Examples

### Example 1: Scan Single IP
```
Enter Start IP: 192.168.1.1
Enter End IP (press Enter for single IP): [Press Enter]

[✓] Camera Found: 192.168.1.1:80 - WEB SERVICE
```

### Example 2: Scan IP Range
```
Enter Start IP: 192.168.1.1
Enter End IP (press Enter for single IP): 192.168.1.255

[✓] Camera Found: 192.168.1.10:80 - Camera - Login
[✓] Camera Found: 192.168.1.50:8080 - Camera - DVR
[✓] Camera Found: 192.168.1.100:80 - Camera - WEB SERVICE

[i] Total IPs scanned: 255
[i] Cameras found: 3
[i] Time taken: 45.23 seconds
[i] Speed: 1128 ports/sec
```

### Example 3: Neighbours Camera Scanner
```
Select Mode: 3

[📷] NEIGHBOURS CAMERA SCANNER [📷]
==================================================

[i] Detected Subnet: 192.168.1.x
[*] Scanning for RTSP cameras (port 554)...
[*] This may take a few minutes...

[✓] Camera Found: 192.168.1.100 - DH-IPC-HDW1230M
[✓] Camera Found: 192.168.1.101 - HIKVISION CAMERA

[*] Found 2 RTSP CAMERAS:

[1] 192.168.1.100
    Name: DH-IPC-HDW1230M
    RTSP URL: rtsp://192.168.1.100:554

[2] 192.168.1.101
    Name: HIKVISION CAMERA
    RTSP URL: rtsp://192.168.1.101:554

[✓] Results saved to: NeighboursCameras_Results.txt

[i] Total IPs scanned: 254
[i] Cameras found: 2
[i] Time taken: 12.45 seconds
```

### Example 4: Results File
Results are automatically saved to `SuperFastScan_Results.txt`:
```
============================================================
SUPER FAST SCAN - CAMERAS FOUND
============================================================

IP: 192.168.1.10:80
Title: Login Page
Server: nginx/1.18.0
Type: Camera - Login
URL: http://192.168.1.10
------------------------------------------------------------

IP: 192.168.1.50:8080
Title: DVR System
Server: Unknown
Type: Camera - DVR
URL: http://192.168.1.50:8080
------------------------------------------------------------
```

---

## ⚡ Performance

- **Speed:** Up to 1000+ ports per second
- **Threads:** Automatically scales to your CPU (up to 500 threads)
- **Efficiency:** Only shows cameras, filters out regular web servers
- **Memory:** Low memory footprint (~50MB)

### Performance Benchmarks
| IP Range | Time | Speed | System |
|----------|------|-------|--------|
| 256 IPs (/24) | ~45s | 1128 ports/sec | 4-core CPU |
| 1024 IPs (/22) | ~3min | 1138 ports/sec | 8-core CPU |
| Single IP | <1s | Instant | Any |

---

## 🎨 Features Breakdown

### Smart Camera Detection
The tool identifies cameras based on:
- **Title keywords:** WEB, Login, DVR, Camera, IPCam
- **Content signatures:** WEB SERVICE, login.asp, DVR markers
- **Response patterns:** Camera-specific HTTP responses
- **RTSP protocol:** Detects streaming cameras on port 554
- **Brand identification:** Dahua (DH-XXX) and Hikvision models

### Filtered Output
Only shows:
- ✅ Cameras and DVR systems
- ✅ RTSP streaming cameras
- ❌ Regular web servers (filtered out)
- ❌ Empty responses (ignored)

---

## 🛠️ Technical Details

### Ports Scanned
- **Port 80** (HTTP) - Super Fast Scan
- **Port 8080** (Alternative HTTP) - Super Fast Scan
- **Port 554** (RTSP) - Neighbours Camera Scanner
- **Port 37777** (Dahua) - Camera identification
- **Port 8000** (Hikvision) - Camera identification

### Timeouts
- **Port Check:** 0.3-0.5 seconds
- **HTTP Request:** 1-2 seconds
- **RTSP Check:** 0.3 seconds
- **Optimized for speed**

### Detection Methods
1. **Title Extraction** - Parses HTML `<title>` tags
2. **Content Analysis** - Searches for camera signatures
3. **Server Headers** - Identifies server types
4. **Response Patterns** - Matches known camera patterns
5. **RTSP Protocol** - Detects RTSP streaming cameras
6. **Brand Detection** - Identifies Dahua and Hikvision models

---

## 📝 Requirements

### Python Packages
- **colorama** - For colored terminal output

### System Requirements
- **Python:** 3.7+
- **RAM:** 512MB minimum
- **Disk:** 10MB
- **Network:** Internet connection

---

## 🐛 Troubleshooting

### Issue: "colorama not found"
**Solution:**
```bash
pip install colorama
```

### Issue: "Traceroute command not found" (Linux/Termux)
**Solution:**
```bash
# For Termux
pkg install inetutils

# For Debian/Ubuntu
sudo apt install traceroute

# For Arch Linux
sudo pacman -S traceroute
```

### Issue: No cameras found
**Possible reasons:**
- No cameras in the IP range
- Firewall blocking connections
- Network timeout
- Cameras using different ports

**Try:**
- Scan your local network (192.168.x.x)
- Check if IPs are reachable
- Increase timeout values

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**W8SOJIB** (W8Team)

- GitHub: [@W8SOJIB](https://github.com/W8SOJIB)
- Repository: [W8CameraScannerV1](https://github.com/W8SOJIB/W8CameraScannerV1)

---

## ⭐ Support

If you find this tool useful, please:
- ⭐ **Star** this repository
- 🐛 **Report issues** on GitHub
- 🔀 **Fork** and contribute
- 📢 **Share** with others

---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing purposes only**. 

- ✅ Use on your own networks
- ✅ Use with proper authorization
- ❌ Do NOT use on unauthorized networks
- ❌ Do NOT use for illegal activities

**The author is not responsible for misuse of this tool.**

---

## 🚀 Future Updates

- [ ] IPv6 support
- [ ] Custom port scanning
- [ ] Export to CSV/JSON
- [ ] GUI version
- [ ] More camera signatures
- [ ] Proxy support
- [ ] Save credentials detection

---

## 📞 Contact

For questions, suggestions, or issues:
- **GitHub Issues:** [Report here](https://github.com/W8SOJIB/W8CameraScannerV1/issues)
- **Email:** Create an issue on GitHub

---

<div align="center">

**Made with ❤️ by W8Team**

⭐ **Star this repo if you find it useful!** ⭐

</div>

