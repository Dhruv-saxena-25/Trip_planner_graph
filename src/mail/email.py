import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
from dotenv import load_dotenv
load_dotenv()
import os


def email_sender(destination_city: str, sender_id, result: str):
    # --- Configuration ---
    user = os.getenv('EMAIL')
    password = os.getenv('EMAIL_KEY')
    to_email = sender_id
    subject = f"🧳 Your Travel Itinerary for {destination_city} City."
    
    # Convert markdown to HTML
    html_content = markdown.markdown(result)
    
    # --- Build the Email ---
    msg = MIMEMultipart("alternative")
    msg['From'] = user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the HTML part
    msg.attach(MIMEText(html_content, 'html'))
    
     # --- Send the Email via Gmail SMTP ---
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(user, password)
            server.sendmail(user, to_email, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")