import cv2

def extract_video_segment(video_path, output_path, start_time, end_time):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # 设置视频编码器和输出参数
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0

    while True:
        success, frame = video.read()

        if not success:
            break

        if frame_count >= start_frame and frame_count <= end_frame:
            output_video.write(frame)

        if frame_count > end_frame:
            break

        frame_count += 1

    video.release()
    output_video.release()

video_path = "G:/BaiduNetdiskDownload/YN100017.MP4"  # 输入视频文件路径
output_path = "./output_video.mp4"  # 输出视频文件路径
start_time = 4 * 60 + 36  # 开始时间，单位为秒
end_time = 5 * 60 + 13  # 结束时间，单位为秒

extract_video_segment(video_path, output_path, start_time, end_time)