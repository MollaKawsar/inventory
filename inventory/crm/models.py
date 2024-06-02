from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Crm_user(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='author')
    
    
    
class Product(models.Model):
    CATEGORY_TYPE_CHOICES = (
            ('women', 'Women'),
            ('mens', 'Mens'),
            ('girls', 'Girls'),
            ('boys','Boys'),
            ('children','Children'),
    )
    
    
   
    staff=models.ForeignKey(Crm_user,on_delete=models.CASCADE,related_name='profile')
    product_name=models.CharField(max_length=260,blank=True)
    category=models.CharField(max_length=20,choices=CATEGORY_TYPE_CHOICES)
    Sub_category=models.CharField(max_length=20,blank=True)
    Style=models.CharField(max_length=20,blank=True)
    color=models.CharField(max_length=60,blank=True)
    Qunatity=models.IntegerField()
    cost=models.DecimalField(max_digits=50,decimal_places=2)
    MRP=models.DecimalField(max_digits=50,decimal_places=2)
    description=models.TextField(max_length=500,blank=True)
    product_pic=models.ImageField(upload_to='product_pic')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name
    

class customer (models.Model):
    cus_name=models.CharField(max_length=200)
    contact_number =models.CharField(max_length=200)
    address=models.CharField(max_length=200) 
    
    
    
    def __str__(self):
        return self.cus_name 
    
    
class Markting_campaign(models.Model):
    campaign_name=models.CharField(max_length=200)
    start_date=models.DateField()
    End_date=models.DateField()
    

    def __str__(self):
        return self.campaign_name


class Marketing (models.Model):
    channel=(
            ('none','None'),
            ('youtube', 'Youtube'),
            ('facebook', 'Facebook'),
            ('tiktok', 'Tiktok'),
            ('web','Web'),
    )
    campaign_name =models.ForeignKey(Markting_campaign,on_delete=models.CASCADE)
    channel_name =models.CharField(max_length=200,choices=channel)
    Engaged=models.CharField(max_length=200)
    Reach=models.CharField(max_length=200)
    Budget=models.DecimalField(max_digits=50,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.channel_name

class Order(models.Model):
    
    SIZE=(
        ('xl','XL'),
        ('m','M'),
        ('xxl','XXL'),
        ('xs','XS'),
        ('s','S'),
        ('l','L'),
    )
    
    cus_name = models.ForeignKey(customer,on_delete=models.CASCADE)
    product=models.ManyToManyField(Product,through='order_item')
    total_price=models.DecimalField(max_digits=40,decimal_places=2)
    ordered_created_by=models.ForeignKey(Crm_user,on_delete=models.CASCADE)
    product_size=models.CharField(max_length=250,choices=SIZE)
    campaign=models.ForeignKey(Marketing,on_delete=models.CASCADE,null=True,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return  f"{self.cus_name}"
    

class order_item(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=20,decimal_places=2)
    discount=models.DecimalField(max_digits=20,decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

