import json
import logging
import hmac
import hashlib
import os

# setup logging
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    "statusCode": 200,
    "headers": {"Content-Type": "application/json"},
    "body": json.dumps("ok"),
}
ERROR_RESPONSE = {"statusCode": 400, "body": json.dumps("Oops, something went wrong!")}

UNAUTH_REPSONSE = {
    "statusCode": 403,
    "body": json.dumps("Signature Verification Failed"),
}


def configure_message():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """


def notification(event, context):
    """
    Receives notification from API Gateway
    """
    logger.info(f"Event: {event}")

    return OK_RESPONSE


def eventsub_callback(event, context):
    """
    Receives eventsub callback from API Gateway
    """

    def is_signature_valid(event, headers):
        headers = event.get("headers")
        key = os.environ.get("CALLBACK_SECRET")
        computed_sig = hmac.new(
            key.encode(), msg=b"message", digestmod=hashlib.sha256,
        ).hexdigest()
        expected_header = f"sha256={computed_sig}"
        return expected_header == headers["Twitch-Eventsub-Message-Signature"]

    headers = event.get("headers")
    if headers["Twitch-Eventsub-Message-Type"] == "webhook_callback_verification":
        if is_signature_valid(event, headers):
            logger.info("Signature verified!")
            return OK_RESPONSE
        else:
            logger.warn("Signature verification failed!")
            return UNAUTH_REPSONSE

    return ERROR_RESPONSE
