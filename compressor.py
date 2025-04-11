# compressor.py
#
# Copyright (C) 2025 [Il Tuo Nome]
#
# This file is part of VideoCompressor.
#
# VideoCompressor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VideoCompressor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pymediainfo import MediaInfo
import os
import subprocess
from threading import Thread

class Video:
    def __init__(self, filename, filext, filepath):
        self.filename = filename
        self.filext = filext 
        self.filepath = filepath
        self.compress_process = None
        self.ffmpeg_process = None
        self.filesize = os.path.getsize(self.filepath)
        self.nfilesize = 0
        self.compression_complete = False
        self.ffmpeg_path = "./ffmpeg/bin/ffmpeg.exe"

        # Get video duration
        self.ms_duration = 0
        media_info = MediaInfo.parse(self.filepath)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                self.ms_duration = track.duration

    def calculate_bit_rate(self, nDim, audio_bitrate=128):
        B_dimension = nDim * (10 ** 6)
        b_dimension = B_dimension * 8
        s_duration = (self.ms_duration / (10 ** 3))
        if not s_duration == 0:
            bitrate = int(((b_dimension / s_duration) - audio_bitrate) / (10 ** 3))
            return bitrate
        return None

    def compress_video(self, nDim, output, audio_bitrate="128k", buffer_size="5000k"):
        t1 = Thread(target=self.compress_proc, args=[nDim, output,])
        t1.start()

    def compress_proc(self, nDim, output, audio_bitrate="128k", buffer_size="5000k"):
        self.compression_complete = False
        video_bitrate = self.calculate_bit_rate(nDim)
        
        if not video_bitrate:
            return 1
        else:
            video_bitrate = str(video_bitrate) + 'k'
            command = [
                self.ffmpeg_path, "-i", self.filepath,
                "-c:v", "libx264", "-b:v", video_bitrate, "-minrate", video_bitrate, "-maxrate", video_bitrate,
                "-bufsize", buffer_size, "-c:a", "aac", "-b:a", audio_bitrate, "-y", output
            ]
            
            self.ffmpeg_process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.ffmpeg_process.wait()
            self.compression_complete = True

    def stop_compression(self):
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ffmpeg_process.kill()
                self.ffmpeg_process.wait()
            self.ffmpeg_process = None

if __name__ == "__main__":
    filename, filext = os.path.splitext(input("Enter Filename: "))
    filepath = input("Enter File Path: ")
    new_dimension = int(input("Enter the desired dimensions (MB): "))

    v1 = Video(filename, filext, filepath)
    v1.compress_video(nDim=new_dimension, output="vid_test.mp4")

    