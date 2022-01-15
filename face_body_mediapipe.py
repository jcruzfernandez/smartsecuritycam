import mediapipe as mp
import cv2
from datetime import datetime, timedelta
#
import tensorflow as tf
import tensorflow_hub as hub
#from matplotlib import pyplot as plt
import numpy as np


########## tensorFlow
model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']
#######################


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_fc_detection = mp.solutions.face_detection
mp_pose = mp.solutions.pose
pose=mp_pose.Pose(min_detection_confidence=0.75,static_image_mode=False)
holistic = mp_holistic.Holistic(min_detection_confidence=0.75, 
                                static_image_mode=False)
face_detection = mp_fc_detection.FaceDetection(min_detection_confidence=0.65)
V=r"D:\PROYECTOS_PY\deteccion_movimiento\videos_de_prueba\ROBOS_captados_camaras de seguridad NOCHE.mp4"
# cap = cv2.VideoCapture(V)
# while cap.isOpened():
Time_0=datetime.now()
def make_picture(img):
    name=str(datetime.now()).split(".")[0]
    name=name.replace(" ","_")
    name=name.replace(":",".")
    picturefile=r'captures_img/{}.jpg'.format(name)
    cv2.imwrite(picturefile, img)
    return name

def detect_face(frame):
    # Recolor Feed
    
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Make Detections
    height, width, _=frame.shape
    results = face_detection.process(image_rgb)
    # print(results.face_landmarks)
    
    # Recolor image back to BGR for rendering
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #results = face_detection.process(image)
    # Draw face landmarks
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)

    # Face detections box
    if results.detections is not None:
        for detection in results.detections:
            # Bounding Box
            x = int(detection.location_data.relative_bounding_box.xmin * width)
            y = int(detection.location_data.relative_bounding_box.ymin * height)
            w = int(detection.location_data.relative_bounding_box.width * width)
            h = int(detection.location_data.relative_bounding_box.height * height)
            # mp_drawing.draw_detection(image, detection)
            cv2.rectangle(frame, (x,y),(x+w, y+h), (0, 0, 255),2)
        make_picture(frame)
    return frame
    #return q.put(frame)

def detect_body(frame):
    global Time_0
    # frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    # Recolor Feed
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Make Detections
    results1=pose.process(frame_rgb)
    # results1 = holistic.process(image_rgb)
    if results1.pose_landmarks is not None:
        # Pose Detections
        try:
            landmarks = results1.pose_landmarks.landmark
            # print(landmarks)
            if datetime.now()>Time_0:
                try:
                    Time_0 = datetime.now() + timedelta(seconds=6)
                    mp_drawing.draw_landmarks(frame, results1.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                    name=make_picture(frame)
                except:
                    pass
        except:
            pass
        # mp_drawing.draw_landmarks(frame, results1.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        #make_picture(frame)
    return frame


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

def loop_through_people(frame, keypoints_with_scores, confidence_threshold):
    for person in keypoints_with_scores:
        #draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)

def detect_body_tf(frame):
    # Resize image
    img = frame.copy()
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 256,256)
    input_img = tf.cast(img, dtype=tf.int32)

    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))

    loop_through_people(frame, keypoints_with_scores, 0.35)

    name=make_picture(frame)
    return frame