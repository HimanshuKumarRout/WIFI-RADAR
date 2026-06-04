
<div align="center">
  <h1>📡 WiFi Radar Tracker</h1>
  <p>
    <strong>A real-time WiFi radar visualization tool built with Python and Tkinter for Windows systems.</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white" />
    <img src="https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge" />
    <img src="https://img.shields.io/badge/Windows-Only-0078D6?style=for-the-badge&amp;logo=windows&amp;logoColor=white" />
    <img src="https://img.shields.io/badge/WiFi-Radar-success?style=for-the-badge" />
  </p>
</div>

<br />

## 🌟 Overview

**WiFi Radar Tracker** is a desktop-based Python application that scans nearby WiFi networks and visualizes them on a radar-style graphical interface.

Using the Windows `netsh` command, the application continuously detects nearby wireless networks and displays their signal strengths dynamically in a clean Tkinter GUI.

This project is ideal for:
- 📡 Network visualization practice  
- 🖥️ Python GUI learning  
- 🔍 WiFi signal monitoring concepts  
- ⚡ Real-time background scanning systems  

---

## 🚀 Key Features

- 📶 **WiFi Network Scanning** – Detect nearby wireless networks using `netsh`
- 🎯 **Radar Visualization** – Represent networks as radar points
- 📊 **Signal Strength Display** – Show SSID and signal quality
- 🔄 **Continuous Background Updates** – Auto-refresh nearby network data
- 🖥️ **Tkinter GUI Interface** – Interactive radar-style application
- ⚡ **Lightweight & Fast** – Minimal dependencies required

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** (GUI Framework)
- **Windows netsh Command**
- **Threading / Background Processing**

---

## 📁 Project Structure

```text
WIFI-RADAR-TRACKER/
├── init.py                 # Startup script
├── Radar/
│   ├── __init__.py         # Radar package marker
│   ├── main.py             # Radar GUI & visualization logic
│   └── scanner.py          # WiFi scanning & parsing logic
├── .gitignore              # Git ignore rules
└── README.md
````

---

## ⚙️ Requirements

* Python 3.x
* Windows Operating System
* WiFi Adapter Enabled
* Tkinter (usually included with Python)

---

## ▶️ Running the Project

### 1️⃣ Clone the Repository

```bash id="hjv3m2"
git clone https://github.com/HimanshuKumarRout/WIFI-RADAR.git
cd WIFI-RADAR
```

---

### 2️⃣ Run the Full Application

```powershell id="lhq7u1"
python init.py
```

This will:

* Launch the radar GUI
* Continuously scan nearby WiFi networks
* Run `Radar/scanner.py` after the GUI closes

---

### 3️⃣ Run Only the GUI

```powershell id="5a8o2f"
python Radar\main.py
```

---

### 4️⃣ Run Only the Scanner

```powershell id="0f6jpw"
python Radar\scanner.py
```

---

## 🖥️ Application Highlights

* 📡 Real-time wireless network monitoring
* 🎨 Animated radar-style visualization
* 📶 Dynamic signal strength updates
* ⚙️ Background scanning architecture
* 🖥️ Lightweight desktop GUI experience

---

## ⚠️ Important Notes

This project is designed specifically for **Windows systems** because it relies on:

```powershell id="yx9vlr"
netsh wlan show networks mode=bssid
```

Ensure:

* WiFi is enabled
* Your device supports wireless scanning
* Python includes Tkinter support

If `tkinter` is missing:

* Reinstall Python with Tkinter enabled
* Or install it through your Python distribution/package manager

---

## 🔮 Future Enhancements

* 🌐 Linux & macOS support
* 📊 Real-time signal graphs
* 📍 WiFi heatmap generation
* 🎞️ Advanced radar animations
* 🔔 Alerts for network changes

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch (`feature/new-feature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 👨‍💻 Author

**Himanshu Kumar Rout**

* GitHub: [https://github.com/HimanshuKumarRout](https://github.com/HimanshuKumarRout)
* Email: [himanshurout136@gmail.com](mailto:himanshurout136@gmail.com)

---

## ⭐ Support

If you like this project, please **star ⭐ the repository** and share it!

---

<p align="center">Built with 📡 using Python & Tkinter</p>
```
