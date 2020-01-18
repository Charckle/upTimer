import smtplib
from email.message import EmailMessage

#{"smtp_server": "ns1.strojnica.com", "smtp_port": "465", "from_address": "email", "pass": "password123", "to_address": "to_email", "subject": "stuff", "body": "write something"}

def sendEmail(data):

    smtp_server = data["smtp_server"]
    smtp_port = data["smtp_port"]

    from_addr = data["from_address"]
    password = data["pass"]
    to_addr = data["to_address"]
    subject = data["subject"]
    body = data["body"]

    
    msg = EmailMessage()
    msg.add_header('from', from_addr)
    msg.add_header('to', to_addr)
    msg.add_header('subject', subject)
    msg.set_content(body)
    
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(from_addr, password)
    server.send_message(msg, from_addr=from_addr, to_addrs=to_addr)

