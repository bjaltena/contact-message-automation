import pandas as pd
from hugchat.login import Login

from config import EXCEL_FILE_PATH, HUGGING_CHAT_PASSWORD, HUGGING_CHAT_USERNAME
from utils import create_message, send_email


def send_invitation_message(excel_file) -> int:
    """
    Send an invitation to each contact listed in the Excel file

    :param excel_file: the Excel file
    :return: a number representing how many successful notifications were sent
    """

    # Initialize the success counter
    success_counter = 0

    # Log in to huggingface and grant authorization to huggingchat
    sign = Login(HUGGING_CHAT_USERNAME, HUGGING_CHAT_PASSWORD)
    cookies = sign.login()

    # Loop through each row with data
    for index, row in excel_file.iterrows():
        try:
            # Gather contact info
            full_name = row["Name"]
            name = full_name.split(" ")[0]
            invited = row["Invited?"]
            email = row["Email Address"] if str(row["Email Address"]) != "nan" else ""
            death_date = row["Death Date"] if str(row["Death Date"]) != "NaT" else ""
            # phone = row['Phone Number'] if str(row["Phone Number"]) != "nan" else ""

            # Check if they have not been invited yet, have a valid form of contacting them, and have not passed away
            if invited == "No" and email and not death_date:

                # Create a custom message using the contact name
                interesting_fact = create_message(
                    cookies=cookies,
                    name=name,
                    message=f"Please provide one short interesting fact about my name, {name}, with no greeting.",
                )
                print(f"Interesting fact for {name}: {interesting_fact}")

                # Set up the invitation message
                message = (
                    f"\n"
                    f"Hello {name}, Welcome to the Contact Automation Subscription Service. If you agree, I will send "
                    f"you a pleasant holiday and happy birthday message on the correct day. Respond with YES to "
                    f"opt into the service or NO to receive no more messages.\n\nFor fun, here is one interesting fact "
                    f"about your name:\n{interesting_fact}"
                )

                # Since Twilio is a free-trial, unable to text unverified numbers
                # if phone:
                #     # Text the contact
                #     if send_text_message(phone_number=phone, message=message):
                #
                #         # Update their invited column
                #         excel_file.at[index, 'Invited?'] = 'Yes'
                #         print(f"Successfully invited {name} via text message!")

                if email:
                    # Email the contact
                    if send_email(email_address=email, message=message):

                        # Update their invited column
                        excel_file.at[index, "Invited?"] = "Yes"
                        print(f"Successfully invited {name} via email!")

                # Increment the success counter and print a separator row
                success_counter += 1
                print()

            else:
                # Display whether the current contact has been invited or if they were ineligible
                if invited == "Yes":
                    print(f"{name} has already been invited!\n")
                else:
                    print(f"{name} is not eligible to be invited.\n")

        # Capture any unhandled exceptions
        except Exception as e:
            print(f"Unexpected Exception. Error: {e}")

    # Return how many contacts were notified
    return success_counter


# Load the Excel file
df = pd.read_excel(EXCEL_FILE_PATH)

# Send the one-time invitation message to each contact
successes = send_invitation_message(df)

# Display how many people were successfully notified
print(f"{successes} contacts successfully invited!")

# Save the updated DataFrame back to the Excel file
df.to_excel(EXCEL_FILE_PATH, index=False)
