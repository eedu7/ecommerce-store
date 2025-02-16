import boto3
from botocore.exceptions import BotoCoreError, ClientError

from core.config import config
from core.exceptions import BadRequestException


class SESEmailSender:
    ses_client = boto3.client(
        "ses",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
    )

    @staticmethod
    def send_email(
        sender: str, recipient: str, subject: str, body_html: str, body_text: str
    ):
        try:
            response = SESEmailSender.ses_client.send_email(
                Source=sender,
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": body_text}, "Html": {"Data": body_html}},
                },
            )
            return response
        except (BotoCoreError, ClientError) as e:
            raise BadRequestException(f"Error sending email: {e}")
