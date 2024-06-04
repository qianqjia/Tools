import cv2

def extract_frames(video_path, output_path, interval):
    video = cv2.VideoCapture(video_path)
    frame_count = 1

    while True:
        success, frame = video.read()

        if not success:
            break

        if frame_count % interval == 0:
            frame_path = "{}/frame_{:04d}.jpg".format(output_path, frame_count)
            cv2.imwrite(frame_path, frame)
            print("Saved frame: {}".format(frame_path))

        frame_count += 1

    video.release()

video_path = "D:/Code/ZoomLab_NeRF/output_video.mp4"  # 视频文件路径
output_path = "./frames"  # 输出照片的文件夹路径
interval = 10  # 截取间隔（帧）

extract_frames(video_path, output_path, interval)