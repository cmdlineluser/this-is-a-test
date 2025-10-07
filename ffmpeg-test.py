from pathlib import Path
import tempfile
import subprocess

with tempfile.TemporaryDirectory() as tmpdir:
    source_video_path = (Path(tmpdir) / "my'file is 'here.mkv")
    subprocess.run(
[
r'C:\Users\runneradmin\AppData\Local/Microsoft/WinGet/Links/ffmpeg.exe',
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
str(source_video_path)
]
)

    #source_video_path.write_text("Hello!")
    subtitle_path = source_video_path.with_suffix('.srt')
    subtitle_path.write_text("""1
00:00:02,000 --> 00:00:05,120
<font color="#ffffffff">This programme contains some</font>
    """)
    
    video_filter = 'crop=1920:800:0:140' # Example starting filter

    # The subtitle path is formatted for the filter string
    # NOTE: My real code finds this path dynamically.
    formatted_subtitle_path = str(subtitle_path).replace('\\', '/')
    formatted_subtitle_path = formatted_subtitle_path.replace(":", r"\\\:")
    #formatted_subtitle_path = str(subtitle_path)
    formatted_subtitle_path = formatted_subtitle_path.replace("'", r"\\\'")
    formatted_subtitle_path = formatted_subtitle_path.replace(" ", r"\\ ")

    # A simplified version of my style loop
    style_string = r'"FontName=Segoe\\ UI,FontSize=18,PrimaryColour=&H00FFFFFF"'

    # The filename is placed inside single quotes in the filter
    #video_filter += f',subtitles=filename="{formatted_subtitle_path}":force_style={style_string}'
    video_filter += f',subtitles=filename="{formatted_subtitle_path}"'

    # --- The final ffmpeg command list ---
    command = [
        r'C:\Users\runneradmin\AppData\Local/Microsoft/WinGet/Links/ffmpeg.exe',
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
