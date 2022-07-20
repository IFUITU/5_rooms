import smtplib
from pswrd import gmail, password

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content


# def send_email(data):
#     sent_from = gmail
#     to = ["tntcorporation@mail.ru"]
#     subject = "Room booking!"
#     body = "You booked a room!"


#     email_text = """\
#     From: %s
#     To: %s
#     Subject: %s
#     %s
#     """ % (sent_from, ", ".join(to), subject, body)

#     try:
#         smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         smtp_server.ehlo()
#         smtp_server.login(gmail, password)
#         smtp_server.sendmail(sent_from, to, email_text)
#         smtp_server.close()

#         print ("Email sent successfully!")

#     except Exception as ex:
#         print ("Something went wrong….",ex)

# send_email('s')

def send_email():
    my_sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    # Change to your verified sender

    from_email = Email("ifuitu@gmail.com")  
    to_email = To("tntcorporation@mail.ru")  

    subject = "Lorem ipsum dolor sit amet"
    content = Content("text/plain", "consectetur adipiscing elit")

    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = my_sg.client.mail.send.post(request_body=mail_json)


send_email()
