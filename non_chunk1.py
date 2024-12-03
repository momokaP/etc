import os
import time
from multiprocessing import Pool
import subprocess

def run_demucs(file_path):
    command = f"demucs -j=5 -o output_folder_origin {file_path}"
    os.system(command)
    return f"Processed {file_path}"

if __name__ == "__main__":
    audio_file = "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'"

    total_start_time = time.time()

    run_demucs(audio_file)

    total_end_time = time.time()

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")
    
    

