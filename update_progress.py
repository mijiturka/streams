from datetime import timedelta
from pathlib import Path
import threading

def readable(seconds):
    return timedelta(seconds=seconds)

class Progress():
    def __init__(self, movie_length):
        self.now_at = 0
        self.movie_length = movie_length
        self.movie_length_readable = readable(movie_length)

        file_path = "./movie-progress.txt"
        self.f = Path(file_path)

        self.lock = threading.Lock()

    def update(self):
        if self.now_at < self.movie_length-1:
            threading.Timer(1.0, self.update).start()

        with self.lock:
            self.now_at += 1

        self.write()

    def write(self):
        self.f.write_text(f'{readable(self.now_at)}/{self.movie_length_readable}')

    def start(self):
        threading.Timer(1.0, self.update).start()

progress = Progress(32)
progress.start()
