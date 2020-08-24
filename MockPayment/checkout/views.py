from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import django

from .forms import PaymentForm
import requests
import json

# Create your views here.
class CheckoutView(View):
    def get(self, request):
        context = {
            'form' : PaymentForm()
        }
        return render(request, 'checkout/index.html', context)

    def post(self, request):
        form = PaymentForm(request.POST or None)
        state = form
        if form.is_valid():
            url = "http://127.0.0.1:8000/gateway/pay"
            token = django.middleware.csrf.get_token(request)
            body = {
                'credit_card_number': form.cleaned_data['credit_card_number'],
                'card_holder'       : form.cleaned_data['card_holder'],
                'expiration_date'   : form.cleaned_data['expiration_date'],
                'security_code'     : form.cleaned_data['security_code'],
                'amount'            : form.cleaned_data['amount'],  
                'form'              : state,
                'csrfmiddlewaretoken' : token
            }

            # get csrf token
            response = requests.get(url)
            headers = {}
            headers['cookie'] = 'csrftoken=' + str(token)
            
            response = requests.post(url, data=body, headers = headers)
            status = response.status_code
            # decode and extract message
            data = json.loads(response.content.decode('utf-8'))['message']

            if status == 500:
                return HttpResponse('<h1>Internal server error...</h1><br><br> <h1>Message from gateway:</h1>' + str(data), status=500)
            return HttpResponse('<h1>Payment OK</h1><br><br> <h1>Message from gateway:</h1>' + str(data))
        else:
            context = {
                'errors' : form.errors
            }
            return render(request, 'checkout/wrong_credentials.html', context, status=400)