import os
import shutil

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


UPLOAD_DIR = "media/uploads"
OUTPUT_DIR = "media/outputs"
MOTION_DIR = "media/motions"


def clear_folder(folder):

    os.makedirs(folder, exist_ok=True)

    for item in os.listdir(folder):

        item_path = os.path.join(folder, item)

        try:

            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)

            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        except Exception as e:

            print(f"Could not delete {item_path}: {e}")


def clear_all_media():

    print()
    print("Clearing old media files...")

    clear_folder(UPLOAD_DIR)
    clear_folder(OUTPUT_DIR)
    clear_folder(MOTION_DIR)

    print("Old media files cleared.")
    print()


def home(request):

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        video = request.FILES.get("video")

        if not video:
            return redirect("home")

        # ---------------------------------------------
        # Remove previous files before new upload
        # ---------------------------------------------

        clear_all_media()

        # ---------------------------------------------
        # Create upload folder
        # ---------------------------------------------

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        # ---------------------------------------------
        # Save uploaded video
        # ---------------------------------------------

        fs = FileSystemStorage(
            location=UPLOAD_DIR
        )

        filename = fs.save(
            video.name,
            video
        )

        uploaded_video_path = fs.path(
            filename
        )

        print("=" * 60)
        print("POSE ANIMATOR")
        print("=" * 60)

        print()
        print("Uploaded video:")
        print(uploaded_video_path)

        print()
        print("Processing video...")
        print()

        # ---------------------------------------------
        # Import processor here
        # ---------------------------------------------
        # This prevents processor from loading during
        # Django startup.
        # ---------------------------------------------

        from .video_processor import process_video_pose

        try:

            result = process_video_pose(
                uploaded_video_path
            )

        except Exception as e:

            print()
            print("PROCESSING ERROR:")
            print(str(e))
            print()

            return render(
                request,
                "index.html",
                {
                    "error": str(e)
                }
            )

        print()
        print("Generated:")
        print(result)

        print()
        print("Processing completed successfully.")
        print()

        # ---------------------------------------------
        # Convert path
        # ---------------------------------------------

        result = result.replace("\\", "/")

        if result.startswith("media/"):

            output_video = "/" + result

        else:

            output_video = "/media/outputs/" + os.path.basename(
                result
            )

        # ---------------------------------------------
        # Store output ONLY temporarily in session
        # ---------------------------------------------

        request.session["one_time_output"] = output_video

        request.session.modified = True

        # ---------------------------------------------
        # Redirect after POST
        # ---------------------------------------------

        return redirect("home")


    # =====================================================
    # GET
    # =====================================================

    if request.method == "GET":

        # ---------------------------------------------
        # Take output from session ONCE
        # ---------------------------------------------

        output_video = request.session.pop(
            "one_time_output",
            None
        )

        request.session.modified = True

        # ---------------------------------------------
        # If there is NO one-time output:
        #
        # This means:
        # - normal page opening
        # - page refresh
        # - browser revisiting page
        #
        # So clear everything.
        # ---------------------------------------------

        if output_video is None:

            clear_all_media()

        response = render(
            request,
            "index.html",
            {
                "output_video": output_video
            }
        )

        # ---------------------------------------------
        # Prevent browser from caching old page
        # ---------------------------------------------

        response["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, "
            "max-age=0"
        )

        response["Pragma"] = "no-cache"

        response["Expires"] = "0"

        return response


    return redirect("home")