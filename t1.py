import cv2
import mediapipe as mp
import time
import numpy as np
import glob
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip, ImageClip, concatenate_videoclips


def save_img():
    i=0 #to save all the clicked images
    while(True):
        ret, frame = cap.read()
        cv2.imshow("imshow",frame)
        key=cv2.waitKey(30)
        if key==ord('q'):
            break
        # if key==ord('c'):
        if True:
            i+=1
            cv2.imshow("imshow2",frame)
            cv2.imwrite('C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs/T'+str(i)+'.png', frame)
            # cv2.imwrite('C:\Users\shach\Documents\code2021\handsTracking1\mpImgs\T' +str(i)+'.png', frame)
            # cv2.imwrite('C:\Users\shach\Documents\code2021\handsTracking1\mpImgs\T.png', frame)
            # cv2.imwrite('C:/Users/codersmine/desktop/image'+str(i)+'.png'png, framme)
            print("Wrote Image")
        time.sleep(1)


def create_video_from_imgs():
    image_folder = 'C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs'
    video_name = './tmpImgs/video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

def create_video_from_imgs2():
    image_folder = 'C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs'
    video_name = './tmpImgs/video_clip.avi'

    imgs_list = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images = [ImageClip("./tmpImgs/" + img).set_duration(2) for img in imgs_list]
    clip = concatenate_videoclips(images, method="compose")
    clip.write_videofile("test1.mp4", fps=24)

def append_img_to_video():
    new_img = 'C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs2/Te10.png'
    exist_video_name = './tmpImgs/video.avi'
    new_video_name = './tmpImgs/video_new.avi'
    cap = cv2.VideoCapture(exist_video_name)

    ret, frame = cap.read()
    height, width, layers = frame.shape
    out = cv2.VideoWriter(new_video_name, cv2.VideoWriter_fourcc(*'MJPG'), 1, (width, height))
    while ret:
        out.write(frame)
        ret, frame = cap.read()

    out.write(cv2.imread(new_img))
    print("!")


def append_img_to_video2():
    new_img = 'C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs2/Te10.png'
    exist_video_name = './tmpImgs/video.avi'
    new_video_name = './tmpImgs/video_new44.avi'
    cap = cv2.VideoCapture(exist_video_name)

    ret, frame = cap.read()
    height, width, layers = frame.shape
    out = cv2.VideoWriter('tmp_video.mp4', cv2.VideoWriter_fourcc(*'MJPG'), 1, (width, height))
    out.write(cv2.imread(new_img))

    image_clip = VideoFileClip('./tmp_video.mp4')
    orig_video_clip = VideoFileClip(exist_video_name)
    final_clip = concatenate_videoclips([image_clip, orig_video_clip], method="compose")
    final_clip.write_videofile(new_video_name)

    print("!")

def append_img_to_video3():
    img_name = 'C:/Users/shach/Documents/code2021/handsTracking1/tmpImgs/Te10.png'
    exist_video_name = './tmpImgs/video.avi'
    new_video_name = './tmpImgs/video_new.avi'
    frame = cv2.imread(img_name)
    height, width, layers = frame.shape
    video = cv2.VideoWriter(new_video_name, 0, 1, (width, height))

    video.write(cv2.imread(exist_video_name))
    video.write(cv2.imread(img_name))


cap = cv2.VideoCapture(0)
if __name__ == '__main__':
    create_video_from_imgs()
    append_img_to_video()

    # create_video_from_imgs2()
    # append_img_to_video2()
    cap.release()
    cv2.destroyAllWindows()
