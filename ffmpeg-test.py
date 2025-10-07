from pathlib import Path
import tempfile
import subprocess

with tempfile.TemporaryDirectory() as tmpdir:
    source_video_path = (Path(tmpdir) / "my'file is 'here.mkv")
    source_video_path.write_text("Hello!")
    subtitle_path = source_video_path.with_suffix('.srt')
    subtitle_path.write_text("World!")
    
    video_filter = 'crop=1920:800:0:140' # Example starting filter

    # The subtitle path is formatted for the filter string
    # NOTE: My real code finds this path dynamically.
    #formatted_subtitle_path = str(subtitle_path).replace('\\', '/')
    formatted_subtitle_path = str(subtitle_path)

    # A simplified version of my style loop
    style_string = "FontName=Segoe UI,FontSize=18,PrimaryColour=&H00FFFFFF"

    # The filename is placed inside single quotes in the filter
    video_filter += f",subtitles=filename='{formatted_subtitle_path}':force_style='{style_string}'"

    # --- The final ffmpeg command list ---
    command = [
        'ffmpeg.exe',
        '-y',
        '-i', str(source_video_path),
        '-vf', video_filter,
        '-c:a', 'copy',
        'output.mkv',
    ]

    print("--- Generated FFmpeg Command ---")
    # Using print to show how Python sees the arguments before execution
    for i, arg in enumerate(command):
        print(f"Arg[{i}]: {arg}")

    # When run, ffmpeg fails on this command because of the ' in the filename.
    process = subprocess.run(command, text=True, capture_output=True)
    print("\n--- FFmpeg Output ---")
    print(process.stderr) 
