
import cv2
import mediapipe as mp
import numpy as np
import os
import subprocess
import sys

# MediaPipe
mp_pose = mp.solutions.pose

# ------------------------------------------------------------
# Landmark smoother
# ------------------------------------------------------------
class LandmarkSmoother:

    def __init__(self, window_size=3):
        self.window_size = window_size
        self.history = []

    def smooth(self, landmarks):

        arr = np.array([
            [lm.x, lm.y, lm.z]
            for lm in landmarks
        ])

        self.history.append(arr)

        if len(self.history) > self.window_size:
            self.history.pop(0)

        smoothed_arr = np.mean(self.history, axis=0)

        smoothed_landmarks = []

        for i, orig_lm in enumerate(landmarks):

            new_lm = type(orig_lm)()

            new_lm.x = smoothed_arr[i][0]
            new_lm.y = smoothed_arr[i][1]
            new_lm.z = smoothed_arr[i][2]

            new_lm.visibility = orig_lm.visibility

            smoothed_landmarks.append(new_lm)

        return smoothed_landmarks


# ------------------------------------------------------------
# Draw animated character
# ------------------------------------------------------------
def draw_animated_character(
    canvas,
    landmarks,
    body_color=(19, 69, 139),
    end_circles_color=(255, 255, 255),
    thickness_ratio=0.025
):

    h, w = canvas.shape[:2]

    def pt(idx):

        lm = landmarks[idx]

        if lm.visibility < 0.3:
            return None

        return (
            int(lm.x * w),
            int(lm.y * h)
        )

    # --------------------------------------------------------
    # Head
    # --------------------------------------------------------

    nose = pt(mp_pose.PoseLandmark.NOSE)

    left_shoulder = pt(mp_pose.PoseLandmark.LEFT_SHOULDER)
    right_shoulder = pt(mp_pose.PoseLandmark.RIGHT_SHOULDER)

    if None not in [left_shoulder, right_shoulder]:

        shoulder_dist = np.linalg.norm(
            np.array(left_shoulder) - np.array(right_shoulder)
        )

        head_radius = max(int(shoulder_dist * 0.28), 18)

        thickness = max(
            6,
            int(min(w, h) * thickness_ratio)
        )

        mid_shoulder = (
            (left_shoulder[0] + right_shoulder[0]) // 2,
            (left_shoulder[1] + right_shoulder[1]) // 2
        )

        if nose:

            cv2.line(
                canvas,
                mid_shoulder,
                nose,
                body_color,
                thickness
            )

            cv2.circle(
                canvas,
                nose,
                head_radius,
                body_color,
                -1
            )

    # --------------------------------------------------------
    # Torso
    # --------------------------------------------------------

    left_hip = pt(mp_pose.PoseLandmark.LEFT_HIP)
    right_hip = pt(mp_pose.PoseLandmark.RIGHT_HIP)

    if None not in [
        left_shoulder,
        right_shoulder,
        left_hip,
        right_hip
    ]:

        torso_pts = np.array([
            left_shoulder,
            right_shoulder,
            right_hip,
            left_hip
        ], np.int32)

        cv2.fillPoly(canvas, [torso_pts], body_color)

    # --------------------------------------------------------
    # Arms & Legs
    # --------------------------------------------------------

    joints = {

        "left_elbow": pt(mp_pose.PoseLandmark.LEFT_ELBOW),
        "right_elbow": pt(mp_pose.PoseLandmark.RIGHT_ELBOW),

        "left_wrist": pt(mp_pose.PoseLandmark.LEFT_WRIST),
        "right_wrist": pt(mp_pose.PoseLandmark.RIGHT_WRIST),

        "left_knee": pt(mp_pose.PoseLandmark.LEFT_KNEE),
        "right_knee": pt(mp_pose.PoseLandmark.RIGHT_KNEE),

        "left_ankle": pt(mp_pose.PoseLandmark.LEFT_ANKLE),
        "right_ankle": pt(mp_pose.PoseLandmark.RIGHT_ANKLE),
    }

    thickness = max(
        6,
        int(min(w, h) * thickness_ratio)
    )

    # Arms

    if left_shoulder and joints["left_elbow"]:
        cv2.line(
            canvas,
            left_shoulder,
            joints["left_elbow"],
            body_color,
            thickness
        )

    if joints["left_elbow"] and joints["left_wrist"]:
        cv2.line(
            canvas,
            joints["left_elbow"],
            joints["left_wrist"],
            body_color,
            thickness
        )

    if right_shoulder and joints["right_elbow"]:
        cv2.line(
            canvas,
            right_shoulder,
            joints["right_elbow"],
            body_color,
            thickness
        )

    if joints["right_elbow"] and joints["right_wrist"]:
        cv2.line(
            canvas,
            joints["right_elbow"],
            joints["right_wrist"],
            body_color,
            thickness
        )

    # Legs

    if left_hip and joints["left_knee"]:
        cv2.line(
            canvas,
            left_hip,
            joints["left_knee"],
            body_color,
            thickness
        )

    if joints["left_knee"] and joints["left_ankle"]:
        cv2.line(
            canvas,
            joints["left_knee"],
            joints["left_ankle"],
            body_color,
            thickness
        )

    if right_hip and joints["right_knee"]:
        cv2.line(
            canvas,
            right_hip,
            joints["right_knee"],
            body_color,
            thickness
        )

    if joints["right_knee"] and joints["right_ankle"]:
        cv2.line(
            canvas,
            joints["right_knee"],
            joints["right_ankle"],
            body_color,
            thickness
        )

    # --------------------------------------------------------
    # White circles
    # --------------------------------------------------------

    end_radius = max(
        12,
        int(thickness * 1.5)
    )

    for key in [
        "left_wrist",
        "right_wrist",
        "left_ankle",
        "right_ankle"
    ]:

        if joints[key]:

            cv2.circle(
                canvas,
                joints[key],
                end_radius,
                end_circles_color,
                -1
            )


