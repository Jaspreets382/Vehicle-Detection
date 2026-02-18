from flask import Flask, render_template, Response
import cv2
import torch
import numpy as np
from flask import jsonify
import time


app = Flask(__name__)
 
streaming = True
# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  
 # car, motorcycle, bus, truck (COCO classes)
model.classes = [2, 3, 5, 7] 

# Class names mapping
class_map = {2: "car", 3: "motorbike", 5: "bus", 7: "truck"}
total_counts = {v: 0 for v in class_map.values()}

# Video setup
count_line_y_min, count_line_y_max = 550, 565

video_path = "videos/vehicle.mp4"
def generate_frames():
    global total_counts, streaming
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    total_counts = {v: 0 for v in class_map.values()}  # Reset at start

    while True:
        if not streaming:
            time.sleep(0.1)
            continue

        success, frame = cap.read()
        if not success:
            break

        frame_number += 1
        if frame_number % 2 != 0:
            continue

        frame = cv2.resize(frame, (1280, 720))
        height, width = frame.shape[:2]

        # Run YOLOv5 inference
        results = model(frame)
        detections = results.xyxy[0].cpu().numpy()

        counts = {v: 0 for v in class_map.values()}
        cv2.rectangle(frame, (0, count_line_y_min), (width, count_line_y_max), (0, 255, 255), 2)

        for *xyxy, conf, cls_id in detections:
            cls_id = int(cls_id)
            if cls_id in class_map:
                label = class_map[cls_id]
                x1, y1, x2, y2 = map(int, xyxy)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

                if count_line_y_min <= cy <= count_line_y_max:
                    counts[label] += 1
                    total_counts[label] += 1

        y_offset = 30
        for v_type in counts:
            cv2.putText(frame, f"{v_type.capitalize()} (This Frame): {counts[v_type]}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            y_offset += 20
        for v_type in total_counts:
            cv2.putText(frame, f"{v_type.capitalize()} (Total): {total_counts[v_type]}", (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            y_offset += 20

        total = sum(total_counts.values())
        cv2.putText(frame, f"Total Vehicles: {total}", (10, y_offset + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Encode and yield frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/start', methods=['POST'])
def start_stream():
    global streaming
    streaming = True
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop_stream():
    global streaming
    streaming = False
    return jsonify({"status": "stopped"})



@app.route('/vehicle_count')
def vehicle_count():
    total = sum(total_counts.values())
    return jsonify({"total": total, "details": total_counts})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


from flask import request

@app.route('/change_video', methods=['POST'])
def change_video():
    global current_video, streaming
    data = request.get_json()
    filename = data.get("filename")

    # Stop streaming temporarily (optional)
    streaming = False
    time.sleep(0.2)  # Allow stream to stop

    current_video = f"videos/{filename}"
    print("[INFO] Changed video to:", current_video)

    # Resume streaming if needed
    streaming = True
    return jsonify({"status": "video changed", "file": filename})


@app.route('/set_video', methods=['POST'])
def set_video():
    global video_path, streaming
    data = request.get_json()
    filename = data.get("filename")
    video_path = f"videos/{filename}"
    streaming = True
    return jsonify({"status": "video changed", "file": filename})

if __name__ == '__main__':
    app.run(debug=True)
