import os
import time
from flask import Flask, request
from google import genai
import requests

app = Flask(__name__)

# --- ⚙️ CONFIGURATION ---
# 🔑 Reminder: Replace this with your key for local testing, 
# but use "PASTE_YOUR_KEY_HERE" when uploading to GitHub!
GEMINI_KEY = "PASTE_YOUR_KEY_HERE" 
client = genai.Client(api_key=GEMINI_KEY)

traffic_history = []

def call_detective_ai(logs):
    """Refined AI call with error handling. Gracefully handles rate limits."""
    prompt = f"Analyze these timestamps: {logs}. If a visitor clicks more than 3 times in 10 seconds, they are a BOT. Answer only 'BOT' or 'HUMAN'."
    
    try:
        # Using the most stable model name for 2026
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return response.text.strip().upper()
    except Exception as e:
        # This handles 429 Quota errors or 401 Key errors without crashing
        print(f"📡 System Note: AI Analysis bypassed due to rate-limit. Defaulting to BOT-trap mode.")
        return "BOT" 

@app.route("/secret-treasure-vault", methods=["GET", "POST"])
def the_trap():
    ip = request.remote_addr
    now = time.time()
    traffic_history.append(now)
    
    # 1. SHOW LOGIN PAGE (GET Request)
    if request.method == "GET":
        return f"""
        <html>
        <body style="background-color:#0d1117; color:#58a6ff; font-family:sans-serif; text-align:center; padding-top:100px;">
            <div style="border: 1px solid #30363d; display:inline-block; padding:40px; border-radius:10px; background:#161b22;">
                <h2 style="color:#ffffff;">🔐 Secure Internal Vault</h2>
                <p style="color:#8b949e;">Restricted Area - Unauthorized Access Prohibited</p>
                <form method="POST">
                    <input type="text" placeholder="Username" style="display:block; margin:10px auto; padding:10px; width:200px; border-radius:5px; border:1px solid #30363d; background:#0d1117; color:white;"><br>
                    <input type="password" placeholder="Password" style="display:block; margin:10px auto; padding:10px; width:200px; border-radius:5px; border:1px solid #30363d; background:#0d1117; color:white;"><br>
                    <button type="submit" style="background:#238636; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold;">Login</button>
                </form>
            </div>
        </body>
        </html>
        """

    # 2. ANALYZE LOGIN ATTEMPT (POST Request)
    recent_logs = traffic_history[-5:]
    if len(recent_logs) >= 3:
        verdict = call_detective_ai(str(recent_logs))
        if "BOT" in verdict:
            print(f"🤖 [TRAP] Bot detected from {ip}. Redirecting to maze.")
            return f"""
            <body style="background-color:#1a1a1a; color:#00ff00; font-family:sans-serif; text-align:center; padding-top:100px;">
                <h1>🛡️ SYSTEM: BRUTE-FORCE DETECTED</h1>
                <p>Security protocols bypassed. Initializing admin session...</p>
                <a href='/secret-treasure-vault/1' style="color:white; font-weight:bold;">[ CLICK HERE TO ACCESS DATABASE ]</a>
            </body>
            """

    return "<h1 style='color:red; text-align:center;'>ERROR: Invalid Credentials</h1><p style='text-align:center;'><a href='/secret-treasure-vault' style='color:gray;'>Try Again</a></p>", 401

@app.route("/secret-treasure-vault/<int:level>")
def infinite_maze(level):
    """The deception sinkhole that keeps the bot busy."""
    # Log progress for forensics
    with open("trophy_room.txt", "a") as f:
        f.write(f"Intruder reached Level {level} at {time.ctime()}\n")

    fake_key = f"SECRET-DATA-PART-{level}-{int(time.time())}"
    return f"""
    <html>
    <body style="background-color:black; color:green; font-family:monospace; padding: 50px;">
    <h1 style="color:lime;">🗄️ INTERNAL DATABASE - LEVEL {level}</h1>
    <hr color="green">
    <p>> Successfully decrypted fragment {level}...</p>
    <p>> [FRAGMENT]: {fake_key}</p>
    <br>
    <a href='/secret-treasure-vault/{level+1}' style="color:yellow; font-size: 18px; text-decoration:none;">[ >> DOWNLOAD NEXT DATA FRAGMENT << ]</a>
    <p style="color: #222; margin-top: 150px;">AI-Guardian v1.2 Monitoring Active</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("\n🚀 AI GUARDIAN IS LIVE")
    print("URL: http://127.0.0.1:5000/secret-treasure-vault\n")
    app.run(host="0.0.0.0", port=5000)
