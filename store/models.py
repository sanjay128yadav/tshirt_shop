from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TshirtProperty(models.Model):
    title = models.CharField(max_length=30, null=False)
    slug  = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.title

    class Meta :
        abstract: True

class Occasion(TshirtProperty):
    pass
class IdealFor(TshirtProperty):
    pass
class NeckType(TshirtProperty):
    pass
class Sleeve(TshirtProperty):
    pass
class Brand(TshirtProperty):
   pass
class Color(TshirtProperty):
   pass
    
class Tshirt(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=200, null=True, unique=True, default="")
    description = models.CharField(max_length=500, null=True)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='upload/images/', null=False)
    Occasion = models.ForeignKey(Occasion, on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    Sleeve = models.ForeignKey(Sleeve, on_delete = models.CASCADE)
    neck_type = models.ForeignKey(NeckType, on_delete = models.CASCADE)
    ideal_for = models.ForeignKey(IdealFor, on_delete = models.CASCADE)
    color = models.ForeignKey(Color, on_delete = models.CASCADE)

    def __str__(self):
        return self.ideal_for.__str__() + "--" + self.name
    

    class Meta:
        db_table= 'table_tshirt' 


class SizeVariant(models.Model):
    SIZE = (
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Extra Extra Large"),
    )   

    price = models.IntegerField(null=False)    
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZE, max_length=5)

class Cart(models.Model):  
    sizeVariant = models.ForeignKey(SizeVariant , on_delete= models.CASCADE)  
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User , on_delete = models.CASCADE)

class Order(models.Model): 
    orderStatus = (
        ('PENDING', "Pending"),
        ('Placed', "Placed"),
        ('CANCLED', "Cancled"),
        ('COMPLETED', "Completed"),
    ) 
    method = (
        ('COD', "COD"),
        ('ONLINE', "Online"),
    )  
    order_status = models.CharField(max_length=15 , choices=orderStatus)  
    payment_method = models.CharField(max_length=15 , choices=method)
    shipping_address = models.CharField(max_length=100 , default=False)
    phone = models.CharField(max_length=10 , default=False)
    user = models.ForeignKey(User , on_delete = models.CASCADE) 
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)   

class OrderItem(models.Model):        
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    tshirt = models.ForeignKey(Tshirt , on_delete = models.CASCADE)
    size = models.ForeignKey(SizeVariant , on_delete = models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

class Payment(models.Model): 
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    date = models.DateTimeField(null=False, auto_now_add=True)  
    payment_status = models.CharField(max_length=15, default='FAILED')   
    payment_id = models.CharField(max_length=60)   
    payment_request_id = models.CharField(max_length=60, default='FAILED', unique=True, null=False)   

