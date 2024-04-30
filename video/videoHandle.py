from utils.logger import Logger
from utils.logger import LogLevel
import ffmpeg

class videoHandler:
    def __init__(self):
        self.logger = Logger()

    def add_suffix(self, filename, suffix):
        self.logger.log(LogLevel.DEBUG, f"为{filename}添加后缀{suffix}")
        file_name = '.'.join(filename.split('.')[:-1])
        file_type = filename.split('.')[-1]
        return file_name + '_' + suffix + '.' + file_type

    def progress_callback(self, filename, progress):
        print(f"Processing {filename} - progress: {progress:.2f}%")

    def change_speed(self, filename, speed):
        output_file = self.add_suffix(filename, str(speed))
        input_file = ffmpeg.input(filename)
        audio = input_file.audio.filter('atempo', speed)
        video = input_file.video.filter('setpts', 'PTS/' + str(speed))
        # ffmpeg.output(audio, video, output_file, progress=lambda p: self.progress_callback(p, filename)).run()
        ffmpeg.output(audio, video, output_file).run()
        self.logger.log(LogLevel.DEBUG, f"转换完成，输出文件为{output_file}")

    def change_speed_all(self, input_files, speed):
        for filename in input_files:
            if filename:
                self.logger.log(LogLevel.DEBUG, f"改变{filename}的速度为{speed}倍")
                self.change_speed(filename, speed)

