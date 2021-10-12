import moviepy.video.io.ImageSequenceClip
import moviepy.editor as mpe
import sys
import os
destinFolder = "VideoOut/"

def CleanDestinFolder():
    for x in os.listdir(destinFolder):
        os.remove(destinFolder + x)
    return

def combine_audio(vidname, audname, outname, fps=24):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)


text = sys.argv[1].split(".")[0]

fps=24
audname = "Audio/"+text+".wav"
out = "Final/Out.mp4"

image_files = [destinFolder+'/'+img for img in os.listdir(destinFolder) if img.endswith(".png")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
if text+'.wav' in os.listdir("Audio/"):
    audio_background = mpe.AudioFileClip(audname)
    final_clip = clip.set_audio(audio_background)
    final_clip.write_videofile(out)
else:
    print("No audio generated.")
    clip.write_videofile(out)
print("Video generated sucessfully....")

"""
CleanDestinFolder()"""