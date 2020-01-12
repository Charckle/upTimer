import smtplib
from email.message import EmailMessage


def sendEmail(subj,bod):
    from_addr = "server@razor.si"
    to_addr = "andrej.zubin@email.com"
    subject = subj
    body = bod
    
    msg = EmailMessage()
    msg.add_header('from', from_addr)
    msg.add_header('to', to_addr)
    msg.add_header('subject', subject)
    msg.set_content(body)
    
    server = smtplib.SMTP_SSL('ns1.strojnica.com', 465)
    server.login(from_addr, '9D&nEWn*O^@S')
    server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])

