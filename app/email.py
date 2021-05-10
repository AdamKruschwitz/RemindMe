from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_phone_verification(phone_number, link):
    text = 'Remind me verification link: ' + link + '/n If you did not request this verification, please disregard this message'
    recipient = phone_number + '@vtext.com'
    send_email("Remind Me Verification", "remindmesmsbot@gmail.com", [recipient], text, "")