# ------------------------------------------------------------
# FFmpeg check
# ------------------------------------------------------------
def is_ffmpeg_available():

    try:

        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )

        return True

    except:
        return False


# ------------------------------------------------------------
# Main processor
# ------------------------------------------------------------
def process_video_pose(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # --------------------------------------------------------
    # Create output folders
    # --------------------------------------------------------

    os.makedirs("media/outputs", exist_ok=True)

    base = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    temp_video = os.path.join(
        "media",
        "outputs",
        f"temp_{base}.mp4"
    )

    final_video = os.path.join(
        "media",
        "outputs",
        f"output_{base}.mp4"
    )

    # --------------------------------------------------------
    # Video writer
    # --------------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    writer = cv2.VideoWriter(
        temp_video,
        fourcc,
        fps,
        (width, height)
    )

    smoother = LandmarkSmoother()

    last_valid_landmarks = None

    # --------------------------------------------------------
    # MediaPipe Pose
    # --------------------------------------------------------

    with mp_pose.Pose(

        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5

    ) as pose:

        frame_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = pose.process(rgb)

            canvas = np.zeros(
                (height, width, 3),
                dtype=np.uint8
            )

            if results.pose_landmarks:

                smoothed = smoother.smooth(
                    results.pose_landmarks.landmark
                )

                draw_animated_character(
                    canvas,
                    smoothed
                )

                last_valid_landmarks = smoothed

            elif last_valid_landmarks is not None:

                draw_animated_character(
                    canvas,
                    last_valid_landmarks
                )

            writer.write(canvas)

            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames")

    cap.release()
    writer.release()

    print("Animation video saved:", temp_video)

    # --------------------------------------------------------
    # FFmpeg audio merge
    # --------------------------------------------------------

    if not is_ffmpeg_available():

        print("FFmpeg not installed")

        return temp_video

    try:

        cmd = [

            "ffmpeg",
            "-y",

            "-i",
            temp_video,

            "-i",
            video_path,

            "-c:v",
            "libx264",

            "-preset",
            "fast",

            "-c:a",
            "aac",

            "-map",
            "0:v:0",

            "-map",
            "1:a:0",

            "-shortest",

            final_video
        ]

        subprocess.run(
            cmd,
            capture_output=True,
            check=True
        )

        print("Final video saved:", final_video)

        os.remove(temp_video)

        return final_video

    except subprocess.CalledProcessError:

        print("Audio merge failed")

        return temp_video


# ------------------------------------------------------------
# Run directly
# ------------------------------------------------------------
if __name__ == "__main__":

    input_video = "input.mp4"

    if not os.path.exists(input_video):

        print("Input video not found")
        sys.exit(1)

    output = process_video_pose(input_video)

    print("Done:", output)

