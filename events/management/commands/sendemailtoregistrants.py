from django.core.management.base import BaseCommand
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.mail import EmailMessage
from events.models import Event, Registrant


class Command(BaseCommand):
    help = "Sent an email to registrants"

    def add_arguments(self, parser):
        parser.add_argument('--event', dest='event_id', required=True, help='Event ID')

    def send_email_to_registrants(self, event_id):
        event = get_object_or_404(Event, pk=event_id)
        registrants = get_list_or_404(Registrant, event=event, is_email_sent=False)

        subject = "[%s] Su código de participante" % (event.title)

        draft_message = """
                        Puede registrarse en la aplicación usando el codigo: %s.
                        Si usted no se registró, ignore este mensaje."""

        for registrant in registrants:
            message = draft_message % (registrant.code)

            try:
                send_mail = EmailMessage(subject, message, to=[registrant.email])
                send_mail.send()
            except Exception as e:
                print(e)

            registrant.is_email_sent = True
            registrant.save()

    def handle(self, *args, **options):
        event_id = options['event_id']
        self.send_email_to_registrants(event_id)
