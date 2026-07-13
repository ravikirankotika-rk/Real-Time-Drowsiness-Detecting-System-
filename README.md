# 🚗 Real-Time Driver Drowsiness Detection System

## 📌 Overview

The **Real-Time Driver Drowsiness Detection System** is an AI-based safety application that monitors a driver's alertness using computer vision and facial landmark detection. The system detects signs of drowsiness such as **eye closure**, **yawning**, and **head tilt**, and communicates with an **ESP32** microcontroller to trigger safety actions.

This project is developed using **Python**, **OpenCV**, **dlib**, and **ESP32** to help reduce road accidents caused by driver fatigue.

---

## ✨ Features

* 👁️ Eye closure detection using Eye Aspect Ratio (EAR)
* 😮 Yawning detection using Mouth Aspect Ratio (MAR)
* 🧑 Head tilt detection using facial landmarks
* 📷 Real-time webcam monitoring
* 🔄 Stable alert mechanism to reduce false alarms
* 📡 Serial communication with ESP32
* 🚨 Automatic drowsiness alert
* 🟢 Live driver status display (SAFE / DANGER)

---

## 🛠️ Technologies Used

### Programming Language

* Python 3.x

### Libraries

* OpenCV
* dlib
* NumPy
* imutils
* pySerial

### Hardware

* ESP32 Development Board
* USB Webcam (or Laptop Camera)
* Buzzer (Optional)
* DC Motor (Optional)
* LCD Display (Optional)

---

## 📂 Project Structure

```
Driver-Drowsiness-Detection/
│
├── main.py
├── EAR.py
├── MAR.py
├── HeadPose.py
├── requirements.txt
├── README.md
│
└── dlib_shape_predictor/
    └── shape_predictor_68_face_landmarks.dat
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Driver-Drowsiness-Detection.git

cd Driver-Drowsiness-Detection
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install opencv-python dlib imutils numpy pyserial scipy
```

---

## 📥 Download Facial Landmark Model

Download the following file:

```
shape_predictor_68_face_landmarks.dat
```

Place it inside:

```
dlib_shape_predictor/
```

---

## 🔌 ESP32 Configuration

Update the serial port in the code if needed:

```python
esp32 = serial.Serial('COM6', 115200, timeout=1)
```

Replace **COM6** with your ESP32 port.

Examples:

Windows

```
COM3
COM5
COM6
```

Linux

```
/dev/ttyUSB0
```

---

## ▶️ Run the Project

```bash
python main.py
```

Press **Q** to quit.

---

## 🧠 Detection Methods

### Eye Closure Detection

Uses **Eye Aspect Ratio (EAR)** to detect closed eyes.

Threshold:

```
EAR < 0.25
```

---

### Yawning Detection

Uses **Mouth Aspect Ratio (MAR)**.

Threshold:

```
MAR > 0.79
```

---

### Head Tilt Detection

Uses facial landmark estimation and head pose calculation.

Threshold:

```
Head Tilt > 30°
```

---

## 🚦 Alert Logic

The system minimizes false alarms by using frame-based stability logic.

* Eye closure must persist for multiple frames.
* Danger state is confirmed after continuous dangerous frames.
* Safe state is restored only after continuous safe frames.

This provides smoother and more reliable detection.

---

## 📺 Output

During execution the application displays:

* Driver face detection
* Eye status
* Yawning detection
* Head tilt detection
* Driver status (SAFE / DANGER)
* Drowsiness warning message

---

## 📡 ESP32 Communication

The Python application sends status messages to the ESP32 through Serial Communication.

Possible messages:

```
SAFE
```

```
DANGER
```

The ESP32 can use these messages to:

* Activate a buzzer
* Stop a motor
* Display a warning on an LCD
* Trigger additional IoT devices

---

## 📈 Future Improvements

* Blink rate analysis
* PERCLOS calculation
* Mobile application integration
* GPS location sharing
* Firebase cloud logging
* Telegram alert notifications
* Night vision support
* Deep Learning (CNN/MediaPipe) based detection

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

## 📄 License

This project is intended for educational and research purposes.

---

## 👨‍💻 Author

**Ravi Kiran**

Electronics and Communication Engineering Graduate

Interested in:

* Computer Vision
* Artificial Intelligence
* IoT
* Embedded Systems
* Java Full Stack Development

---

⭐ If you found this project useful, please consider giving it a **Star** on GitHub.

You can also add screenshots, a demo GIF, or a short demo video to the repository to make it more attractive for recruiters and employers.
