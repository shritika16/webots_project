# 🤖 Webots YouBot: Procedural Dataset Generator

This repository contains a **Webots Supervisor Controller** designed for the KUKA YouBot. It automates the creation of a cluttered environment and collects synchronized image data for computer vision tasks.

## 🌟 Overview
The controller transforms a standard simulation into a data collection powerhouse by:
* **Dynamic Spawning:** Generating 180 random obstacles (Bottles, Knives, Spoons).
* **Environment Shifting:** Randomizing lighting and fog levels to prevent model overfitting.
* **Automated Labeling:** Saving high-quality `.jpg` frames directly to a local dataset folder.

---

## 🛠️ Requirements

| Requirement | Version / Detail |
| :--- | :--- |
| **Simulator** | Webots R2023b or later |
| **Language** | Python 3.8+ |
| **Libraries** | `numpy`, `opencv-python` |
| **Robot** | KUKA YouBot (Supervisor enabled) |

---

## 🚀 Setup & Installation

### 1. Webots Scene Tree Configuration
Before running the controller, ensure the following nodes are named correctly in the **Scene Tree** (using the `DEF` field):

* **Robot:** `DEF YOUBOT` (Set the `supervisor` field to `TRUE`)
* **Light:** `DEF light` (PointLight or DirectionalLight)
* **Fog:** `DEF fog` (Fog node)
* **Camera:** `DEF camera` (Attached to the YouBot)

> **⚠️ Critical Step:** You must add `WaterBottle`, `Knife`, and `Spoon` to the `importableExternProto` list in the **WorldInfo** node or the supervisor will fail to spawn them.

### 2. File Path Setup
Update the `data_folder` variable in `shri_controller.py` to match your local machine:
```python
data_folder = "/home/ml/project/webots/datasets/run1/"# webots_project

📸 Controller Logic
🟢 Environment Initialization
The script starts by clearing a 20x20 meter area and spawning 60 instances of three different objects.

🟡 Motion & Vision
The YouBot is configured for constant forward motion using its four-wheeled omnidirectional base:

Wheel Velocity: 0.4 * MAX_SPEED

Camera Resolution: Managed via camera.getWidth() and camera.getHeight()

🔴 Data Augmentation (On-the-fly)
Every 500 steps, the supervisor modifies the world state:

Luminosity: np.random.rand(1) (Simulates different times of day)

Fog Visibility: np.random.rand(1)*10 + 1 (Simulates weather/depth occlusion)

📂 Dataset Structure
Once the simulation runs, your specified folder will populate as follows:

Plaintext

run1/
├── 0.jpg
├── 10.jpg
├── 20.jpg
└── ...
💻 Technical Snippet: Image Processing
The controller converts the raw Webots BGRA buffer into an OpenCV-friendly format:

Python

raw_image = camera.getImage()
image = np.frombuffer(raw_image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
frame = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
Developed by: Shri

Project: AI Robotics Dataset Generation


---

### Tips for your README:
1.  **Image Tags:** I added a placeholder ``. Once you run your simulation, take a screenshot of the spawned bottles/knives and replace that line with `![Environment](path/to/your/screenshot.png)`.
2.  **Pathing:** If you plan to share this on GitHub, change the `data_folder` in the text to a generic path like `./dataset/` so others aren't confused by your local Linux path.
