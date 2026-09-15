import json
import os

MOTION_DIR = os.path.join(
    "media",
    "motions"
)

os.makedirs(
    MOTION_DIR,
    exist_ok=True
)


def save_pose_frame(landmarks, frame_no):

    data = []

    for lm in landmarks:

        if isinstance(lm, dict):

            data.append({
                "x": float(lm.get("x", 0.0)),
                "y": float(lm.get("y", 0.0)),
                "z": float(lm.get("z", 0.0)),
                "visibility": float(
                    lm.get("visibility", 1.0)
                )
            })

        else:

            data.append({
                "x": float(lm.x),
                "y": float(lm.y),
                "z": float(lm.z),
                "visibility": float(
                    getattr(lm, "visibility", 1.0)
                )
            })

    filename = os.path.join(
        MOTION_DIR,
        f"{frame_no:06d}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )