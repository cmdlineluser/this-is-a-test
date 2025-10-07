from pathlib import Path
import tempfile
import subprocess

ffmpeg = r'C:\Users\runneradmin\AppData\Local/Microsoft/WinGet/Links/ffmpeg.exe'
with tempfile.TemporaryDirectory() as tmpdir:
    filename = "m@~[]\"y'file is 'here.mkv"
    source_video_path = (Path(tmpdir) / filename)

    #source_video_path.write_text("Hello!")
    subtitle_path = source_video_path.with_suffix('.srt')
    subtitle_path.write_text("""1
00:00:02,000 --> 00:00:05,120
<font color="#ffffffff">This programme contains some</font>
    """)
    
    video_filter = 'crop=1920:800:0:140' # Example starting filter

    # The subtitle path is formatted for the filter string
    # NOTE: My real code finds this path dynamically.
    escaped_filename = str(filename).replace("\\", "/")
    for char in "'[]:":
        escaped_filename = escaped_filename.replace(char, rf"\\\{char}")
    formatted_subtitle_path = str(subtitle_path).replace("\\", "/")
    for char in "'[]:":
        formatted_subtitle_path = formatted_subtitle_path.replace(char, rf"\\\{char}")


    # A simplified version of my style loop
    style_string = r"'FontName=Segoe UI,FontSize=18,PrimaryColour=&H00FFFFFF'"

    # The filename is placed inside single quotes in the filter
    #video_filter += f',subtitles=filename="{formatted_subtitle_path}":force_style={style_string}'
    video_filter += f',subtitles=filename={formatted_subtitle_path}:force_style={style_string}'

    subprocess.run([
        ffmpeg,
        '-f',
        'lavfi',
        '-i',
        'smptehdbars=s=1920x1080:r=25,format=yuv420p',
         '-c:v', 
        'libx264',
        '-b:v',
        '3500k',
        '-crf:v',
        '23',
        '-t', 
        '10',
        '-y',
        str(escaped_filename)
    ])

    # --- The final ffmpeg command list ---
    command = [
            ffmpeg,
        '-y',
        '-i', str(escaped_filename),
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

