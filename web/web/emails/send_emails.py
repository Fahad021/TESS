import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from python_http_client.exceptions import (BadRequestsError, UnauthorizedError, TooManyRequestsError,
                                           PayloadTooLargeError, ServiceUnavailableError, InternalServerError,
                                           UnsupportedMediaTypeError, NotFoundError, ForbiddenError)


def send_email(alert_type, notification_message, email_address):
    '''sendgrid email setup'''

    message = Mail(
        from_email=os.getenv('EMAIL_ADDRESS'),
        to_emails=email_address
    )

    message.dynamic_template_data = {
        "subject": "TESS Notification: " + alert_type + " alert",
        "notification_message": notification_message
    }

    message.template_id = os.environ.get('SENDGRID_NOTIFICATION_TEMPLATE_ID')

    try:

        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)

    except (BadRequestsError, UnauthorizedError, NotFoundError, PayloadTooLargeError,
            TooManyRequestsError, UnsupportedMediaTypeError, ServiceUnavailableError,
            InternalServerError, ForbiddenError) as e:

        print(e.body)
