# 🤖 YouBot Webots Simulation Controller

![Webots](https://img.shields.io/badge/Webots-R2023b-blue?style=for-the-badge&logo=webots)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

> A **Webots Supervisor-based controller** for the **KUKA YouBot** robot. Dynamically spawns randomized household objects into the scene, controls all 4 wheels, varies lighting and fog conditions, and streams camera frames to disk for dataset collection.

---

## 📸 Simulation Preview

> *(Sample screenshot of YouBot navigating the randomized scene in Webots)*

![YouBot in Webots](https://raw.githubusercontent.com/cyberbotics/webots/released/docs/guide/images/robots/youbot/model.png)

> **Scene**: YouBot moves forward through a world populated with randomly placed `WaterBottle`, `Knife`, and `Spoon` objects, under dynamically varying lighting and fog.

---

## 📁 Project Structure

```
webots_youbot_supervisor/
├── controllers/
│   └── youbot_supervisor/
│       └── youbot_supervisor.py   # Main controller (this file)
├── worlds/
│   └── youbot_scene.wbt           # Webots world file
├── datasets/
│   └── run1/                      # Captured camera images (JPEG)
│       ├── 0.jpg
│       ├── 10.jpg
│       └── ...
└── README.md
```

---

## ⚙️ Features

| Feature | Description |
|---|---|
| 🌐 **Supervisor API** | Uses `Supervisor` (not just `Robot`) to dynamically modify the scene at runtime |
| 📦 **Random Object Spawning** | Spawns 60× each of `WaterBottle`, `Knife`, `Spoon` (180 objects total) at random positions |
| 💡 **Dynamic Lighting** | Randomly adjusts scene `luminosity` every 500 steps |
| 🌫️ **Dynamic Fog** | Randomly adjusts `visibilityRange` of the fog node every 500 steps |
| 🎥 **Camera Streaming** | Captures live camera feed from the robot; displays in OpenCV window |
| 💾 **Dataset Collection** | Saves a JPEG image every 10 simulation steps to `datasets/run1/` |
| 🔧 **4-Wheel Drive** | Controls all 4 YouBot wheels in velocity mode |

---

## 🛠️ Requirements

### Software

```txt
Python >= 3.8
Webots R2023b (or compatible)
OpenCV (cv2) >= 4.5
NumPy >= 1.21
```

### Install Python dependencies

```bash
pip install opencv-python numpy
```

> **Note:** `controller` module is provided by Webots automatically — no `pip install` needed.

---

## 🚀 Getting Started

### 1. Clone / Set Up Your Webots World

Open your `.wbt` world file in Webots and ensure the following **DEF nodes** exist:

```vrml
DEF light PointLight { luminosity 1.0 }
DEF fog Fog { visibilityRange 100.0 }
```

Your YouBot robot node must have the following devices:
- `wheel1`, `wheel2`, `wheel3`, `wheel4` — HingeJoint motors
- `camera` — Camera device

### 2. Configure the Controller

In Webots, assign the controller to your robot node:

```
Controller: youbot_supervisor
```

### 3. Set the Dataset Output Path

Edit this line in the script to point to your desired output folder:

```python
# Line ~59 in youbot_supervisor.py
data_folder = "/home/ml/project/webots/datasets/run1/"
```

> ⚠️ Make sure the directory exists before running:
> ```bash
> mkdir -p /home/ml/project/webots/datasets/run1/
> ```

### 4. Run the Simulation

Hit **Play** in Webots. The controller will:
1. Spawn 180 random objects across a 20×20 unit grid
2. Set initial luminosity to `0.1` and fog to `100.0`
3. Start driving all 4 wheels at **40% of max speed**
4. Stream camera frames via OpenCV
5. Save frames every **10 steps**

---

## 🧠 Controller Breakdown

### Supervisor Initialization

```python
from controller import Supervisor
sp = Supervisor()
root_node = sp.getRoot()
children_field = root_node.getField('children')
```

> `Supervisor` extends `Robot` and grants full scene-graph access, allowing node creation, deletion, and field manipulation.

---

### Dynamic Object Spawning

```python
scale = 20
for i in range(60):
    d = scale * np.random.rand(2) - scale / 2

    obj_string = f'DEF WB_{i} WaterBottle {{ translation {d[0]} {d[1]} 0.0 }}'
    children_field.importMFNodeFromString(-1, obj_string)

    # Same for Knife and Spoon...
```

| Object | DEF Prefix | Count |
|---|---|---|
| 💧 WaterBottle | `WB_i` | 60 |
| 🔪 Knife | `KN_i` | 60 |
| 🥄 Spoon | `SP_i` | 60 |

Positions are sampled uniformly from `[-10, +10]` in X and Y (Z = 0.0).

---

### Wheel Control (YouBot 4WD)

```python
MAX_SPEED = 6.28  # rad/s (≈ 1 full revolution/sec)

w1 = sp.getDevice('wheel1')  # Right Front
w2 = sp.getDevice('wheel2')  # Left Front
w3 = sp.getDevice('wheel3')  # Right Rear
w4 = sp.getDevice('wheel4')  # Left Rear

# Infinite position = velocity control mode
w1.setPosition(float('inf'))
w2.setPosition(float('inf'))
w3.setPosition(float('inf'))
w4.setPosition(float('inf'))

w1.setVelocity( 0.4 * MAX_SPEED)  # RF → forward
w2.setVelocity(-0.4 * MAX_SPEED)  # LF → forward (inverted axis)
w3.setVelocity( 0.4 * MAX_SPEED)  # RR → forward
w4.setVelocity(-0.4 * MAX_SPEED)  # LR → forward (inverted axis)
```

> Left-side wheels have **inverted axes** on the YouBot, so negative velocity = forward motion.

---

### Camera & Dataset Collection

```python
camera = sp.getDevice('camera')
camera.enable(timestep)

raw_image = camera.getImage()
image = np.frombuffer(raw_image, np.uint8).reshape(
    (camera.getHeight(), camera.getWidth(), 4)
)
frame = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

if cnt % 10 == 0:
    cv2.imwrite(f"{data_folder}{cnt}.jpg", frame)
```

> Camera output is in **BGRA** format (Webots default). Converted to **BGR** for OpenCV compatibility.

---

### Dynamic Environment Changes (Every 500 Steps)

```python
if cnt % 500 == 0:
    lmval = np.random.rand(1)               # luminosity in [0, 1]
    lum_field.setSFFloat(float(lmval))

    lmval_fog = np.random.rand(1) * 10 + 1  # fog range in [1, 11]
    vis_fog.setSFFloat(float(lmval_fog))
```

This creates **domain randomization** — useful for training robust vision models.

---

## 📊 Dataset Output

| Property | Value |
|---|---|
| Format | JPEG |
| Naming | `{step_count}.jpg` (multiples of 10) |
| Color Space | BGR |
| Resolution | Determined by Webots camera settings |
| Frequency | Every 10 simulation steps |

---

## 🔬 Domain Randomization

The controller implements two forms of **domain randomization** to improve dataset diversity:

```
Luminosity  →  Random in [0.0, 1.0]     (every 500 steps)
Fog Range   →  Random in [1.0, 11.0]    (every 500 steps)
Object Pos  →  Random in [-10, +10] XY  (once at startup)
```

This is commonly used to improve **sim-to-real transfer** in robotics and computer vision tasks.

---

## ⚠️ Common Issues

| Issue | Fix |
|---|---|
| `No device named 'wheel1'` | Check your YouBot PROTO — device names may differ (e.g. `left wheel motor`) |
| `DEF light not found` | Add `DEF light PointLight {}` manually in your `.wbt` world |
| `DEF fog not found` | Add `DEF fog Fog { visibilityRange 100 }` to your world |
| OpenCV window not showing | Ensure you're not running headless; `cv2.imshow` requires a display |
| Images not saving | Verify `data_folder` path exists and has write permissions |
| Controller not found | Ensure folder name matches the controller name in Webots |

---

## 🗺️ Roadmap

- [ ] Add LiDAR sensor integration
- [ ] Implement obstacle avoidance logic
- [ ] Support additional object types (chairs, tables, cups)
- [ ] Export dataset in COCO/YOLO annotation format
- [ ] Add ROS2 bridge support

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Cyberbotics Webots](https://cyberbotics.com/) — Open-source robot simulator
- [KUKA YouBot](https://www.youbot-store.com/) — Mobile manipulator platform
- [OpenCV](https://opencv.org/) — Computer vision library
- [NumPy](https://numpy.org/) — Numerical computing

---

*Made with ❤️ for robotics research and simulation-based dataset collection.*
