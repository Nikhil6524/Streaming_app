import subprocess
import os


def generate_hls(input_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    master_playlist = os.path.join(output_dir, "master.m3u8")

    # 720p
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-vf", "scale=1280:720",
        "-c:a", "aac", "-ar", "48000",
        "-c:v", "h264", "-profile:v", "main",
        "-crf", "20", "-g", "48", "-keyint_min", "48",
        "-sc_threshold", "0",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-b:v", "2800k",
        "-maxrate", "2996k",
        "-bufsize", "4200k",
        "-hls_segment_filename", f"{output_dir}/720p_%03d.ts",
        f"{output_dir}/720p.m3u8"
    ])

    # 480p
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-vf", "scale=854:480",
        "-c:a", "aac", "-ar", "48000",
        "-c:v", "h264",
        "-crf", "23",
        "-g", "48", "-keyint_min", "48",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-b:v", "1400k",
        "-maxrate", "1498k",
        "-bufsize", "2100k",
        "-hls_segment_filename", f"{output_dir}/480p_%03d.ts",
        f"{output_dir}/480p.m3u8"
    ])

    # Master playlist
    with open(master_playlist, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\n")
        f.write("720p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=854x480\n")
        f.write("480p.m3u8\n")

    return master_playlist


def generate_thumbnail(input_path: str, output_dir: str):
    thumbnail_path = os.path.join(output_dir, "thumbnail.jpg")

    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ss", "00:00:02",
        "-vframes", "1",
        thumbnail_path
    ])

    return thumbnail_path