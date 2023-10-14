import imaplib
import email
import csv
import html2text
from bs4 import BeautifulSoup
import re

# Your Gmail credentials
username = 'aayushsenapati2002@gmail.com'
password = 'suxo pivx waqx ohde'

# Connect to Gmail using IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, password)

# Select the mailbox you want to fetch emails from (e.g., 'inbox')
mail.select('inbox')

# Search for the latest 1000 emails
result, data = mail.uid('search', None, 'ALL')
email_uids = data[0].split()
email_uids = email_uids[-1000:]  # Retrieve the latest 1000 emails

# Create a CSV file to store email data
csv_file = 'demails.csv'

# Function to extract text from email content
def extract_text_from_email(msg):
    text = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            content=BeautifulSoup(part.get_payload(decode=True).decode("utf-8", errors="ignore"),'html.parser').get_text()
            text += content
    return text

# Initialize the CSV file with headers
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject', 'From', 'Date', 'Content'])

# Retrieve and save email content to the CSV file
for uid in email_uids:
    result, email_data = mail.uid('fetch', uid, '(RFC822)')
    raw_email = email_data[0][1]

    # Parse the raw email data
    parsed_email = email.message_from_bytes(raw_email)
    """print(parsed_email)
    break"""

    # Extract relevant information (you can customize this based on your needs)
    subject = parsed_email['subject']
    sender = parsed_email['from']
    date = parsed_email['date']

    # Extract text content from the email
    content = extract_text_from_email(parsed_email)

    # Append the email data to the CSV file
    with open(csv_file, 'a', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([' '.join(content.split())])

# Close the IMAP connection
mail.logout()

print(f"Retrieved and saved {len(email_uids)} emails to {csv_file}")