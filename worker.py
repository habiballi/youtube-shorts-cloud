import os, random
from gtts import gTTS
from moviepy.editor import *
from datetime import datetime

# YouTube upload function
def upload_to_youtube(video_path, title, description):
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=creds)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": ["Shorts", "AI"],
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
        },
        media_body=video_path
    )
    response = request.execute()
    return response

def generate_short(topic="Motivation", lang="ur"):
    # 1. Story (already saved)
    with open("data/last_story.txt", "r", encoding="utf-8") as f:
        story = f.read()
    
    # 2. Audio TTS
    tts_lang = 'ur' if lang=='ur' else 'en'
    tts = gTTS(story, lang=tts_lang)
    audio_path = f"data/audio_{datetime.now().strftime('%H%M%S')}.mp3"
    tts.save(audio_path)
    
    # 3. Video banayein - simple background + text
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Background color clip (9:16 for shorts)
    clip = ColorClip(size=(1080,1920), color=(15,23,42), duration=duration)
    txt = TextClip(story[:100], fontsize=70, color='white', size=(900, None), method='caption').set_duration(duration).set_position('center')
    video = CompositeVideoClip([clip, txt]).set_audio(audio)
    
    output = f"data/short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac')
    
    # 4. Auto upload
    title = f"{topic} - {datetime.now().strftime('%d %b')}"
    upload_to_youtube(output, title, story)
    return output

def clip_long_video(channel_url, clips_per=4):
    import yt_dlp
    # Download latest video
    ydl_opts = {'format': 'best', 'outtmpl': 'data/long.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=True)
    
    video = VideoFileClip("data/long.mp4")
    duration = video.duration
    clip_len = 45
    
    for i in range(clips_per):
        start = random.randint(30, int(duration - clip_len - 30))
        sub = video.subclip(start, start+clip_len)
        # Resize for shorts
        sub_resized = sub.resize(height=1920).crop(x_center=sub.w/2, width=1080, height=1920)
        out = f"data/clip_{i+1}.mp4"
        sub_resized.write_videofile(out, codec='libx264', audio_codec='aac')
        upload_to_youtube(out, f"Clip {i+1} - {info.get('title','')}", "Auto clipped")
