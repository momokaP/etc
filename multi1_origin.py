import os
import time

if __name__ == "__main__":
    audio_files = [
        "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'",
        "/usr/lib/demucs/20_sample_songs/'Django - Wonderland.mp3'"
    ]

    total_start_time = time.time()

    command = f"demucs --jobs=2 -o output_folder_origin {' '.join(audio_files)}"
    os.system(command)

    total_end_time = time.time()

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")
