import os
import time
from multiprocessing import Pool

def run_demucs(file_path):
    command = f"demucs -o output_folder {file_path}"
    os.system(command)
    return 

if __name__ == "__main__":
    audio_files = [
            "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'",
            "/usr/lib/demucs/20_sample_songs/'Django - Wonderland.mp3'"
            ]

    total_start_time = time.time()

    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(run_demucs, audio_files)

    total_end_time = time.time()

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")
