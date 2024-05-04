from video.abstract_videoHandle import videoHandler
from utils.logger import LogLevel
from utils.naming import add_suffix
import ffmpeg
import os

class videoSpeeder(videoHandler):
    def change_speed(self, filename, speed):
        self.logger.log(LogLevel.DEBUG, f"为{filename}添加后缀{str(speed)}")
        output_filename = add_suffix(filename, f"_{str(speed)}")
        if os.path.exists(output_filename): os.remove(output_filename)
        output_filters = {
            'vf' : f'setpts=PTS/{speed}',
            'af' : f'atempo={speed}'
        }
        if self.gpu_acceleration:
            output_filters.update({})
        with self.lock:
            self.process = ffmpeg.input(filename).output(output_filename, **output_filters).run_async()
        #等待任务结束
        self.process.wait()
        self.logger.log(LogLevel.DEBUG, f"转换完成，输出文件为{output_filename}")

    def change_speed_all(self, input_files, speed):
        for filename in input_files:
            if filename and self.atomic_is_running():
                self.logger.log(LogLevel.DEBUG, f"改变{filename}的速度为{speed}倍")
                self.change_speed(filename, speed)
        with self.lock:
            self.running = False
            self.process = None
