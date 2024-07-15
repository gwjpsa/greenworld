from email.message import EmailMessage
import ssl
import smtplib

def sendNotificationMail(
    subject,
    body,
    emailSmtp = 'smtp.gmail.com',
    port = 465,
    sender = 'sig.greenworld@gmail.com',
    pwd = 'glnmgaqjezivcuay',
    #receiver = ['rhcsilva@gmail.com', 'jooaosa@gmail.com'],
    receiver = ['jooaosa@gmail.com'],
    ):
    
    """
    por defeito, sender = sig.greenworld@gmail.combinations
    receivers: Ricardo e João
    """
    
    email_sender = sender
    email_pwd = pwd
    email_receiver = receiver

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context = context) as smtp:
        smtp.login(email_sender, email_pwd)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
    print('Email enviado com sucesso!')
    
subject = 'Teste função'
body = """
teste função
"""

sendNotificationMail(subject, body)