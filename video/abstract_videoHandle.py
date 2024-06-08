from utils.logger import Logger
from utils.logger import LogLevel
from utils.naming import add_suffix
import ffmpeg
import threading
class videoHandler:
    def __init__(self):
        self.logger = Logger()
        self.gpu_acceleration = False
        self.process = None
        self.running = False
        self.lock = threading.Lock()

    def atomic_is_running(self):
        with self.lock:
            return self.running

    def stop_processing(self):
        with self.lock:
            if self.process:
                self.process.terminate()
                self.running = False
                self.process = None
                self.logger.log(LogLevel.DEBUG, "已停止处理")