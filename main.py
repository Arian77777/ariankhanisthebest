import psutil
import geocoder
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = "arianaka2024@gmail.com"
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"

def get_status():
    # Get battery
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged

    # Get IP location (not GPS)
    location = geocoder.ip('me')
    latlng = location.latlng if location.ok else ['Unknown', 'Unknown']

    return f"""
    🔋 Battery: {percent}% {'Charging' if plugged else 'Not Charging'}
    📍 Location (approx): Latitude {latlng[0]}, Longitude {latlng[1]}
    """

def send_email():
    status = get_status()

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = "Hourly Device Report"
    msg.attach(MIMEText(status, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule it
schedule.every(1).hours.do(send_email)

# Initial send
send_email()

while True:
    schedule.run_pending()
    time.sleep(10)
