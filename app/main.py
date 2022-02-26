from pkg_resources import UnknownExtra
from flask import Flask, Response, request
from flask_cors import CORS

from pycoral.adapters.common import input_size
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import classify

import random
from datetime import datetime

import database as db
import cv2
import json
import time
import threading
import uuid

app = Flask(__name__, static_url_path="/images")
CORS(app)

current_frame = None
lock = threading.Lock()
previous_detection = None


def inference():
    global current_frame, lock

    interpreter = make_interpreter(
        "./lite-model_cropnet_classifier_cassava_disease_V1_1.tflite"
    )
    interpreter.allocate_tensors()
    labels = read_label_file("./cassava_labels.txt")
    size = common.input_size(interpreter)

    cap = cv2.VideoCapture(-1)

    y = random.uniform(40.20073530692846, 40.2151558052675)
    x = -88.12527531155014

    prev_result = None

    while cap.isOpened():
        x = random.uniform(x - 0.001, x + 0.001)
        ret, frame = cap.read()
        if not ret:
            break
        cv2_im = frame

        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, size)

        common.set_input(interpreter, cv2_im_rgb)

        start_time = time.monotonic()
        interpreter.invoke()
        results = classify.get_classes(interpreter, 3, 0.1)

        end_time = time.monotonic()
        text_lines = [
            " ",
            "Inference: {:.2f} ms".format((end_time - start_time) * 1000),
        ]

        for result in results:
            text_lines.append("score={:.2f}: {}".format(result.score, labels[result.id]))
            print(" ".join(text_lines))

        if prev_result != 4 and prev_result != 5:
            if prev_result != results[0].id:
                file_name = "images/" + str(uuid.uuid4()) + ".jpg"
                cv2.imwrite(file_name, frame)

                epoch = datetime.now().timestamp()
                day = datetime.now().strftime("%Y%m%d")
                db.add_object(file_name, labels[results[0].id], x, y, day, epoch)

        for idx, val in enumerate(text_lines, start=1):
            if idx == 1:
                height = 10
            else:
                height = idx * 30

            cv2_im = cv2.putText(
                cv2_im,
                val,
                (10, height),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
            )

        prev_result = results[0].id

        with lock:
            current_frame = cv2_im

        prev_result = results[0].id

    cap.release()


def create_response():
    global current_frame, lock
    while True:
        with lock:
            if current_frame is None:
                continue

            ret, frame = cv2.imencode(".jpg", current_frame)
            if not ret:
                continue

        yield (
            b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + bytearray(frame) + b"\r\n"
        )


@app.route("/stream")
def stream():
    return Response(
        create_response(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/api/v1/get_data")
def get_data():
    date = request.args.get("date")

    features = []
    objects = db.get_objects_by_date(date)

    for obj in objects:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [obj["x_coordinate"], obj["y_coordinate"]],
                },
                "properties": {
                    "classification": obj["classification"],
                    "date": obj["date"],
                    "image": obj["image"],
                },
            }
        )

    return json.dumps({"type": "FeatureCollection", "features": features})


t = threading.Thread(target=inference)
t.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
