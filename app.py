from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3, os, json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from worker import generate_short, clip_long_video, upload_to_youtube

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'local-only-secret'
DB = 'data/automator.db'
os.makedirs('data', exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (user_id INTEGER, key TEXT, value TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY, user_id INTEGER, time TEXT, enabled INTEGER)''')
    conn.commit(); conn.close()

init_db()
scheduler = BackgroundScheduler(); scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username,password) VALUES (?,?)", (data['username'], data['password']))
    conn.commit(); conn.close()
    session['user'] = data['username']
    return jsonify({"ok":True})

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    # AI story generation - yahan OpenAI ya local model lagayen
    topic = data.get('topic', 'Motivation')
    theme = data.get('theme', 'Motivational')
    lang = data.get('lang', 'ur')
    
    # Simple template (aap OpenAI API se replace kar sakte hain)
    story = f"{topic} par ek short story: Zindagi me kamyabi ke liye roz 3 kaam karein. Pehla, shukr guzari. Dusra, mehnat. Teesra, sabr."
    if lang == 'en':
        story = f"Short story on {topic}: Success needs 3 habits daily: gratitude, hard work, and patience."
    
    # Save locally
    with open(f"data/last_story.txt", "w", encoding="utf-8") as f:
        f.write(story)
    
    return jsonify({"story": story})

@app.route('/api/schedule', methods=['POST'])
def set_schedule():
    times = request.json.get('times', [])
    # Clear old jobs
    for job in scheduler.get_jobs(): job.remove()
    for t in times:
        h,m = map(int, t.split(':'))
        scheduler.add_job(lambda: generate_short(), 'cron', hour=h, minute=m)
    return jsonify({"scheduled": times})

@app.route('/api/clip', methods=['POST'])
def api_clip():
    data = request.json
    channel_url = data['channel']
    clips_per = int(data.get('clips', 4))
    # Background me chalega
    clip_long_video(channel_url, clips_per)
    return jsonify({"started": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
