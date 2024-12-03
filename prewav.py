import os
import time
from multiprocessing import Pool
import subprocess

def run_demucs(file_path):
    command = f"demucs -o output_folder {file_path}"
    subprocess.run(command, shell=True, check=True)
    return f"Processed {file_path}"

def convert_mp3_to_wav(input_file, output_file):
    command = f"ffmpeg -i {input_file} -vn -acodec pcm_s16le -ar 44100 -ac 2 {output_file}"
    subprocess.run(command, shell=True, check=True)
    return output_file

if __name__ == "__main__":
    audio_file = "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'"

    total_start_time = time.time()

    wav_file = audio_file.replace(".mp3", ".wav")
    convert_mp3_to_wav(audio_file, wav_file)

    run_demucs(wav_file)

    total_end_time = time.time()

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")
