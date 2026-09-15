# 🎭 PoseAnimator

### 🎥 AI-Based Video Pose Detection & Character Animation

**PoseAnimator** is a web-based application that processes uploaded videos using **MediaPipe Pose** and **OpenCV** to detect human body movements and generate an animated character based on the detected pose data.

The project is designed to make **video-based pose analysis and animation** easier through a simple web interface.

---

## 🚀 Project Overview

Creating character animations manually can be time-consuming and difficult for beginners.

**PoseAnimator** provides a simple workflow where a user can upload a video and the application automatically:

```text
Upload Video
      ↓
Video Processing
      ↓
Human Pose Detection
      ↓
Pose Landmark Extraction
      ↓
Motion Data Storage
      ↓
Animated Character Generation
      ↓
Processed Video Output
```

The goal of this project is to convert human movement from a video into usable pose and motion information.

---

## ✨ Features

* 🎥 Video upload support
* 🧍 Human pose detection
* 🤖 AI-based pose processing
* 📍 Body landmark detection
* 🎞️ Frame-by-frame video processing
* 🦴 Skeleton-based character animation
* 💾 Pose landmark data storage
* 📂 Motion JSON generation
* 🎬 Processed video generation
* 🔊 Audio preservation using FFmpeg
* 🌐 Django web interface
* 🔄 Automatic media cleanup
* 📱 Simple and beginner-friendly interface

---

## 🧠 How It Works

### 1️⃣ Upload a Video

The user uploads a video through the web interface.

Supported video formats depend on the installed OpenCV and FFmpeg configuration.

Common formats include:

```text
MP4
AVI
MOV
MKV
WEBM
```

---

### 2️⃣ Pose Detection

The uploaded video is processed frame by frame using **MediaPipe Pose**.

MediaPipe detects important body landmarks such as:

* Nose
* Shoulders
* Elbows
* Wrists
* Hips
* Knees
* Ankles
* Feet

---

### 3️⃣ Landmark Processing

For every detected frame, the application extracts pose coordinates.

Each landmark contains:

```text
X coordinate
Y coordinate
Z coordinate
```

These values are used to understand the movement of the human body.

---

### 4️⃣ Motion Data Storage

The extracted pose information can be stored as JSON files.

Example:

```text
media/
└── motions/
    ├── 000001.json
    ├── 000002.json
    ├── 000003.json
    └── ...
```

Each JSON file represents the pose information of an individual video frame.

---

### 5️⃣ Character Animation

The detected body movements are converted into a simplified animated character/skeleton representation.

This allows the application to visually represent the movement detected from the original video.

---

### 6️⃣ Video Output

After processing, the application generates a new video containing the animated pose representation.

The generated output is stored temporarily inside:

```text
media/outputs/
```

---

## 🛠️ Technologies Used

### Programming Language

* 🐍 Python

### Web Framework

* Django

### Computer Vision

* OpenCV

### Pose Detection

* MediaPipe Pose

### Numerical Processing

* NumPy

### Video Processing

* FFmpeg
* OpenCV VideoWriter

### Database

* SQLite

---

## 📁 Project Structure

```text
PoseAnimator/
│
├── app/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── pose_storage.py
│   ├── tests.py
│   ├── urls.py
│   ├── video_processor.py
│   └── views.py
│
├── PoseAnimator/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── index.html
│
├── media/
│   ├── uploads/
│   ├── outputs/
│   └── motions/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💻 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/shekinapilla4809/PoseAnimator.git
```

---

### 2️⃣ Open the Project Folder

```bash
cd PoseAnimator
```

---

### 3️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

---

### 4️⃣ Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### 5️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 6️⃣ Apply Django Migrations

```bash
python manage.py migrate
```

---

### 7️⃣ Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

Open the address in your web browser.

---

## 🎬 Usage

### Step 1

Open the PoseAnimator website.

### Step 2

Upload a video containing a visible human body.

### Step 3

Start the pose processing.

### Step 4

The application detects body landmarks frame by frame.

### Step 5

The pose information is converted into an animated character representation.

### Step 6

The processed video is generated and displayed to the user.

