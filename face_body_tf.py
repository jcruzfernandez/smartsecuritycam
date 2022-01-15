import cv2
from datetime import datetime, timedelta
import os
import tensorflow as tf
import tensorflow_hub as hub
#from matplotlib import pyplot as plt
import numpy as np

########## tensorFlow
# model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
model= hub.load(os.path.join(os.getcwd(),"movenet_multipose_lightning_1"))
movenet = model.signatures['serving_default']
#######################
#Opcional si se cuenta con una tarjeta de video - GPU
# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

Time_0=datetime.now()
def make_picture_tf(img):
    name=str(datetime.now()).split(".")[0]
    name=name.replace(" ","_")
    name=name.replace(":",".")
    picturefile=r'captures_img/{}.jpg'.format(name)
    cv2.imwrite(picturefile, img)
    return name

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    kp_conf_mean=np.mean(shaped, axis=0)
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            print (kp_conf_mean[2])
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

def loop_through_people(frame, keypoints_with_scores, confidence_threshold):
    for person in keypoints_with_scores:
        #draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)

def detect_body_tf(frame,confidence_threshold):
    global Time_0
    # Resize image
    img = frame.copy()
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 160,256)
    input_img = tf.cast(img, dtype=tf.int32)

    # Detection section
    results = movenet(input_img)
    keypoints_with_scores = results['output_0'].numpy()[:,:,:51].reshape((6,17,3))
    kp_conf_bol=False
    for keypoints in keypoints_with_scores:
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        # kp_conf_mean=np.mean(shaped, axis=0)
        # print(kp_conf_mean)
        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                if datetime.now()>Time_0:
                    kp_conf_bol=True
                    cv2.circle(frame, (int(kx), int(ky)), 6, (0,0,255), 1)
    if kp_conf_bol==True:
        Time_0 = datetime.now() + timedelta(seconds=6)
        name=make_picture_tf(frame)

    # loop_through_people(frame, keypoints_with_scores, 0.50)
        #name=make_picture_tf(frame)
    return frame