import sys
import os
import logging
from moviepy.editor import VideoFileClip
import ssl
import time
import json
from profanityfilter import ProfanityFilter
import yt_dlp as youtube_dl
import certifi
import shutil

ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
decision = "True"


class Create_SubtitleFromLink:
    def __init__(self, output_path="whisperX/examples"):
        os.makedirs(output_path, exist_ok=True)
        self.output_path = os.path.abspath(output_path)
        self.examples_output_dir = ''
        self.sanitized_video_file = ""

    def sanitize_filename(self, filename):
        '''
        Replace spaces with underscores and remove special characters
        '''
        sanitized = filename.replace(" ", "_")
        return sanitized

    def download_video(self, link):
        '''
        Download Youtube video using youtube_dl
        '''
        logging.info("Downloading YouTube video...")
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(self.output_path, 'video.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'logger': logging,
            'progress_hooks': [self.my_hook],
            'nocheckcertificate': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            self.sanitized_video_file = os.path.join(
                self.output_path, "video.mp4")
            print(self.sanitized_video_file)
            return self.sanitized_video_file

    def my_hook(self, d):
        if d['status'] == 'finished':
            logging.info('Download completed successfully')

    def extract_audio(self, video_file):
        '''
            Define the correct path for audio extraction
            '''
        logging.info("Extracting audio from video...")
        video_path = video_file
        audio_file = os.path.splitext(video_path)[0] + ".wav"

        try:
            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_file)
            video_clip.close()
        except Exception as e:
            logging.error(f"Error while extracting audio: {e}")
            return None
        else:
            logging.info("Audio extraction completed successfully")
            return os.path.abspath(audio_file)

    def run_whisperx(self, audio_file):
        '''
        Create subtitle file using whisperX
        '''
        self.examples_output_dir = os.path.join(
            os.getcwd(), 'whisperX', 'examples')
        change_dir_command = "cd whisperX"
        whisperx_command = "whisperx " + audio_file + \
            " --compute_type int8 --language en --output_dir examples"
        full_command = f"{change_dir_command} && {whisperx_command}"

        logging.info(f"Running whisperx with input: {audio_file}")
        logging.info("Whisperx output will be saved.")

        try:
            logging.debug(f"Full command: {full_command}")
            os.system(full_command)
            logging.info(f"WhisperX completed for {audio_file}")
        except Exception as e:
            logging.error(f"Error while running WhisperX: {e}")

    def is_clean(self):
        file = open(self.sanitized_video_file[:-3] + "txt", "r")
        content = file.read()
        file.close()
        pf = ProfanityFilter()
        result = pf.is_clean(content)
        logging.info(result)
        self.grb_collections(self.examples_output_dir)
        return result

    def grb_collections(self, path):
        '''
        Delete all files from the directory specified in self.sanitized_video_file
        '''
        if os.path.isdir(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                    logging.info(f"Deleted: {file_path}")
                except Exception as e:
                    logging.error(f"Failed to delete {file_path}. Reason: {e}")
        else:
            logging.error(
                f"Provided path is not a directory: {path}")


if __name__ == "__main__":
    start_time = time.time()

    ssl._create_default_https_context = ssl._create_unverified_context

    if len(sys.argv) < 2:
        logging.error("Usage: python script_name.py <youtube_link>")
        sys.exit(1)

    link = sys.argv[1]

    creater = Create_SubtitleFromLink()
    video_file = creater.download_video(link)

    if video_file:
        audio_file = creater.extract_audio(video_file)

        if audio_file:
            creater.run_whisperx(audio_file)
    result = creater.is_clean()
    print(result)

    end_time = time.time()
    full_time = end_time - start_time
    logging.info(f"Runtime: {full_time:.2f} seconds")
