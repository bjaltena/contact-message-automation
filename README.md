# contact-message-automation
Message friends and family automatically for their birthdays and holidays.


## Expected Credentials
- TWILIO_ACCOUNT_SID = ""
- TWILIO_AUTH_TOKEN = ""
- TWILIO_SENDER_PHONE = ""
- EMAIL_SENDER = ""
- EMAIL_PASSWORD = ""
- HUGGING_CHAT_USERNAME = ""
- HUGGING_CHAT_PASSWORD = ""
- EXCEL_FILE_PATH = ""

The following accounts are needed to implement the contact message automation 
project, Twilio, Email, and Hugging Chat.
- Twilio sign up can be found [here](https://www.twilio.com/try-twilio).
- Hugging Chat sign up can be found [here](https://huggingface.co/chat/).
- If using Gmail, the app password tutorial
can be found [here](https://support.google.com/accounts/answer/185833?hl=en). 


## Expected Excel File Headers
- Name *
- Birth Date *
- Death Date
- Age *
- Email Address
- Phone Number
- Invited? *
- Agreed to Subscription *

`*` Signals that a value is required for this column each row.

The `Invited?` and `Agreed to Subscription` columns should have a value 
of `Yes` or `No`.