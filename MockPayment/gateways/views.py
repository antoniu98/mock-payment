from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse

from .forms import PaymentForm
from .decider import Decider
from .payment_gateways import GeneralPaymentGateway, CheapPaymentGateway, ExpensivePaymentGateway, PremiumPaymentGateway


# Create your views here.
class PaymentView(View):
    """
    Class for proccessing payments
    """
    def post(self, request):
        fields = {
            'credit_card_number': request.POST.get('credit_card_number'),
            'card_holder'       : request.POST.get('card_holder'),
            'expiration_date'   : request.POST.get('expiration_date')[:-6] + '.0',
            'security_code'     : request.POST.get('security_code'),
            'amount'            : request.POST.get('amount'),
            'form'              : request.POST.get('form'),
        }
        form = PaymentForm(fields)

        if form.is_valid():
            decider = Decider()
            response = decider.selectGateway(form.data['amount'])
            return response
        else:
            data = {
                "message" : "Wrong credentials :" + str(form.errors)
            }
            return JsonResponse(data, status=400)


    def get(self, request):
        return HttpResponse("Use post...")


class ApiView(View):
    """
    Class for services state changes
    """
    def post(self, request):
        self.setState(request, CheapPaymentGateway()      , "cheap")
        self.setState(request, ExpensivePaymentGateway()  , "expensive")
        self.setState(request, PremiumPaymentGateway()    , "premium")
        return HttpResponse("Services updated.")

    def get(self, request):
        context = {
            'cheap_state'       : self.getState(CheapPaymentGateway()),
            'expensive_state'   : self.getState(ExpensivePaymentGateway()),
            'premium_state'     : self.getState(PremiumPaymentGateway())
        }
        return render(request, "gateways/api.html", context)


    def getState(self, gateway):
        if gateway.getAvailability() is True:
            return "ON"
        return "OFF"

    def setState(self, request, gateway, value):
        try:
            if request.POST.get(value) == "ON":
                gateway.setAvailability(True)
            else:
                gateway.setAvailability(False)
        except Exception as e:
            # no button checked
            print("error: " + str(e))
            pass