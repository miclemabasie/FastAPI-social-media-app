from email_validator import validate_email, EmailNotValidError

def validate_user_email(email):
    """Checks to make sure that user inputs a valid email address"""

    try:
        value = validate_email(email)

        # get the email address
        email = value.email
        return True
    except EmailNotValidError as e:
        # Email is not valid, Exception msg is human-readable
        return False