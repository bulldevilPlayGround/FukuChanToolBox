from utils.logger import Logger
from utils.logger import LogLevel
from utils.naming import add_suffix
import ffmpeg

class videoHandler:
    def __init__(self):
        self.logger = Logger()
        self.gpu_acceleration = False

    def progress_callback(self, filename, progress):
        print(f"Processing {filename} - progress: {progress:.2f}%")

    def change_speed(self, filename, speed):
        self.logger.log(LogLevel.DEBUG, f"为{filename}添加后缀{str(speed)}")
        output_file = add_suffix(filename, f"_{str(speed)}")
        input_file = ffmpeg.input(filename)
        audio = input_file.audio.filter('atempo', speed)
        video = input_file.video.filter('setpts', 'PTS/' + str(speed))
        # 启用GPU加速
        if self.gpu_acceleration:
            ffmpeg_options = {
            '-hwaccel': 'cuda',  # 使用NVIDIA CUDA加速
            '-c:v': 'h264_nvenc',  # 使用NVIDIA NVENC编码器
            '-preset': 'fast',  # 设置编码预设为快速编码
            }
            ffmpeg.output(audio, video, output_file, options=ffmpeg_options).run()
        else:
            ffmpeg.output(audio, video, output_file).run()
        self.logger.log(LogLevel.DEBUG, f"转换完成，输出文件为{output_file}")

    def change_speed_all(self, input_files, speed):
        for filename in input_files:
            if filename:
                self.logger.log(LogLevel.DEBUG, f"改变{filename}的速度为{speed}倍")
                self.change_speed(filename, speed)

    def split_video(self, filename, timestamps, file_text):
        for i in range(len(timestamps)):
            start_time = timestamps[i]
            output_filename = add_suffix(filename, f"_{str(i+1)}{file_text[i]}")
            if i < len(timestamps) - 1:
                end_time = timestamps[i + 1]
            else:
                end_time = None
            # 使用ffmpeg切割视频, 对于最后一个片段，不需要指定结束时间
            if i < len(timestamps) - 1:
                self.logger.log(LogLevel.DEBUG, f"正在处理第{i+1}个片段，时间段为{start_time} - {end_time}，输出文件为{output_filename}")
                # ffmpeg.input(filename, ss=start_time, to=end_time).output(output_filename, acodec='copy', vcodec='copy', loglevel='warning').run()
            else:
                self.logger.log(LogLevel.DEBUG, f"正在处理最后一个片段，时间段为{start_time}，输出文件为{output_filename}")
                # ffmpeg.input(filename, ss=start_time).output(output_filename, acodec='copy', vcodec='copy', loglevel='warning').run()

    def split_videos(self, input_files, timestamps_list, file_text_list):
        for i, filename in enumerate(input_files):
            if filename:
                self.logger.log(LogLevel.DEBUG, f"正在处理第{i+1}个视频文件{filename}")
                self.split_video(filename, timestamps_list[i], file_text_list[i])
