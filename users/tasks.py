from celery import shared_task


@shared_task
def send_sms_to_user(phone_number, otp):
    print(f' sms sent to {phone_number} : otp:{otp}')
    return True
