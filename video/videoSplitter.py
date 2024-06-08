from video.abstract_videoHandle import videoHandler
from utils.logger import LogLevel
from utils.naming import add_suffix
import ffmpeg
import os

class videoSplitter(videoHandler):
    def split_video(self, filename, timestamps, file_text):
        for i in range(len(timestamps)):
            output_filename = add_suffix(filename, f"_{str(i+1)}_{file_text[i]}")
            if os.path.exists(output_filename): os.remove(output_filename)
            start_time = timestamps[i]
            if i < len(timestamps) - 1:
                end_time = timestamps[i + 1]
            else:
                end_time = None
            output_filters = {
                'acodec' : 'copy',
                'vcodec' : 'copy',
                'loglevel' : 'warning'
            }
            # 使用ffmpeg切割视频, 对于最后一个片段，不需要指定结束时间
            with self.lock:
                if i < len(timestamps) - 1:
                    self.logger.log(LogLevel.DEBUG, f"正在处理第{i+1}个片段，时间段为{start_time} - {end_time}，输出文件为{output_filename}")
                    self.process = ffmpeg.input(filename, ss=start_time, to=end_time).output(output_filename, **output_filters).run_async()
                else:
                    self.logger.log(LogLevel.DEBUG, f"正在处理最后一个片段，时间段为{start_time}，输出文件为{output_filename}")
                    self.process = ffmpeg.input(filename, ss=start_time).output(output_filename, **output_filters).run_async()
            #等待任务结束
            self.process.wait()

    def split_videos(self, input_files, timestamps_list, file_text_list):
        for i, filename in enumerate(input_files):
            if filename and self.atomic_is_running():
                self.logger.log(LogLevel.DEBUG, f"正在处理第{i+1}个视频文件{filename}")
                self.split_video(filename, timestamps_list[i], file_text_list[i])
        with self.lock:
            self.running = False
            self.process = None
