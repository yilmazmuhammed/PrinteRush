import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_addr_list,
               subject, message, message_type="plain",
               from_addr="noreply@printerush.com",
               login='noreply@printerush.com', password=os.environ.get("NOREPLY_MAIL_PASSWORD"),
               smtpserver='mail.printerush.com:587'):
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = ','.join(to_addr_list)
    msg["Subject"] = subject
    body = MIMEText(message, message_type)
    msg.attach(body)

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, msg.as_string())
    server.quit()
    return problems


if __name__ == "__main__":
    send_email("noreply@printerush.com", ["mhyilmaz97@gmail.com"], "asd", "qwe")
