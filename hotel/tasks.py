from celery import shared_task


@shared_task(queue='reservation')
def check_raservation():
    print(True)
    return True
