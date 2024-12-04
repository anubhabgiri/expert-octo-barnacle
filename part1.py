from auth import get_service
from db import create_records, create_table, connect_db
import re
from dateutil import parser

def fetch_emails(service, maxResults: int=200):
    """Fetches the user's email messages.

    Args:
        service: The Gmail API service instance.

    Returns:
        List of email snippets.
    """
    try:
        results = service.users().messages().list(userId='me', maxResults=maxResults).execute()
        messages = results.get('messages', [])
        email_snippets = []

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_snippets.append(msg)  # Get the email snippet

        return email_snippets
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

def parse_date(date_str):
    try:
        # Try to parse the date string into a datetime object
        return parser.parse(date_str)
    except (ValueError, TypeError):
        # Return None if parsing fails
        return None

def extract_email(string: str):
    pattern = "<\S+@\S+>"
    match = re.search(pattern, string)
    if match:
        string = match.group().replace(">", "").replace("<", "")
    return string

def extract_email_info(messages):
    email_list = []
    
    for message in messages:
        email_info = {}
        headers = message['payload']['headers']
        
        # Extract headers into a dictionary for easier lookup
        header_dict = {header['name'].lower(): header['value'] for header in headers}
        
        # Get the required fields, using get() to handle missing fields gracefully
        email_from = extract_email(header_dict.get('from', '')).lower()
        # email_to = extract_email(header_dict.get('to', '')).lower()
        email_subject = header_dict.get('subject', '')
        email_date = parse_date(header_dict.get('date', ''))
        email_id = message['id']
        
        email_info = (email_id, email_from, email_subject, email_date)

        email_list.append(email_info) # change this to tuple
    
    return email_list
def main():
    try:
        print("TESTING DATABASE CONNECTION..")
        connection = connect_db()
        print("SUCCESSFULLY CONNECTED")
    except Exception as e:
        print(f"COULD NOT CONNECT TO DATABASE {e}")
        return

    # creating table if not exists
    create_table()
    
    # Get user input with a question
    print("""
    WELCOME TO FIRST PART OF THE STANDALONE PYTHON APPLICATION. HERE WE WILL FETCH EMAILS FROM GMAIL USING
    OAUTH WITH THE CREDENTIALS PROVIDED.    

    """)
    user_input = input("How many emails do you want to fetch (max 200 allowed): ")

    try:
        num_emails = min(int(user_input), 200)
        service = get_service()
        emails = fetch_emails(service, num_emails)
        print("emails fetched")
        prepared_emails = extract_email_info(emails)
        print("emails prepared", prepared_emails)
        create_records(prepared_emails)
        print("SUCCESSFULLY FETCHED EMAILS...")
    except Exception as e:
        print(f"error {e}")


if __name__ == '__main__':
    main()
