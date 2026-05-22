# YouTube Shorts Automator - Local Website

Ye pura system aapke laptop par chalega. Data 100% local save hoga (SQLite database).

## Features jo aapne mange:
- Login / Signup (local)
- YouTube channel manager access (OAuth 2.0)
- AI assistant jo story likhe, caption banaye, audio lagaye
- Daily 3-4 Shorts auto upload (user-defined timing)
- Personalize: topics, themes, images, videos
- Long video clipping: kisi specific channel ki new video se auto clips

## Tech Stack
- Frontend: HTML, CSS, JavaScript (dashboard aapke pass hai)
- Backend: Python Flask (PHP ki jagah - kyunki video/AI ke liye Python best hai)
- Database: SQLite (data aapke laptop me)
- Video: MoviePy + FFmpeg
- Audio: gTTS (Urdu/English) ya ElevenLabs API
- YouTube: google-api-python-client

## Setup (Windows)
1. Python 3.10+ install karein
2. FFmpeg install karein: https://ffmpeg.org
3. CMD me:
   pip install -r requirements.txt
4. YouTube API credentials lein:
   - console.cloud.google.com > APIs > YouTube Data API v3 enable
   - OAuth Client ID (Desktop App) download karein -> client_secret.json is folder me rakhein
5. Run:
   python app.py
6. Browser me: http://localhost:5000

Data save location: ./data/automator.db
