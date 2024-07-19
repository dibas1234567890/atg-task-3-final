from django.urls import path, re_path
from login_system.views import  AvailableTimesView, ConfirmedAppointmentsView,  GetUserObjView, ReactAppView
from login_system.views import (
    BlogView,
    BlogsByCategory,
    Categories,
    CategoryForBlogView,
    CustomRegisterView, 
    CustomLoginView, 
    DoctorDashboardView, 
    PatientDashboardView, 
    IndexView,
    UserView,
    csrf_token_view,
)
from rest_framework_simplejwt import views as jwt_views

from django.conf import settings
from django.conf.urls.static import static
app_name = 'home'

urlpatterns = [
    path('register', CustomRegisterView.as_view(), name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('patient_dashboard', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctor_dashboard', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('categories', Categories.as_view(), name='categories'),
    path('blogs', BlogView.as_view(), name='blogs'),
    path('blogs_by_category/<int:category_id>', BlogsByCategory.as_view(), name='blogs'),
    path('user/<int:user_id>', UserView.as_view(), name='user'),
    path('categories/<int:category_id>', CategoryForBlogView.as_view(), name='category'),

    path('token', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('token/refresh', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
              path('csrf_token', csrf_token_view, name=''),

    # path('fetch-events/', CalendarView.fetch_events, name='fetch_events'), 
    path('user-obj', GetUserObjView.as_view(), name='get_user_obj'),

    path('fetch-available-slots/<int:doctor_id>', AvailableTimesView.as_view(), 
         name='get_available_times'), 
    path('save-event', AvailableTimesView.as_view(), 
         name='save_event'),
     path('myappointments', ConfirmedAppointmentsView.as_view(), name='myappointments'),
     # path('available-dates', AvailableSlotsView.as_view(), name='available-dates'),

    


] 
