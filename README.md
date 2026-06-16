# Air Canvas: Hand Gesture Controlled Drawing Pad 🎨👋

A real-time computer vision application that allows you to paint in the air using hand gestures captured via your webcam. Built with **Python**, **OpenCV**, **MediaPipe**, and **NumPy**, this project tracks hand landmarks to translate physical finger movements into digital brush strokes. It features a unique **dynamic color-cycling picker** and saves your artwork onto a separate clean canvas layer.

---

## 🚀 Key Features

- **Gesture-Driven Modes:**
  - **Selection Mode (Index + Middle Finger Up):** Move around the screen freely without drawing. Use this mode to hover over UI buttons.
  - **Drawing Mode (Only Index Finger Up):** Draws a smooth, continuous line following your fingertip.
- **Dynamic HSV Color Picker:** The "COLOR" button constantly cycles through the shifting rainbow spectrum. Hovering your hand over it locks in whichever color is active at that exact millisecond.
- **On-Screen Canvas Reset:** Hover over the "CLEAR" button to instantly wipe your canvas white and start a new sketch.
- **Dual-Window Monitoring:** - *Air Canvas - Live Feed:* Blends your drawing seamlessly on top of your webcam feed.
  - *Saved Artwork Canvas:* A pristine, isolated white canvas displaying only your artwork (perfect for saving later).

---

## 🛠️ Tech Stack & Concepts Used

- **Python 3.x**
- **MediaPipe (Hands module):** Configured with high tracking confidence (`0.85`) to process 21 3D hand landmarks in real-time.
- **OpenCV:** Handles frame resizing, mirroring, drawing pipelines, text rendering, and advanced **HSV-to-BGR color conversions**.
- **NumPy Matrix Manipulation:** Operates a $480 \times 640$ matrix for the white canvas and manages efficient coordinate tracking logic to prevent random line breaks.
- **Image Masking:** Utilizes inverse thresholding (`cv.THRESH_BINARY_INV`) and bitwise operations (`cv.bitwise_and`, `cv.bitwise_not`, `cv.add`) to map your drawing cleanly over the camera feed.

---

## 📋 Prerequisites & Installation

Follow these steps to get the project running locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Aikanticmaitra2980/vision4.git](https://github.com/Aikanticmaitra2980/vision4.git)
cd vision4
