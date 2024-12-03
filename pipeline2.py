import os
import time
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import subprocess


def split_audio_with_ffmpeg(input_file, output_dir, chunk_duration_sec=30):
    os.makedirs(output_dir, exist_ok=True)
    command = f"ffmpeg -i {input_file} -f segment -segment_time {chunk_duration_sec} -c copy {output_dir}/output%03d.wav"
    subprocess.run(command, shell=True, check=True)


def run_demucs(file_path):
    command = f"demucs -o output_folder {file_path}"
    subprocess.run(command, shell=True, check=True)
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
    file_list_path = f"file_list_{track_name}.txt"
    with open(file_list_path, "w") as file_list:
        file_list.write("\n".join(combined))

    command = f"ffmpeg -f concat -safe 0 -i {file_list_path} -c copy {output_file}"
    subprocess.run(command, shell=True, check=True)
    os.remove(file_list_path)
    return f"Combined {track_name} and saved to {output_file}"


def process_audio_file(audio_file, chunk_duration_sec=30):
    base_name = os.path.basename(audio_file).replace(".mp3", "").replace("'", "").replace(" ","")
    chunk_output_dir = f"chunks_{base_name}"
    demucs_output_dir = f"output_folder/htdemucs"

    # Step 1: Split audio into chunks
    split_audio_with_ffmpeg(audio_file, chunk_output_dir, chunk_duration_sec)

    # Step 2: Process each chunk with Demucs
    chunk_paths = sorted([
        os.path.join(chunk_output_dir, f) for f in os.listdir(chunk_output_dir) if f.endswith(".wav")
    ])
    print(f"Chunks for {audio_file}: {chunk_paths}")

    #for chunk_path in chunk_paths:
    #    run_demucs(chunk_path)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(run_demucs, chunk_paths))

    # Step 3: Merge chunks for each track
    final_tracks = {}
    for track in ["bass", "drums", "other", "vocals"]:
        output_file = f"{base_name}_{track}_final.wav"
        final_tracks[track] = merge_chunks_for_track(demucs_output_dir, track, output_file)

    return final_tracks


if __name__ == "__main__":
    # List of audio files to process
    audio_files = [
        "/usr/lib/demucs/20_sample_songs/'Cosmonkey - Forever.mp3'",
        "/usr/lib/demucs/20_sample_songs/'Django - Wonderland.mp3'"
    ]

    total_start_time = time.time()

    # Process files in parallel
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_audio_file, audio_files)

    total_end_time = time.time()

    # Print results
    for i, result in enumerate(results):
        print(f"Results for {audio_files[i]}:")
        for track, path in result.items():
            print(path)

    print(f"\nTotal processing time: {total_end_time - total_start_time:.2f} seconds")

