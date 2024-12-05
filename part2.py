import json
from datetime import datetime, timedelta
from db import fetch_all_records
from auth import get_service
from googleapiclient.discovery import build

def mark_as_read(service, email_id):
    """Marks an email as read.

    Args:
        service: The Gmail API service instance.
        email_id: The ID of the email to mark as read.
    """
    try:
        # Define the request body to modify the email's labels
        request_body = {
            'removeLabelIds': ['UNREAD']
        }
        # Call the Gmail API to modify the email
        service.users().messages().modify(userId='me', id=email_id, body=request_body).execute()
        print(f"Email {email_id} marked as read.")
    except Exception as e:
        print(f'An error occurred while marking email as read: {e}')

def mark_as_unread(service, email_id):
    """Marks an email as unread.

    Args:
        service: The Gmail API service instance.
        email_id: The ID of the email to mark as unread.
    """
    try:
        # Define the request body to modify the email's labels
        request_body = {
            'addLabelIds': ['UNREAD']
        }
        # Call the Gmail API to modify the email
        service.users().messages().modify(userId='me', id=email_id, body=request_body).execute()
        print(f"Email {email_id} marked as unread.")
    except Exception as e:
        print(f'An error occurred while marking email as unread: {e}')

def move_message(service, email_id, destination):
    """Marks an email as read.

    Args:
        service: The Gmail API service instance.
        email_id: The ID of the email to mark as read.
    """
    try:
        # Define the request body to modify the email's labels
        request_body = {
            'addLabelIds': [destination]
        }
        # Call the Gmail API to modify the email
        service.users().messages().modify(userId='me', id=email_id, body=request_body).execute()
        print(f"Email {email_id} moved email to {destination}")
    except Exception as e:
        print(f'An error occurred while moving email to {destination}: {e}')

# Function to evaluate conditions
def evaluate_condition(condition, email):
    field = condition['field']
    predicate = condition['predicate']
    value = condition['value']

    if field in ['From', 'Subject']:
        if predicate == 'Contains':
            return value in email[field]
        elif predicate == 'Does not Contain':
            return value not in email[field]
        elif predicate == 'Equals':
            return email[field] == value
        elif predicate == 'Does not equal':
            return email[field] != value
    elif field == 'Received Date/Time':
        threshold_date = datetime.now() - timedelta(days=int(value.split()[0]))
        if predicate == 'Greater than':
            return email[field] < threshold_date
        elif predicate == 'Less than':
            return email[field] > threshold_date

    return False

# Function to process rules
def process_rule(rule, email):
        email = {'id': email[0], 'From' : email[1], 'Subject': email[2], 'Received Date/Time' : email[3]}
        service = get_service()
        predicate = rule['predicate']
        conditions = rule['conditions']
        actions = rule['actions']

        # Evaluate conditions based on the predicate
        if predicate == 'All':
            if all(evaluate_condition(cond, email) for cond in conditions):
                for action in actions:
                    if action['action'] == 'Mark as read':
                        mark_as_read(service, email['id'])
                    elif action['action'] == 'Mark as unread':
                        mark_as_unread(service, email['id'])
                    elif action['action'] == 'Move Message':
                        move_message(service, email['id'], action['destination'])
        elif predicate == 'Any':
            if any(evaluate_condition(cond, email) for cond in conditions):
                for action in actions:
                    if action['action'] == 'Mark as read':
                        mark_as_read(service, email['id'])
                    elif action['action'] == 'Mark as unread':
                        mark_as_unread(service, email['id'])
                    elif action['action'] == 'Move Message':
                        move_message(service, email['id'], action['destination'])
            

def main():
    with open("rules.json", "r") as rules_file:
      rules = json.load(rules_file)['rules']
    choice = input("CHOOSE THE RULE YOU WANT TO PROCESS:")
    matches = list(filter(lambda x: x['rule_name'] == choice, rules))
    if len(matches) < 1:
        print("NO RULE FOUND WITH THE PROVIDED NAME")
        return
    rule = matches[0]
    emails = fetch_all_records()
    for email in emails:
        process_rule(rule, email)

if __name__ == "__main__":
    main()

