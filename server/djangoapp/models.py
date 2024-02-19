from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model 
class CarMake(models.Model):
    name = models.CharField(null = False, max_length = 30)
    description = models.CharField(max_length = 200) # Description
    
    def __str__(self):
        return self.name # - method to print a car make object


# <HINT> Create a Car Model model 
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    
    CAR_MODEL_CHOICES = [
    (SEDAN, 'Sedan'),
    (SUV, 'SUV'),
    (WAGON, 'Wagon')
    ]
    make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=True)
    name = models.CharField(null=False, max_length=30, default="")
    model_type = models.CharField(null=True, max_length=30, choices=CAR_MODEL_CHOICES)
    year = models.DateField(null=True)

    def __str__(self):
            return self.name + " " + self.model_type



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name



# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership 
        self.dealership = dealership
        # name
        self.name = name
        # Purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Sentiment of review
        self.sentiment = sentiment
        # Dealer id
        self.id = id
