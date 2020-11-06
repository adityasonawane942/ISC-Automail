from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

import csv


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


filename = "trialvirt.csv"
print("found")
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)

print("opned")
rows.pop(0)

for row in rows:
    email = row[2]
    print(email)
    # cert = row[1]
    # print(cert)
    # bibno = row[7]
    # print(bibno)
    # rl = row[8]
    # print(rl)
    # wl = row[9]
    # print(wl)

    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    print("WWWWWWWWW")

    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """

    # print("xxxxxxx")
    # message = MIMEText("Hello!<br><br>"
    #         "We congratulate you for achieving rank <b>" + row[1] + "</b> in your category in the Aavhan's Virtual Run, IIT Bombay 2020. However, for being eligible to claim prizes or E-certificate, we need to verify your identity. Please provide the following documents:<br>"
    #         "    1) Aadhar Card/ PAN card photo where your name and date of birth should be clearly visible.<br>"
    #         "    2) If you are a college student, college ID should be compulsorily sent.<br><br>"
    #         "Please do the needful at the earliest.<br><br>"
    #         "Thanks & Regards", 'html')
    # message['to'] = row[0]
    # message['from'] = "sadityam123@gmail.com"
    # message['subject'] = "Welcome to Aavhan, IIT Bombay's Virtual Run!"
    # msg = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    """Create a message for an email.

      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file_dir: The directory containing the file to be attached.
        filename: The name of the file to be attached.

      Returns:
        An object containing a base64url encoded email object.
      """
    message = MIMEMultipart()
    message['to'] = row[2]
    message['from'] = "sadityam123@gmail.com"
    message['subject'] = "Certificate of Participation | Aavhan Online Chess Tournament 2020"

    msg = MIMEText("Dear "+row[1]+",<br><br>"
            "Hi<br>"
            "Hope you are safe and doing well<br><br>"
            "The Post Graduate Sports Community is looking for opportunities to collaborate with "+row[0]+" for an Orientation Program to be conducted on 21st August with an attendance of 1300+ participants who are welcomed into the sporting legacy of IIT Bombay.<br><br>"
            "Attached below are the details regarding the Orientation Event and specifics about collaboration.<br><br>"
            "Feel free to contact us regarding any clarifications you may require.<br><br>"
            "Shani Saha<br>"
            "Post Graduate Sports Nominee<br>"
            "IIT Bombay<br>"
            "Ph No: 85752 12951", 'html')
    message.attach(msg)

    path = os.path.join("chess_normal", row[4])
    content_type, encoding = mimetypes.guess_type(path)
    print (content_type, encoding)

    if content_type is None or encoding is not None:
        print ("if")
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=row[4])
    message.attach(msg)
    tobesent = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    print("XXXXXXXXXX")
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """

    print("ZZZZZZZZZZ")
    try:
        message = (service.users().messages().send(userId='me', body=tobesent)
                   .execute())
        print('Message Id: %s' % message['id'])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)