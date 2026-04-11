from celery import shared_task
import time

@shared_task
def sent_emails():
    for i in range(10):  
        print(f"Sending email {i}")
        time.sleep(1)
    return "Emails sent!"

