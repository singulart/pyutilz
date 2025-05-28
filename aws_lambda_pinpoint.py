import boto3
import logging
import re

client = boto3.client('pinpoint-sms-voice-v2')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def normalize_us_phone_number(phone):
    """
    Validates and normalizes a US phone number.
    Adds +1 only if it's not already present.
    
    Args:
        phone (str): The phone number string.
        
    Returns:
        str or None: Normalized phone number with +1 or None if invalid.
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if digits.startswith('1') and len(digits) == 11:
        # Already has country code
        return f'+{digits}'
    elif len(digits) == 10:
        # Add country code
        return f'+1{digits}'
    else:
        # Invalid phone number format
        return None

def get_origination_identity_id(phone_number):
    """
    Finds the PhoneNumberId associated with the given phone number (E.164 format).
    """
    try:
        paginator = client.get_paginator('describe_phone_numbers')
        for page in paginator.paginate():
            for number in page.get('PhoneNumbers', []):
                if number.get('PhoneNumber') == phone_number:
                    return number.get('PhoneNumberId')
    except Exception as e:
        logger.error(f"Failed to list phone numbers: {str(e)}")
        return None
    return None

def lambda_handler(event, context):
    originator_number = event.get("from")
    message = event.get("message")
    recipients = event.get("recipients", [])

    if not originator_number or not message or not recipients:
        return {
            "statusCode": 400,
            "body": "Missing required fields: 'from', 'message', or 'recipients'"
        }

    origination_identity = get_origination_identity_id(originator_number)
    if not origination_identity:
        return {
            "statusCode": 404,
            "body": f"Origination phone number {originator_number} not found or not provisioned in Pinpoint SMS Voice V2"
        }

    responses = []

    for recipient in recipients:
        phone_number = recipient.get("endpoint")
        firstname = recipient.get("firstname", "")
        lastname = recipient.get("lastname", "")

        if not phone_number or not normalize_us_phone_number(phone_number):
            logger.warning(f"Skipping recipient {firstname} {lastname} due to missing phone number.")
            continue

        norm_phone = normalize_us_phone_number(phone_number)

        try:
            response = client.send_text_message(
                DestinationPhoneNumber=norm_phone,
                OriginationIdentity=origination_identity,
                MessageBody=message,
                MessageType='TRANSACTIONAL'
            )
            logger.info(f"Sent message to {firstname} {lastname} ({norm_phone})")
            responses.append({
                "recipient": f"{firstname} {lastname}",
                "phone_number": norm_phone,
                "message_id": response.get("MessageId")
            })
        except Exception as e:
            logger.error(f"Error sending to {phone_number}: {str(e)}")
            responses.append({
                "recipient": f"{firstname} {lastname}",
                "phone_number": phone_number,
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "results": responses
    }


