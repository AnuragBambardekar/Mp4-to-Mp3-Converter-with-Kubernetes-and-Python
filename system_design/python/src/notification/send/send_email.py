import smtplib, os, json
from email.message import EmailMessage
import ssl
import yagmail

print()

def notification(message):
    # try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]

        subject = "MP3 Download"
        content = f"mp3 file_id: {mp3_fid} is now ready!"

        yag = yagmail.SMTP(sender_address, sender_password)
        contents = ['This is the body, and here is just text']
        yag.send(to=receiver_address, subject = subject, contents = [content])

        print("Mail Sent")

    # except Exception as err:
    #     print(err)
    #     return err
    
# notification()