from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.db.models.signals import post_save
from login_system.models import CalendarModel, CustomerUserProfile

SCOPES_F = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES_F)
    return build('calendar', 'v3', credentials=credentials)

@receiver(post_save, sender=CustomerUserProfile)
def create_calendar_for_doctor(sender, instance, **kwargs):
    if instance.user_type == 'doctor' and not instance.calendar_id:
        service = get_google_calendar_service()
        
        calendar = {
            'summary': f' {instance.username} {instance.first_name} {instance.last_name}  Calendar',
            'timeZone': 'Asia/Kathmandu'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()
        instance.calendar_id = created_calendar['id']
        instance.save()

        CalendarModel.objects.create(
            doctor=instance,
            calendar_id=created_calendar['id'],
            summary=created_calendar['summary'],
            timezone=created_calendar['timeZone']
        )
        
        print("Calendar created successfully for doctor.")
