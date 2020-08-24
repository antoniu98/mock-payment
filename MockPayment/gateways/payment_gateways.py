class GeneralPaymentGateway():
    gatewayName = "GENERAL"
    availability = True
    
    def processPayment(self, amount):
        return 'Processing the amount of : {1}, using {0} gateway...'.format(self.gatewayName, amount)

    @classmethod
    def getAvailability(cls):
        return cls.availability

    @classmethod
    def setAvailability(cls, state):
        cls.availability = state

    def __str__(self):
        return self.gatewayName + " gateway"

class CheapPaymentGateway(GeneralPaymentGateway):
    gatewayName = "CHEAP"


class ExpensivePaymentGateway(GeneralPaymentGateway):
    gatewayName = "EXPENSIVE"

class PremiumPaymentGateway(GeneralPaymentGateway):
    gatewayName = "PREMIUM"
    availability = False
