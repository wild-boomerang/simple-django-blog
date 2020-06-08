from django.core.mail import send_mail
from multiprocessing import Process, Manager
# from static_vars import static_vars

from BlogSite.settings import EMAIL_HOST


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def process_sent_queue(queue):
    while True:
        if not queue.empty():
            address, subject, message = queue.get()
            send_mail(subject, message, EMAIL_HOST, [address], False)


@static_vars(IS_ACTIVE=False)
def send_email_multiproc(address, subject, message):
    if not send_email_multiproc.IS_ACTIVE:
        send_email_multiproc.queue = Manager().Queue()
        process = Process(target=process_sent_queue, args=(send_email_multiproc.queue,))
        process.daemon = True
        process.start()
        send_email_multiproc.IS_ACTIVE = True

    send_email_multiproc.queue.put((address, subject, message))
