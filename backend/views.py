from django.shortcuts import render
from backend import models
from rest_auth.registration.views import RegisterView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from fcm_django.models import FCMDevice
from django.core import serializers
from backend.serializers import CustomUserDetailsSerializer, MechanicDetailsSerializer, CarSerializer, ZipCodesSerializer, AppointmentSerializer, UserCarSerializer, UserNotificationsSerializer

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
import json
import braintree


def index(request):
	device = FCMDevice.objects.all().get(user=models.User.objects.get(id=2))
	device.send_message("Mech Oil Test", "A test from the server.")
	return device
	# device.send_message(data={"test": "test"})
	# device.send_message(title="Title", body="Message", icon=..., data={"test": "test"})
	return 
	# return render(request, 'test.html', context={'user': models.User.objects.get(id=2)})

class createUserToken(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		user = request.user
		gateway = braintree.BraintreeGateway(
	    braintree.Configuration(
	        braintree.Environment.Sandbox,
	        merchant_id=settings.BRAINTREE_MERCHANT_ID,
	        public_key=settings.BRAINTREE_PUBLIC_KEY,
	        private_key=settings.BRAINTREE_PRIVATE_KEY
	    	)
		)
		# result = gateway.customer.create({
		# 	"first_name": user.first_name,
		# 	"email": user.email
		# 	}
		# )
		# if result.is_success:
		# 	user.customer_id = result.customer.id
		# user.save()
		client_token = gateway.client_token.generate({
			"customer_id":user.customer_id
			})
		return Response({"client_token":client_token})
	def post(self, request):
		user = request.user
		gateway = braintree.BraintreeGateway(
	    braintree.Configuration(
	        braintree.Environment.Sandbox,
	        merchant_id=settings.BRAINTREE_MERCHANT_ID,
	        public_key=settings.BRAINTREE_PUBLIC_KEY,
	        private_key=settings.BRAINTREE_PRIVATE_KEY
	    	)
		)
		result = gateway.transaction.sale({
			"amount": request.data.get('amount'),
			"payment_method_nonce": request.data.get('payment_method_nonce'),
			"options": {
				"submit_for_settlement":True
			}
		})
		if result.is_success:
			return Response({"response": result.transaction.id})
		else:
			return Response({"response": result.message})

#getProfile
class HelloView(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		user = request.user
		serializer = CustomUserDetailsSerializer(user)
		return Response(serializer.data)
	def put(self, request):
		file = request.data.get('image', None)
		user = request.user
		if file is not None:
			user.image = file
		name = request.POST.get('name', None)
		if name:
			user.first_name = name
		phone = request.POST.get('phone', None)
		if phone:
			user.phone = phone
		user.save()
		serializer = CustomUserDetailsSerializer(user)
		return Response(serializer.data)

#getMechanicProfile
class getMechanicProfile(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		mechanic = request.user.mechanic
		serializer = MechanicDetailsSerializer(mechanic)
		return Response(serializer.data)
	def put(self, request):
		mechanic = request.user.mechanic
		file = request.data.get('image', None)
		if file is not None:
			mechanic.license_image = file
		garage = request.POST.get('garage', None)
		if garage is not None:
			mechanic.garage = garage
		is_searching = request.POST.get('is_searching', None)
		if is_searching:
			mechanic.is_searching = is_searching
		insurance = request.POST.get('insurance', None)
		if insurance:
			mechanic.insurance = insurance
		address = request.POST.get('address', None)
		if address:
			mechanic.address = address
		license = request.POST.get('license', None)
		if license:
			mechanic.license = license
		lat = request.POST.get('lat', None)
		if lat:
			mechanic.lat = lat
		lon = request.POST.get('lon', None)
		if lon:
			mechanic.lon = lon
		mechanic.save()
		serializer = MechanicDetailsSerializer(mechanic)
		return Response(serializer.data)

#registerUser
#loginUser
class getUserCars(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		user = request.user
		serializer = CarSerializer(user.car_set.all(), many=True)
		return Response(serializer.data)
	def post(self, request):
		user = request.user
		car_id = request.data.get('car')
		car = models.Car.objects.get(id=car_id)
		car.user.add(user)
		serializer = CarSerializer(user.car_set.all(), many=True)
		return Response(serializer.data)

class getMechanicAppointments(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		st = request.GET.get('status', 'pending')
		mechanic = request.user.mechanic
		cl = mechanic.codes_set.values_list('code', flat=True)
		appointments = models.Appointment.objects.filter(status=st).filter(zip_code__in=cl)
		serializer = AppointmentSerializer(appointments, many=True)
		return Response(serializer.data)
	def post(self, request):
		mechanic = request.user.mechanic
		appt_id = request.data.get('appointment')
		st = request.data.get('status', 'scheduled')
		appt = models.Appointment.objects.get(id=appt_id)
		appt.mechanic = mechanic
		appt.status = st
		appt.save()
		device = FCMDevice.objects.get(user=appt.user)
		if appt.status=="scheduled":
			title = "Appointment Scheduled"
			body=mechanic.user.first_name+" has accepted an appointment for a(n) "+appt.service+" service."
			body2 = "<br>"+mechanic.user.first_name+"</b> has accepted an appointment for a(n) <b>"+appt.service+"</b> service."
		else:
			title="Service Completed"
			body="An appointment for your "+appt.car.manufacturer+" has been completed."
			body2 = "An appointment for your <b>"+appt.car.manufacturer+"</b> has been completed."
		device.send_message(title, body)
		appt.user.notifications_set.create(title=title,body=body2,data=appt.id,image=appt.car.image)
		serializer = AppointmentSerializer(appt)
		return Response(serializer.data)

class PersonCarsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserCarSerializer
	def get_queryset(self):
		user = self.request.user
		serializer = UserCarSerializer(user)
		return serializer.data

class UserNotificationsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	serializer_class = UserNotificationsSerializer
	def get_queryset(self):
		user = self.request.user
		serializer = UserNotificationsSerializer(user.notifications_set.all(), many=True)
		return serializer.data

class UserCarsView(viewsets.ModelViewSet):
	serializer_class = CarSerializer
	permission_classes = (IsAuthenticated,)
	queryset= models.Car.objects.all()

class MechanicZipsView(viewsets.ModelViewSet):
	serializer_class = ZipCodesSerializer
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		user = self.request.user
		return user.mechanic.codes_set.all()

class UserAppointmentView(viewsets.ModelViewSet):
	serializer_class = AppointmentSerializer
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		user = self.request.user
		st = self.request.GET.get('status')
		return user.appointment_set.filter(status=st)
	def create(self, request, *args, **kwargs):
		response = super(UserAppointmentView, self).create(request, *args, **kwargs)
		codes = models.Codes.objects.filter(code=response.data["zip_code"])
		for cd in codes:
			if cd.mechanic.is_searching==True:
				user = cd.mechanic.user
				device = FCMDevice.objects.get(user=user)
				title="A Pending Appointment"
				body="A <b>"+response.data["service"]+"</b> service was requested in your area."
				device.send_message(title, "Your service was requested in your area.")
				user.notifications_set.create(title=title,body=body,data=response.data["id"],image=response.data["car"]["image"])
		return response
	def put(self, request):
		user = request.user
		appt_id = request.data.get('appointment')
		st = request.data.get('status', 'pending')
		appt = models.Appointment.objects.get(id=appt_id)
		appt.status = st
		appt.save()
		serializer = AppointmentSerializer(appt)
		return Response(serializer.data)

class CustomRegisterView(RegisterView):
	queryset = models.User.objects.all()
