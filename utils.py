import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from hugchat import hugchat
from hugchat.message import Message
from twilio.rest import Client

from config import EMAIL_PASSWORD, EMAIL_SENDER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SENDER_PHONE


def send_text_message(*, phone_number: str, message: str):
    """
    Function to send a text message using Twilio

    :param phone_number: a contact's phone number
    :param message: a custom message for the contact
    :return: True/ False if the message was successfully delivered
    """

    try:
        # Send the text message
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(body=message, from_=TWILIO_SENDER_PHONE, to=phone_number)

        print(f"Successfully sent text message to {phone_number}.")
        return True

    except Exception as e:
        print(f"Failed to send text message to {phone_number}. Error: {str(e)}")
        return False


def send_email(*, email_address: str, message: str):
    """
    Function to send an email using SMTP

    :param email_address: a contact's email address
    :param message: a custom message for the contact
    :return: True/ False if the message was successfully delivered
    """
    try:
        # Initialize the email server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        # Set up the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email_address
        msg["Subject"] = "Contact Info Subscription"
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(EMAIL_SENDER, email_address, msg.as_string())
        server.quit()

        print(f"Successfully sent email to {email_address}.")
        return True

    except Exception as e:
        print(f"Failed to send email to {email_address}. Error: {str(e)}")
        return False


def create_message(*, cookies, name: str, theme: str = "", message: str = "") -> str:
    """
    Function to send a prompt to an AI and received a custom message back.

    :param cookies: A login connection for the chatbot AI
    :param name: a contact's full name
    :param theme: Happy Birthday or a US Holiday name
    :param message: If provided, will not use the default prompt
    :return: a custom message using the name and theme
    """

    # Create a ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    if message:
        # Ask the chatbot the provided message
        response = chatbot.chat(text=message)
        Message.wait_until_done(response)
        return response.text
    else:
        # Ask the chatbot a prompt
        prompt = f"Compose a short pleasant message for {name} with about '{theme}'."
        response = chatbot.chat(prompt)
        Message.wait_until_done(response)
        return response.text
