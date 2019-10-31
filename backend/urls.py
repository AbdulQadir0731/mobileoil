from django.urls import path

from . import views
from django.urls import include
from django.conf.urls import url
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

router = routers.DefaultRouter()
router.register(r'cars', views.UserCarsView, basename='Car')
router.register(r'user/appointment', views.UserAppointmentView, basename='Appointment')
router.register(r'user/notifications', views.UserNotificationsView, basename='Notifications')
router.register(r'mechanic/codes', views.MechanicZipsView, basename='Codes')
router.register(r'devices', FCMDeviceAuthorizedViewSet)
# router.register(r'user/cars', views.getUserCars, basename='Car')

urlpatterns = [
    path('', views.index, name='index'),
    path('user/token/', views.createUserToken.as_view()),
    path('user/', views.HelloView.as_view()),
    path('user/cars/', views.getUserCars.as_view()),
    path('mechanic/appointment/', views.getMechanicAppointments.as_view()),
    url(r'^', include(router.urls)),
    # path('user/cars/', views.UserCarsView),
    path('mechanic/', views.getMechanicProfile.as_view()),
    url(r'^user/', include('rest_auth.urls')),
    url(r'^user/registration/', include('rest_auth.registration.urls')),
]