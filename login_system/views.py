import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication 
from rest_framework.authtoken.models import Token
from login_system.models import BlogModel, Category, CustomerUserProfile
from login_system.serializers import AppointmentSerializer, BlogSerializer, CategorySerializer, CustomLoginSerializer, CustomRegisterSerializer, UserSerailizer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from oauth2_provider.views.generic import ProtectedResourceView
from .models import Appointment, Event, CalendarModel
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pytz
from django.shortcuts import render
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from .models import Event  
from django.utils import timezone
import datetime

import dateutil.parser

class CustomRegisterView(APIView):
    def post(self, request):
        print(request.data['password1'])
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
           
            
            return Response({'message': 'Successfully Registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "token": str(refresh.access_token),
            })
        return Response({"detail": "Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)

class PatientDashboardView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        display_object = None
        print(user)
        if user.user_type == 'patient':
            display_object = CustomerUserProfile.objects.filter(user_type = 'doctor')
        print(display_object)
        serializer = UserSerailizer(display_object, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        display_object = CustomerUserProfile.objects.get(user=user)
        context = {
            'id': display_object.id,
            'username': display_object.user.username,
            'email': display_object.user.email,
            'city': display_object.city
        }
        return Response(context, status=status.HTTP_200_OK)

class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(context, status=status.HTTP_200_OK)



class BlogView(APIView):

    def get(self, request):
        if request.user.user_type == 'doctor':
            blogs = BlogModel.objects.filter(user=request.user)
        elif request.user.user_type == 'patient':
            blogs = BlogModel.objects.filter(status='published')
        else:
            blogs = BlogModel.objects.none() 

        if not blogs.exists():
            return Response({'empty': 'No blogs found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        

        data = {
            'title': request.data.get('title'),
            'image': request.data.get('image'),
            'category': request.data.get('category'),  
            'summary': request.data.get('summary'),
            'content': request.data.get('content'),
            'status': request.data.get('status'),
            'user': request.user.id,

        }

        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blog created successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class Categories(APIView):
    def get(self, request):
        serialiser = {} 
        categories = Category.objects.all()
        if categories is None: 
            serializer.data = { 'empty': 'empty'}
        else: 
                    serializer = CategorySerializer(categories, many=True, include_id = True)  

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = CategorySerializer( data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
                      
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
@ensure_csrf_cookie
def csrf_token_view(request):
    print(request.META.get('CSRF_COOKIE'))
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE')})

class UserView(APIView):
    def get(self, request, user_id):
            try:
                user = CustomerUserProfile.objects.get(id=user_id)
                serializer = CustomRegisterSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomerUserProfile.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CategoryForBlogView(APIView):
    def get(self, request, category_id):
            try:
                category = Category.objects.get(id=category_id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
class BlogsByCategory(APIView):
    def get(self, request, category_id):
            try:
                category_blog = BlogModel.objects.filter(id=category_id)
                serializer = BlogSerializer(category_blog, many =True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class AvailableTimesView(APIView):
    permission_classes = [IsAuthenticated]
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    
    def get(self, request, doctor_id):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        try:
            calendar_instance = CalendarModel.objects.get(doctor__id=doctor_id)
            calendar_id = calendar_instance.calendar_id
            calendar_timezone = calendar_instance.timezone

            now = datetime.datetime.now()
            start_of_month = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(seconds=1)

            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=now.isoformat() + 'Z',
                timeMax=end_of_month.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            busy_times = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                start_time = dateutil.parser.isoparse(start)
                end_time = dateutil.parser.isoparse(end)

                if start_time.tzinfo is None:
                    start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
                if end_time.tzinfo is None:
                    end_time = timezone.make_aware(end_time, timezone.get_current_timezone())

                is_busy = any(start_time < busy_end and end_time > busy_start for busy_start, busy_end in busy_times)

                if not is_busy:
                    busy_times.append((start_time, end_time))

            available_dates = {}
            current_date = start_of_month
            while current_date <= end_of_month:
                current_time = current_date.replace(hour=9, minute=0)
                end_time = current_date.replace(hour=17, minute=0)

                if current_time.tzinfo is None:
                    current_time = timezone.make_aware(current_time, timezone.get_current_timezone())
                if end_time.tzinfo is None:
                    end_time = timezone.make_aware(end_time, timezone.get_current_timezone())

                daily_available_times = []
                while current_time < end_time:
                    slot_end_time = current_time + datetime.timedelta(minutes=45)

                    if slot_end_time.tzinfo is None:
                        slot_end_time = timezone.make_aware(slot_end_time, timezone.get_current_timezone())

                    is_available = not any(current_time < busy_end and slot_end_time > busy_start for busy_start, busy_end in busy_times)

                    if is_available:
                        daily_available_times.append({
                            'start_time': current_time.strftime('%H:%M'),
                            'end_time': slot_end_time.strftime('%H:%M'),
                        })
                    current_time = slot_end_time

                if daily_available_times:
                    available_dates[current_date.strftime('%Y-%m-%d')] = daily_available_times

                current_date += datetime.timedelta(days=1)

            return Response({'available_dates': available_dates})

        except CalendarModel.DoesNotExist:
            return Response({'error': 'Calendar not found for this doctor.'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def post(self, request, doctor_id):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        try:
            calendar_instance = CalendarModel.objects.get(doctor__id=doctor_id)
            calendar_id = calendar_instance.calendar_id

            data = request.data
            summary = data.get('summary', 'Appointment')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time')
            

            start_time = datetime.datetime.fromisoformat(start_time_str)
            end_time = start_time + datetime.timedelta(minutes=45)

            print(data)
            start_time_model = dateutil.parser.isoparse(data.get('start_time'))
            end_time_model = start_time_model + datetime.timedelta(minutes=45)

            Appointment.objects.create(
            doctor= CustomerUserProfile.objects.get(id=doctor_id),  
            speciality=data.get('summary'),
            date=start_time.date(),
            start_time=start_time,
            end_time=end_time, 
            patient = request.user, 
        )

            


            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': calendar_instance.timezone,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': calendar_instance.timezone,
                },
            }

            event_result = service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            

            return Response({'message': 'Appointment created successfully', 'event': event_result})

        except CalendarModel.DoesNotExist:
            return Response({'error': 'Calendar not found for this doctor.'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GetUserObjView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = CustomerUserProfile.objects.get(pk=request.user.id)
        return JsonResponse({'user_type': user_profile.user_type})


class ConfirmedAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        appointments = Appointment.objects.filter(patient=user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

@staticmethod
def get_all_available_dates(doctor_id):
    available_dates = {}
    
    start_date = timezone.now().date()
    end_date = start_date + datetime.timedelta(days=30)  

    current_date = start_date
    while current_date <= end_date:
        available_dates[current_date.isoformat()] = [
            {'start_time': f'{current_date.isoformat()}T09:00:00', 'end_time': f'{current_date.isoformat()}T10:00:00'},
            {'start_time': f'{current_date.isoformat()}T10:00:00', 'end_time': f'{current_date.isoformat()}T11:00:00'},
        ]
        current_date += datetime.timedelta(days=1)
    
    return available_dates

# class AvailableSlotsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user

#         try:
#             user_profile = CustomerUserProfile.objects.get(username=user.username)
#         except CustomerUserProfile.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

#         if user_profile.user_type != 'doctor':
#             return Response({"error": "Only doctors have available slots."}, status=status.HTTP_403_FORBIDDEN)
        
#         calendar_id = user_profile.calendar_id
        
#         try:
#             credentials = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
#             service = build('calendar', 'v3', credentials=credentials)

#             events_result = service.events().list(
#                 calendarId=calendar_id,
#                 timeMin='2024-01-01T00:00:00Z',  
#                 timeMax='2024-12-31T23:59:59Z',
#                 singleEvents=True,
#                 orderBy='startTime'
#             ).execute()

#             events = events_result.get('items', [])
            
#             available_dates = []
#             for event in events:
#                 start_time = event['start'].get('dateTime', event['start'].get('date'))
#                 if start_time:
#                     available_dates.append(start_time)

#             return Response({'available_dates': available_dates})

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id, patient=request.user)
            appointment.delete()
            return Response({'message': 'Appointment cancelled successfully'}, status=204)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=404)
        
        
class ReactAppView(View):

    def get(self, request):
        try:

            with open(os.path.join(settings.REACT_APP, 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except :
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )