import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "xrgl zyri ftyp aedz"
SENDER = "python.test20002@gmail.com"
RECEIVER = "python.test20002@gmail.com"
def send_email(image_path):
     print("send_email function started")
     email_message = EmailMessage()
     email_message["Subject"] = "Alert: Motion detected in the monitored area!"
     email_message.set_content("Movement detected in the camera's view.")

     with open(image_path, "rb") as file:
          content = file.read()
     email_message.add_attachment(content, maintype = "image", subtype = imghdr.what(None, content))

     gmail = smtplib.SMTP("smtp.gmail.com", 587)
     gmail.ehlo()
     gmail.starttls()
     gmail.login(SENDER, PASSWORD)
     gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
     gmail.quit()
     print("send_email function ended")


if __name__ == "__main__":
     send_email(image_path="images/20.png")