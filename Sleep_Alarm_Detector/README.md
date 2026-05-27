````md
# 😴 Sleep Alarm Detector

A real-time sleep detection system using **OpenCV** and **MediaPipe** that monitors eye closure through your webcam.  
If your eyes stay closed for too long, the system triggers an alarm and displays a red warning overlay.

---

## Features

- Real-time face and eye tracking
- Eye Aspect Ratio (EAR) based detection
- Alarm sound on prolonged eye closure
- Live status overlay and face box
- Simple and lightweight

---

## Requirements

- Python 3.8+
- Webcam

Install dependencies:

```bash
pip install mediapipe==0.10.14 opencv-python numpy pygame
````

---

## Setup

Place your alarm sound file (`.mp3` or `.wav`) in the project folder and update:

```python
ALARM_SOUND_FILE = r"your_alarm.mp3"
```

You can also adjust detection sensitivity in `sleep_alarm.py`:

| Variable             | Default | Description                  |
| -------------------- | ------- | ---------------------------- |
| `EAR_THRESHOLD`      | `0.22`  | Lower value = less sensitive |
| `EYE_CLOSED_SECONDS` | `2.5`   | Time before alarm triggers   |

---

## Run

```bash
python sleep_alarm.py
```

Press **Q** to quit.

---

## How It Works

* Uses **MediaPipe Face Mesh** for facial landmark tracking
* Calculates **Eye Aspect Ratio (EAR)** for both eyes
* Starts a timer when eyes appear closed
* Triggers alarm if eyes remain closed too long

---

## Troubleshooting

| Problem                 | Fix                                                   |
| ----------------------- | ----------------------------------------------------- |
| Camera not opening      | Change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)` |
| Alarm not playing       | Check `ALARM_SOUND_FILE` path                         |
| Too many false alarms   | Increase `EAR_THRESHOLD`                              |
| Alarm triggers too fast | Increase `EYE_CLOSED_SECONDS`                         |

---

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame

```
```
