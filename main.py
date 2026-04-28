import imaplib
import email
import time
import requests
from email.header import decode_header

EMAIL = "itaienbot@gmail.com"
PASSWORD = "tmnwbcyizewatrbw"
BOT_TOKEN = "8716453924:AAFq4YDHxQlxHqakKbsA_SYyjyfkxSCrlCk"
CHAT_ID = "409155694"
CHECK_INTERVAL = 30
send_telegram("טסט - הבוט עובד!")

def send_telegram(message, photo=None):
    if photo:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        requests.post(url, data={"chat_id": CHAT_ID, "caption": message}, files={"photo": ("img.jpg", photo)})
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def check_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    _, msgs = mail.search(None, '(UNSEEN)')
    for num in msgs[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        photo = None
        for part in msg.walk():
            if part.get_content_type().startswith("image/"):
                photo = part.get_payload(decode=True)
                break
        send_telegram(f"🚨 התראת מצלמה!\n{subject}", photo)
        mail.store(num, "+FLAGS", "\\Seen")
    mail.logout()

print("הסקריפט התחיל לרוץ", flush=True)  # ← שורה 41
while True:
    try:
        print("בודק מיילים...", flush=True)  # ← אחרי try:
        check_emails()
        print("בדיקה הסתיימה", flush=True)  # ← אחרי check_emails()
    except Exception as e:
        print(f"שגיאה: {e}", flush=True)
    time.sleep(CHECK_INTERVAL)
