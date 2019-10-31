from rest_framework import serializers
from backend import models
from .models import User, Mechanic, Car

from rest_auth.registration.serializers import RegisterSerializer
class CustomRegisterSerializer(RegisterSerializer):

	email = serializers.EmailField(required=True)
	password1 = serializers.CharField(write_only=True)
	first_name = serializers.CharField(required=True)
	is_mechanic = serializers.BooleanField(required=True)
	lat = serializers.DecimalField(required=False,max_digits=10,decimal_places=4)
	lon = serializers.DecimalField(required=False,max_digits=10,decimal_places=4)
	address = serializers.CharField(required=False)

	def get_cleaned_data(self):
		super(CustomRegisterSerializer, self).get_cleaned_data()
		return {
			'password1': self.validated_data.get('password1', ''),
			'first_name': self.validated_data.get('first_name', ''),
			'email': self.validated_data.get('email', ''),
			'is_mechanic': self.validated_data.get('is_mechanic', False),
			'address': self.validated_data.get('address', ''),
			'lat': self.validated_data.get('lat', 0),
			'lon': self.validated_data.get('lon', 0),
		}

class ZipCodesSerializer(serializers.HyperlinkedModelSerializer):
	code = serializers.CharField(required=True)
	class Meta:
		model = models.Codes
		fields = ('id','code')
		read_only_fields = ('code',)

	def create(self, validated_data):
		user = self.context.get("request")
		code = validated_data.get('code')
		return user.user.mechanic.codes_set.create(code=code)

class CustomUserDetailsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.User
		fields = ('id','email','first_name', 'is_mechanic', 'phone', 'image', 'customer_id')
		read_only_fields = ('email',)

class MechanicDetailsSerializer(serializers.ModelSerializer):
	user = CustomUserDetailsSerializer(required=False)
	class Meta:
		model = models.Mechanic
		fields = ('lon','lat','address', 'user', 'garage', 'is_searching', 'license_image', 'is_verified')
		read_only_fields = ('address',)

class CarSerializer(serializers.HyperlinkedModelSerializer):
	manufacturer = serializers.CharField(required=True)
	year = serializers.CharField(required=True)
	trim = serializers.CharField(required=False)
	medium_fee = serializers.DecimalField(required=True,max_digits=10,decimal_places=2)
	grade_fee = serializers.DecimalField(required=True,max_digits=10,decimal_places=2)
	conventional_fee = serializers.DecimalField(required=True,max_digits=10,decimal_places=2)
	premium_fee = serializers.DecimalField(required=True,max_digits=10,decimal_places=2)
	image = serializers.ImageField(required=True)
	class Meta:
		model = models.Car
		fields = ('id','manufacturer','year', 'trim', 'medium_fee', 'grade_fee','conventional_fee','premium_fee', 'image')
		read_only_fields = ('year',)

	def create(self, validated_data):
		man = validated_data.get('manufacturer')
		year = validated_data.get('year')
		trim = validated_data.get('trim', '')
		fee = validated_data.get('fee')
		image = validated_data.get('image')
		return Car.objects.create(manufacturer=man,year=year,trim=trim)

class UserCarSerializer(serializers.ModelSerializer):
	car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
	cars = CarSerializer(read_only=True, many=True)
	class Meta:
		model = User
		fields= ('cars', 'car')
	def create(self, validated_data):
		user = self.context['request'].user
		car = validated_data.get('car')
		car.user.add(user)
		return user

class UserNotificationsSerializer(serializers.HyperlinkedModelSerializer):
	title = serializers.CharField(required=True)
	body = serializers.CharField(required=True)
	data = serializers.CharField(required=True)
	image= serializers.CharField(required=False)
	created_at = serializers.DateTimeField(read_only=True,required=False)
	updated_at = serializers.DateTimeField(read_only=True,required=False)
	class Meta:
		model = models.Codes
		fields = ('id','title', 'body', 'data', 'created_at', 'updated_at', 'image')
		read_only_fields = ('title',)

	def create(self, validated_data):
		user = self.context.get("request")
		title = validated_data.get('title')
		data = validated_data.get('data')
		body = validated_data.get('body')
		return user.user.notifications_set.create(title=title,body=body,data=data)

class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
	user = CustomUserDetailsSerializer(required=False)
	mechanic = MechanicDetailsSerializer(required=False)
	car = CarSerializer(required=False)
	zip_code = serializers.CharField(required=True)
	service= serializers.CharField(required=True)
	car_id = serializers.IntegerField(required=True)
	date = serializers.DateTimeField(required=True)
	address = serializers.CharField(required=True)
	grade = serializers.CharField(required=False)
	status = serializers.CharField(required=False)
	instructions = serializers.CharField(required=False)
	lat = serializers.DecimalField(required=False,max_digits=10,decimal_places=6)
	lon = serializers.DecimalField(required=False,max_digits=10,decimal_places=6)
	fee = serializers.DecimalField(required=True,max_digits=10,decimal_places=4)
	class Meta:
		model = models.Car
		fields = ('id','car','address', 'mechanic', 'user', 'date', 'car_id', 'status', 'grade', 'zip_code', 'service', 'fee', 'instructions', 'lat', 'lon')
		read_only_fields = ('address',)

	def create(self, validated_data):
		req = self.context.get("request")
		address = validated_data.get('address')
		car_id = validated_data.get('car_id')
		fee = validated_data.get('fee')
		status = "pending"
		car = Car.objects.get(id=car_id)
		grade = validated_data.get('grade')
		instructions = validated_data.get('instructions')
		zip_code = validated_data.get('zip_code')
		service = validated_data.get('service')
		date = validated_data.get('date')
		lat = validated_data.get('lat', 0)
		lon = validated_data.get('lon', 0)
		return req.user.appointment_set.create(address=address,date=date,car=car,status=status, grade=grade, service=service, zip_code=zip_code, fee=fee, instructions=instructions, lat=lat, lon=lon)
