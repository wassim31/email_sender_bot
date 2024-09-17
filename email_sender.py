import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
import sys

# Email body with a placeholder for the name
email_body = """
Hello {name}

I am Wassim boussebha

Thank you,
"""

# Read email credentials from command-line arguments
def get_credentials():
    if len(sys.argv) != 4:
        print("Usage: python email_sender.py <email_sender> <email_password> <csv_file>")
        sys.exit(1)
    email_sender = sys.argv[1]
    email_password = sys.argv[2]
    csv_file = sys.argv[3]
    return email_sender, email_password, csv_file

# Email credentials from command-line arguments
email_sender, email_password, csv_file = get_credentials()

# SMTP Server setup
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Read the CSV file
def read_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

# Send an email to a single recipient
def send_email(name, recipient_email):
    try:
        # Validate email address
        validate_email(recipient_email)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = recipient_email
        msg['Subject'] = "Recherche d'un stage de fin d'etude"

        # Replace the name placeholder in the email body
        body = email_body.format(name=name if name.strip() else "")
        
        # Attach the body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())

        print(f"Email sent to {recipient_email}")

    except EmailNotValidError as e:
        print(f"Invalid email address {recipient_email}: {e}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Send emails to a list from the CSV file
def send_bulk_emails(csv_file):
    contacts = read_csv(csv_file)
    if contacts is not None:
        for _, row in contacts.iterrows():
            name = row['Name']
            email = row['Email']
            # Send email with an empty string if name is missing
            send_email(name if pd.notna(name) and name.strip() != "" else "", email)

# Run the script
if __name__ == "__main__":
    send_bulk_emails(csv_file)

