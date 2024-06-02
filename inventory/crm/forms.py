from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from crm.models import*
from django.contrib.auth.models import User




class Upload_product_form(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','category','Sub_category','Style',
                'color','Qunatity','cost','MRP','description','product_pic',
                
                ]
        
        
class profile_user(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email','password1', 'password2',]



class CartItemForm(forms.ModelForm):
    class Meta:
        model=Order
        fields= ['cus_name', 'product_size', 'campaign', 'total_price', 'is_ordered']



class CustomerForm(forms.Form):
    class Meta :
        model=customer
        fields='__all__'
        
class product_search(forms.Form):
    q=forms.CharField(max_length=100,label='Search')
    
    
    


class marketingForm(forms.ModelForm):
    class Meta:
        model=Markting_campaign
        fields='__all__'
        widgets = {
           'start_date': forms.DateInput(attrs={'type': 'date'}),
            'End_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = order_item
        fields = [ 'quantity', 'discount']


class MarketingForm(forms.ModelForm):
    
    
    
    class Meta:
        model=Marketing
        fields=['campaign_name','Engaged','Reach','Budget','channel_name']
