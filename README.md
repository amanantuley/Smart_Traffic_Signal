
# 🚦 Smart Traffic Signal – Python Project

This repository contains my **Smart Traffic Signal System**, a Python-based project aimed at optimizing traffic flow using real-time/simulated data. It intelligently adjusts signal durations based on vehicle density to reduce congestion and improve city traffic management.

---

## 📁 Folder Structure

```
📁 static/                         # Static files (e.g., CSS, JS, images for UI if any)
📁 templates/                      # HTML templates (for Flask app interface)
📄 app.py                          # Main Flask application
📄 database.py                     # Handles database connections and schema
📄 database.db                     # SQLite database for user data/logs
📄 generate_verification_codes.py  # Utility script for creating codes (e.g., OTPs)
📄 temp.py                         # Temporary test script or experimental code
📄 test.py                         # Testing or unit test file
📄 test_time.py                    # Simulates signal timing behavior
📄 user_activity.xlsx              # Dataset or logs of simulated user activity
📄 LICENSE.md                      # License file (MIT or other)
📄 Project-Report.pdf              # Final project documentation/report
📄 SmartTrafficSignal_Aman_USC_UCT.pdf # Formal college submission document
📄 Smart_Traffic_Signal_SEM-4.pdf  # Academic report for SEM-4
📄 README.md                       # This file
```

---

## 🎯 Project Objective

To build an intelligent traffic light control system that uses real-time or simulated input to:

* Count vehicle density at intersections
* Dynamically alter traffic signal timings
* Reduce waiting time and congestion
* Log user/traffic activity for analysis

---

## ⚙️ Technologies & Libraries Used

* **Python 3.x** – Core language
* **Flask** – Backend web framework
* **SQLite** – Lightweight database
* **OpenCV** *(optional)* – For real-time camera-based vehicle detection
* **time, random, threading** – Used in simulation logic
* **Excel (XLSX)** – For logging and exporting user/traffic data

---

## 🚦 Key Features

✅ **Dynamic Signal Timing** – Signal times change based on traffic volume
✅ **Web-Based Dashboard** – UI built using Flask with HTML templates
✅ **User Activity Log** – All actions and durations are stored in a DB/XLSX
✅ **Traffic Simulation** – `test_time.py` mimics real-world traffic flow
✅ **Extensible Design** – Can be scaled for multiple intersections

---

## 🧪 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/amanantuley/smart-traffic-signal.git
   cd smart-traffic-signal
   ```

2. **Install dependencies**
   *(Create a `requirements.txt` if needed; otherwise manually install)*

   ```bash
   pip install flask pandas openpyxl
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. **Access the web interface**
   Navigate to `http://localhost:5000` in your browser.

---

## 📸 Screenshots

> *Place screenshots in a `screenshots/` folder and reference here once available.*

---

## 📄 Project Reports

* 📘 `Project-Report.pdf` – Final project documentation
* 📗 `SmartTrafficSignal_Aman_USC_UCT.pdf` – Official college submission
* 📙 `Smart_Traffic_Signal_SEM-4.pdf` – Academic report for semester-4

---

## 📬 Contact

* 👨‍💻 **Developer**: Aman Antuley
* 📧 **Email**: [amanantuley@gmail.com](mailto:amanantuley@gmail.com)
* 🔗 **LinkedIn**: [linkedin.com/in/amanantuley](https://www.linkedin.com/in/amanantuley)
* 🐙 **GitHub**: [github.com/amanantuley](https://github.com/amanantuley)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE.md). Feel free to use, modify, and distribute with attribution.

