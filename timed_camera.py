import cv2
import streamlit as st
from datetime import datetime
import time
import glob
import os
from emailling import send_email
from threading import Thread

st.title("Motion Detector")
start = st.button('Start Camera')

skip = -2
first_frame = None
status_list = []
count = 0

def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")


if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get current time as a datetime object
        now = datetime.now()

        # Get day and time add them to the frame
        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 0),
                    thickness=2, lineType=cv2.LINE_AA)
        streamlit_image.image(frame)
        status = 0
        check, frame = camera.read()
        skip += 1 
        if skip <=22:
            continue
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gauss_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if first_frame is None:
            first_frame = gray_frame_gauss_blur

        delta_frame = cv2.absdiff(first_frame, gray_frame_gauss_blur)

        thresh_frame = cv2.threshold(delta_frame, 45, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1
                cv2.imwrite(f"images/{count}.png", frame)
                count += 1
                all_images = glob.glob("images/*.png")
                index = int(len(all_images)/2)
                image_with_object = all_images[index]
                # send_email()

        cv2.imshow("My video", frame)

        status_list.append(status)
        status_list = status_list[-2:]

        if status_list[0] == 1 and status_list[1] == 0:
            email_thread = Thread(target=send_email, args=(image_with_object, ))
            # email_thread.daemon = True
            clean_thread = Thread(target=clean_folder)
            email_thread.daemon = True
            # send_email(image_with_object) AM CREAT THREAD uri pentru aceste apeluri
            # clean_folder()
            email_thread.start()

        # print(status_list)

    # Afișăm cadrele pt Debug
        # cv2.imshow("First Frame", first_frame)
        # cv2.imshow("Gray Frame", gray_frame)
        # cv2.imshow("Blurred Frame", gray_frame_gauss_blur)
        # cv2.imshow("Delta Frame", delta_frame)
        # cv2.imshow("Threshold Frame", thresh_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

camera.release()
clean_thread.start()