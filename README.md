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
