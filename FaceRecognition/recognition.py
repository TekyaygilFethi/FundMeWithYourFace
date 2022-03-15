import numpy as np
import face_recognition as fr
import cv2
import os
from os import listdir
from os.path import isfile, join
import time

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

file_path_prefix = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "Data/images"
)


def __getencodings():
    known_face_encondings = []
    known_face_names = []
    known_face_ids = []

    images = [f for f in listdir(file_path_prefix) if isfile(join(file_path_prefix, f))]

    for img in images:
        known_face_encondings.append(
            fr.face_encodings(fr.load_image_file(f"{file_path_prefix}/{img}"))[0]
        )
        name = img.split(".")[0].split("_")[0]
        id = img.split(".")[0].split("_")[1]
        known_face_names.append(name)
        known_face_ids.append(id)

    return (known_face_encondings, known_face_names, known_face_ids)


def capture():
    id = None
    name = None

    video_capture = cv2.VideoCapture(0)
    known_face_encondings, known_face_names, known_face_ids = __getencodings()

    isSet = False
    first_tm = time.time()
    while True:
        _, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]
        name = None
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = "Unknown"

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                id = known_face_ids[best_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_SIMPLEX

            if name == "Unknown":
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                )
            else:
                if isSet is False:
                    preframe_tm = time.time()
                    isSet = True

                cv2.putText(
                    frame,
                    f"{name} olarak login olunuyor...",
                    (left + 6, bottom - 6),
                    font,
                    0.5,
                    (255, 255, 255),
                    1,
                )

        cv2.imshow("Webcam_facerecognition", frame)

        if (cv2.waitKey(1) & 0xFF == ord("q")) or (
            ((name != None and name != "Unknown") and (time.time() - preframe_tm > 3))
            or (time.time() - first_tm > 10)
        ):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return (id, name)
