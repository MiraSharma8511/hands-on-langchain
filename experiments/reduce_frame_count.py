import base64

import cv2


def get_frame_count(v_f_p):
    base64frames = []
    v_file = cv2.VideoCapture(v_f_p)

    while v_file.isOpened():
        success, frame = v_file.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64frames.append(base64.b64encode(buffer).decode("utf-8"))

    v_file.release()
    frameCounts = len(base64frames)
    print(frameCounts, " get frames count read.")
    return base64frames, frameCounts


def reduce_frame_counts(v_f):
    # Open the video file
    cap = cv2.VideoCapture(v_f)
    # For streams:
    #   cap = cv2.VideoCapture('rtsp://url.to.stream/media.amqp')
    # Or e.g. most common ID for webcams:
    #   cap = cv2.VideoCapture(0)
    count = 0

    base64frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode(".jpg".format(count), frame)
            count += 5  # i.e. at 30 fps, this advances one second
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            base64frames.append(base64.b64encode(buffer).decode("utf-8"))

            # cv2.imwrite('frame{:d}.jpg'.format(count), frame)
            # count += 30  # i.e. at 30 fps, this advances one second
            # cap.set(cv2.CAP_PROP_POS_FRAMES, count)

        else:
            cap.release()
            break

    frameCounts = len(base64frames)
    print(frameCounts, "reduced count frames read.")


video_read_path = "./pages/video/video_analysis.mp4"
# video = cv2.VideoCapture(video_read_path)
# get_frame_count("video_analysis.mp4")
reduce_frame_counts("video_analysis.mp4")
