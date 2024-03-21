import cv2
import requests
from io import BytesIO
import json
import time
import os


def compare_data(predicted_field, comparision_field, key):
    # TODO: remove this if video data is fixed
    if (key == "Systolic_mmHg" or key == "Diastolic_mmHg") and comparision_field[
        key
    ] is None:
        return True

    if predicted_field[key] is None and comparision_field[key] is None:
        return True
    if str(predicted_field[key]) == str(comparision_field[key]):
        return True
    return False


def get_accuracy_details(predicted_data):
    total_fields_count = 6
    incorrect_fields = []
    correct_fields_count = 0
    comparision_data = original_data[predicted_data["Time_Stamp"]]
    for key in predicted_data:
        if key == "Time_Stamp":
            continue
        if key == "ECG":
            if compare_data(
                predicted_data[key], comparision_data[key], "Heart_Rate_bpm"
            ):
                correct_fields_count += 1
            else:
                incorrect_fields.append(key)
        elif key == "NIBP":
            if compare_data(
                predicted_data[key], comparision_data[key], "Systolic_mmHg"
            ):
                correct_fields_count += 1
            else:
                incorrect_fields.append("Systolic_mmHg")
            if compare_data(
                predicted_data[key], comparision_data[key], "Diastolic_mmHg"
            ):
                correct_fields_count += 1
            else:
                incorrect_fields.append("Diastolic_mmHg")
        elif key == "SpO2":
            if compare_data(
                predicted_data[key],
                comparision_data[key],
                "Oxygen_Saturation_Percentage",
            ):
                correct_fields_count += 1
            else:
                incorrect_fields.append(key)
        elif key == "Respiration_Rate":
            if compare_data(
                predicted_data[key], comparision_data[key], "Breaths_per_Minute"
            ):
                correct_fields_count += 1
            else:
                incorrect_fields.append(key)
        elif key == "Temperature":
            if compare_data(predicted_data[key], comparision_data[key], "Fahrenheit"):
                correct_fields_count += 1
            else:
                incorrect_fields.append(key)

    accuracy = (correct_fields_count / total_fields_count) * 100

    return {
        "accuracy": accuracy,
        "total_field_count": total_fields_count,
        "correct_field_count": correct_fields_count,
        "incorrect_fields": incorrect_fields,
    }


def process_frame(frame, minutes_passed, retry=True):
    try:
        _, buffer = cv2.imencode(".jpg", frame)
        # Convert to bytes and create a BytesIO buffer
        io_buf = BytesIO(buffer)

        # Define the URL of the API endpoint
        url = "http://localhost:8000/api/v2/predict"

        # Create the files dictionary for form-data
        files = {"image": ("image.jpg", io_buf, "image/jpeg")}

        # Make the POST request with the image file
        time_taken = time.time()
        response = requests.post(url, files=files)
        time_taken = time.time() - time_taken

        print("*" * 20)
        # Check if the request was successful
        if response.status_code == 200:
            predicted_data = response.json()["data"]
            predicted_data = json.dumps(predicted_data, indent=4)
            print("Minutes passed:", minutes_passed)
            print("Time taken by api:", time_taken)
            print("")
            print(predicted_data)
            print("")
            stats = get_accuracy_details(response.json()["data"])
            print(
                f"""Accuracy: {stats["accuracy"]}%
    Total Fields: {stats["total_field_count"]}
    Correct Fields: {stats["correct_field_count"]}
    Incorrect Fields: {stats["incorrect_fields"]}
    """
            )
            print("*" * 20)

            if not os.path.exists(stats_file):
                with open(stats_file, "w") as f:
                    json.dump([stats], f)
            else:
                with open(stats_file, "r") as f:
                    stats_data = json.load(f)
                    stats_data.append(stats)
                with open(stats_file, "w") as f:
                    json.dump(stats_data, f)
            return stats["accuracy"]
        else:
            print("Failed to get prediction. Status code:", response.status_code)
            print("Skipping...")
            return None
    except Exception as e:
        print("Error:", e)
        if retry:
            print("Retying in 3 seconds...")
            time.sleep(3)
            return process_frame(frame, minutes_passed, False)
        print("Skipping...")
        return None


def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
    frame_count = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )  # Total number of frames in the video
    duration = frame_count / fps  # Duration of video in seconds

    print(f"FPS: {fps}, Total Frames: {frame_count}, Duration (seconds): {duration}")

    current_frame = 0
    minutes_passed = 0
    accuracy_array = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Done processing video.")
            break
        # Check if one minute has passed; if yes, process the frame
        if current_frame == int(minutes_passed * fps * 60):
            accuracy_array.append(process_frame(frame, minutes_passed))
            minutes_passed += 1

        current_frame += 1

    # Release the video capture object
    cap.release()

    # Calculate the average accuracy
    non_filtered_len = len(accuracy_array)
    accuracy_array = [x for x in accuracy_array if x is not None]
    print(f"Number of none values: {non_filtered_len - len(accuracy_array)}")
    average_accuracy = sum(accuracy_array) / len(accuracy_array)
    with open(stats_file, "r") as f:
        stats_data = json.load(f)
        stats_data.append({"average_accuracy": average_accuracy})
    with open(stats_file, "w") as f:
        json.dump(stats_data, f)


stats_file = "static/stats.json"
original_data = json.load(open("static/time_stamp_data_map.json"))
# Replace 'path_to_your_video.mp4' with your video file path
extract_frames("static/cam1.mp4")
