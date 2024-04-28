import sys
import os
import logging
from pytube import YouTube
from moviepy.editor import VideoFileClip
import ssl
import time
import json
from profanityfilter import ProfanityFilter

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
        self.sanitized_video_file = ""

    def sanitize_filename(self, filename):
        '''
        Replace spaces with underscores and remove special characters
        '''

        sanitized = filename.replace(" ", "_")
        return sanitized

    def download_video(self, link):
        '''
        Download Youtube video using pytube
        '''

        logging.info("Downloading YouTube video...")
        youtube_object = YouTube(link)
        youtube_stream = youtube_object.streams.get_highest_resolution()

        try:
            sanitized_filename = self.sanitize_filename(
                youtube_stream.default_filename)
            youtube_stream.download(
                self.output_path, filename=sanitized_filename)
        except Exception as e:
            logging.error(f"Error while downloading video: {e}")
            return None
        else:
            logging.info("Download completed successfully")
            return sanitized_filename

    def extract_audio(self, video_file):
        '''
        Define the correct path for audio extraction
        '''

        logging.info("Extracting audio from video...")
        self.sanitized_video_file = self.sanitize_filename(video_file)
        video_path = os.path.join(self.output_path, self.sanitized_video_file)
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

        change_dir_command = "cd whisperX"
        whisperx_command = "whisperx " + audio_file + \
            " --compute_type int8 --language en --output_dir results"
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
        file = open(os.getcwd() + "/whisperX/results/" +
                    self.sanitized_video_file[:-3] + "txt", "r")
        content = file.read()
        file.close()
        pf = ProfanityFilter()
        result = pf.is_clean(content)
        logging.info(result)
        return result


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
    sys.stdout.write(json.dumps({"decision": result}))

    end_time = time.time()
    full_time = end_time - start_time
    '''

    try:
        video_file = os.getcwd() + f"/whisperX/examples/{video_file}"
        os.remove(video_file)
        print(f"File '{video_file}' deleted successfully.")
        os.remove(audio_file)
        print(f"File '{audio_file}' deleted successfully.")
    except FileNotFoundError as e:
        print(f"File '{e}' not found.")
    '''
    logging.info(f"Runtime: {full_time:.2f} seconds")
