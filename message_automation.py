import time
from datetime import datetime

import holidays
import pandas as pd
from hugchat.login import Login

from config import EXCEL_FILE_PATH, HUGGING_CHAT_PASSWORD, HUGGING_CHAT_USERNAME
from utils import create_message, send_email, send_text_message


def send_greetings(excel_file, holidays_us):
    """
    Check and send a custom message to each contact that has a birthday today or everyone if it is a holiday today

    :param excel_file: the Excel file
    :param holidays_us: a list of all US holidays and their date
    """
    # Initialize the counters
    birthday_counter = 0
    holiday_counter = 0

    # Get today's date
    today = datetime.now().date()

    # Log in to huggingface and grant authorization to huggingchat
    sign = Login(HUGGING_CHAT_USERNAME, HUGGING_CHAT_PASSWORD)
    cookies = sign.login()

    # Loop through all contacts
    for index, row in excel_file.iterrows():

        # Gather contact info
        full_name = row["Name"]
        name = full_name.split(" ")[0]
        age = row["Age"]
        birthday = row["Birth Date"].date()
        agreed = row["Agreed to Subscription"]
        email = row["Email Address"] if str(row["Email Address"]) != "nan" else ""
        phone = row["Phone Number"] if str(row["Phone Number"]) != "nan" else ""
        death_date = row["Death Date"] if str(row["Death Date"]) != "NaT" else ""

        # Ensure that the contact has agreed to be messaged and that they have not passed away
        if agreed == "Yes" and not isinstance(death_date, str):

            # Initialize the notified
            notified = False

            # Check if it is their birthday today
            if birthday == today and (phone or email):

                # Create a custom happy birthday message using an AI
                message = create_message(
                    cookies=cookies,
                    name=name,
                    theme=f"Happy Birthday turning {age} old! (only the message, no ending signature)",
                )
                print(f"Message for {name}: {message}")

                # Send message via phone and email if present
                if phone:
                    send_text_message(phone_number=phone, message=message)
                    print(f"Successfully wished {name} happy birthday via text!")
                if email:
                    send_email(email_address=email, message=message)
                    print(f"Successfully wished {name} happy birthday via email!")

                # Update variables due to a successful notification
                birthday_counter += 1
                notified = True

            # Loop through all US Holidays
            for date, holiday_name in holidays_us.items():

                # Check if it is a US Holiday today
                if date == today and (phone or email):

                    # Create a custom holiday message using an AI
                    message = create_message(
                        cookies=cookies, name=name, theme=holiday_name + "  (only the message, no ending signature)"
                    )
                    print(f"Message for {name}: {message}")

                    # Send message via phone and email if present
                    if phone:
                        send_text_message(phone_number=phone, message=message)
                        print(f"Successfully wished {name} a happy {holiday_name} via text!")
                    if email:
                        send_email(email_address=email, message=message)
                        print(f"Successfully wished {name} a happy {holiday_name} via email!")

                    # Update variables due to a successful notification
                    holiday_counter += 1
                    notified = True

            # If this contact was notified, print a separator row
            if notified:
                print()

    # Display how many people were notified today
    if birthday_counter or holiday_counter:
        print(f"{birthday_counter} contacts successfully wished happy birthday!")
        print(f"{holiday_counter} contacts successfully wished a happy holiday!\n")
    else:
        print("It was no one's birthday and it was not a US holiday today.\n")


# Load the Excel file
df = pd.read_excel(EXCEL_FILE_PATH)

# Create a list of United States holidays
us_holidays = holidays.US(years=datetime.now().year)

# Run this loop non-stop
while True:

    # Get the current time
    now = datetime.now()

    # Check to see if it is between midnight and 1:00 AM
    if now.hour == 0:

        # Send a message for applicable scenarios
        send_greetings(df, us_holidays)

    # Sleep for 1 hour to avoid constantly checking
    time.sleep(3600)
