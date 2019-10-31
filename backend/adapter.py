from allauth.account.adapter import DefaultAccountAdapter
from .models import Mechanic, Codes
from django.conf import settings
import braintree

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )
        result = gateway.customer.create({
          "first_name": user.first_name,
          "email": user.email
          }
        )
        if result.is_success:
          user.customer_id = result.customer.id
        data = form.cleaned_data
        user.is_mechanic = data.get('is_mechanic')
        user.save()
        if user.is_mechanic:
            m = Mechanic.objects.create(
            		user=user,
            		address=data.get('address'),
            		lat=data.get('lat'),
            		lon=data.get('lon')
            	)
            m.save()
        return user