---

## 📊 Pose Landmark Data

PoseAnimator extracts 3D landmark coordinates from the detected body pose.

Example JSON structure:

```json
[
    {
        "x": 0.52,
        "y": 0.31,
        "z": -0.12
    },
    {
        "x": 0.48,
        "y": 0.42,
        "z": -0.08
    }
]
```

The coordinates can be used for further animation and motion-processing workflows.

---

## 🎯 Problem Statement

Traditional character animation requires manual keyframing and animation knowledge.

Beginners may find it difficult to create realistic body movements manually.

There is a need for a simple system that can extract human movement from ordinary videos and convert it into usable animation data.

---

## 💡 Proposed Solution

**PoseAnimator** uses computer vision and pose estimation to automatically detect human body movements from video.

The system converts the detected movements into pose information and uses that information to generate an animated character representation.

This reduces the amount of manual animation work required.

---

## 🌟 Key Benefits

* ⏱️ Reduces manual animation effort
* 🤖 Uses AI-based pose detection
* 🎥 Works directly with video input
* 📊 Produces structured pose data
* 🎨 Provides visual character animation
* 🧑‍💻 Beginner-friendly workflow
* 🔧 Can be extended for advanced animation systems

---

## 🔮 Future Enhancements

Future versions of PoseAnimator may include:

* 🧍 Realistic 3D character animation
* 🦴 Automatic skeleton/rig detection
* 🎭 Support for custom 3D characters
* 📦 GLB / GLTF / FBX character support
* 🎬 Mixamo animation support
* 🔄 Automatic animation retargeting
* 🦴 Advanced bone mapping
* 🎨 Character texture preservation
* 🖼️ Multiple texture support
* 🎞️ Improved animation export
* 🎥 MP4 animation export
* 🎙️ Audio synchronization
* 📐 Custom keyframe editing
* ⏱️ Timeline-based animation editing
* 📹 Improved motion extraction
* 🌐 Cloud deployment
* 🤖 AI-assisted animation generation

---

## ⚙️ Requirements

The project currently uses:

```text
Python
Django
OpenCV
MediaPipe
NumPy
FFmpeg
```

Python dependencies are available in:

```text
requirements.txt
```

---

## 📦 FFmpeg

PoseAnimator uses **FFmpeg** for video/audio processing when available.

FFmpeg must be installed separately because it is not a Python package.

After installing FFmpeg, verify it using:

```bash
ffmpeg -version
```

If FFmpeg is available in the system PATH, PoseAnimator can use it for audio processing.

---

## 🔐 Security & Git

The following files and folders are intentionally excluded from Git:

```text
venv/
db.sqlite3
media/uploads/
media/outputs/
media/motions/
.env
```

This prevents large generated files, local database files, virtual environments, and sensitive environment variables from being uploaded to GitHub.

---

## 🧪 Development

To start development:

```bash
python manage.py runserver
```

For checking Django configuration:

```bash
python manage.py check
```

For applying database migrations:

```bash
python manage.py migrate
```

---

## 📌 Project Status

🚧 **Active Development**

The current version focuses on:

```text
Video Upload
      ↓
Pose Detection
      ↓
Pose Processing
      ↓
Character/Skeleton Animation
      ↓
Video Output
```

More advanced 3D character and animation-retargeting features are planned for future versions.

---

## 👩‍💻 Developer

### Shekina Pilla

**B.Tech – Computer Science & Engineering (Data Science)**

### Areas of Interest

* 🤖 Artificial Intelligence
* 🎨 3D Animation
* 🎥 Motion Capture
* 💻 Software Development
* 📊 Data Science
* 🧠 Computer Vision

---

## 🙏 Acknowledgements

This project uses open-source technologies and libraries including:

* Python
* Django
* OpenCV
* MediaPipe
* NumPy
* FFmpeg

---

## 📜 License

This project is developed for **educational, research, and development purposes**.

---

## ⭐ Support

If you find **PoseAnimator** useful or interesting, please consider giving the repository a ⭐ **Star**.

Thank you for checking out **PoseAnimator**! 🎭🎥🤖
