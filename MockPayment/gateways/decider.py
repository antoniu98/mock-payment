from .payment_gateways import GeneralPaymentGateway, CheapPaymentGateway, ExpensivePaymentGateway, PremiumPaymentGateway
from time import sleep
from django.http import JsonResponse

class Decider():
    """
    This class can also implement validation, act as a load balancer or other stuff
    """
    gateway = GeneralPaymentGateway()

    def selectGateway(self, amount):
        amount = float(amount)

        # Cheap Gateway
        if amount < 21:
            self.gateway = CheapPaymentGateway()
            if self.gateway.getAvailability() is False:
                return self.InternalServerErrorResponse()
            return self.OkResponse(amount)

        # Expensive Gateway
        elif amount <= 500:
            self.gateway = ExpensivePaymentGateway()
            if self.gateway.getAvailability() is False:
                # try cheap
                self.gateway = CheapPaymentGateway()
                if self.retryGateway(1) is True:
                    return self.OkResponse(amount) 
                else:
                    self.gateway = ExpensivePaymentGateway()
                    return self.InternalServerErrorResponse()
            return self.OkResponse(amount)

        # Premium Gateway
        else:
            self.gateway = PremiumPaymentGateway()
            # retry 3 times or error
            if self.retryGateway(3) is True:
                return self.OkResponse(amount) 
            return self.InternalServerErrorResponse()


    def retryGateway(self, times):
        for i in range(times):
            # try
            if self.gateway.getAvailability() is True:
                return True
            # timeout before retrying
            sleep(1)
            print("Retrying {}...".format(i+1))
        return None


    """
    Responses
    """
    def InternalServerErrorResponse(self):
        return JsonResponse({'message':'Server error for ' + str(self.gateway)}, status=500)

    def OkResponse(self, amount):
        return JsonResponse({'message': self.gateway.processPayment(amount)}, status=200)
