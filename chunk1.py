import os
import time
from multiprocessing import Pool
import subprocess

def split_audio_with_ffmpeg(input_file, output_dir, chunk_duration_sec=30):
    os.makedirs(output_dir, exist_ok=True)
    command = f"ffmpeg -i {input_file} -f segment -segment_time {chunk_duration_sec} -c copy {output_dir}/output%03d.wav"
    subprocess.run(command, shell=True, check=True)

def run_demucs(file_path):
    command = f"demucs -o output_folder {file_path}"
    os.system(command)
    return f"Processed {file_path}"

def merge_chunks_for_track(chunk_output_dir, track_name, output_file):
    track_chunks = sorted([
        os.path.join(chunk_output_dir, chunk_dir, f"{track_name}.wav")
        for chunk_dir in os.listdir(chunk_output_dir)
        if os.path.isdir(os.path.join(chunk_output_dir, chunk_dir))
    ])

    if not track_chunks:
        raise FileNotFoundError(f"No files found for track: {track_name}")

    print(f"Track {track_name} chunks: {track_chunks}")


    combined = [f"file '{chunk}'" for chunk in track_chunks]
    with open("file_list.txt", "w") as file_list:
        file_list.write("\n".join(combined))

    command = f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_file}"
    subprocess.run(command, shell=True, check=True)
    os.remove("file_list.txt")
    return f"Combined {track_name} and saved to {output_file}"

if __name__ == "__main__":
    audio_file = "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'"

    total_start_time = time.time()

    chunk_output_dir = "chunks1"
    split_audio_with_ffmpeg(audio_file, chunk_output_dir, chunk_duration_sec=30)

    chunk_paths = sorted([os.path.join(chunk_output_dir, f) for f in os.listdir(chunk_output_dir) if f.endswith(".wav")])
    print(chunk_paths)
    
    
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(run_demucs, chunk_paths)

    
    demucs_output_dir = "output_folder/htdemucs"
    final_tracks = {}
    for track in ["bass", "drums", "other", "vocals"]:
        output_file = f"{track}_final.wav"
        final_tracks[track] = merge_chunks_for_track(demucs_output_dir, track, output_file)

    total_end_time = time.time()

    print("\n".join(results))
    for track, path in final_tracks.items():
        print(path)

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")
    
    

