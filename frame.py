import os
import cv2
import numpy
import random

def image_from_video(video_path, num_frames=5):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = sorted(random.sample(range(total_frames), num_frames))
    frames = []
    
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    video_path = os.path.dirname(video_path)
    frames_dir = os.path.join(video_path, 'frames')
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    for i, frame in enumerate(frames):
        cv2.imwrite(os.path.join(frames_dir, f'frame_{i}.jpg'), frame)
    cap.release()

    return