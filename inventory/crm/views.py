from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import HttpResponseRedirect,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from crm.forms import*
from crm.models import*
from django.db.models import Sum
from django.contrib import messages




def SignUp(req):
    form=profile_user()
    if req.method=="POST":
        form=profile_user(data=req.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('login'))
    diction={'form':form}

    return render(req,'register.html',context=diction)




def user_login(req):
    form=AuthenticationForm()
    if req.method=='POST':
        form=AuthenticationForm(data=req.POST)
        if form.is_valid():
            username =form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user != None:
                login(req,user)
            #return HttpResponseRedirect(reverse(''))
    return render(req,'login.html',context={'form':form})



@login_required
def user_out(req):
    logout(req)
    
    return HttpResponseRedirect(reverse('login'))
    
    
    
    
@login_required
def product_add(req):
    add_product=Upload_product_form( )
    if req.method=='POST':
        add_product=Upload_product_form(req.POST,req.FILES)
        if add_product.is_valid():
            product=add_product.save(commit=False)
            crm_user_instance, created = Crm_user.objects.get_or_create(user= req.user)
            product.staff = crm_user_instance
            product.save()     
            
            return HttpResponseRedirect(reverse('product_uplaod'))
    return render(req,'product_upload.html',context={'product':add_product})       



@login_required
def deshborad(req):
    total_products=Product.objects.count()
    total_order=Order.objects.count()
    total_cost = Product.objects.aggregate(Sum('cost'))['cost__sum'] or 0
    total_store_in = Product.objects.aggregate(Sum('Qunatity'))['Qunatity__sum'] or 0
    
    return render(req,'deshborad.html',context={'total_products':total_products,'total_order':total_order,'total_cost':total_cost,'total_store':total_store_in})



@login_required
def search(req):
    query =req.GET.get('q')
    products=[]
    if query:
        
        products = Product.objects.filter(product_name__icontains=query)
    
    return render(req, 'order.html', {'products': products, 'query': query})




@login_required

def marketing (req):
    
    marketing_form=marketingForm()
    if req.method=='POST':
        marketing_form=marketingForm(req.POST)
        if marketing_form.is_valid():
        
            marketing_form.save()
            return HttpResponseRedirect(reverse('campaign'))
    return render(req, 'Marketing.html', {'form': marketing_form})

@login_required
def campagin (req):
    campagin=MarketingForm()
    if req.method=="POST":
        campagin=MarketingForm(req.POST)
        if campagin.is_valid():
            campaign_name = campagin.cleaned_data['campaign_name']
            engaged = campagin.cleaned_data['Engaged']
            reach = campagin.cleaned_data['Reach']
            budget = campagin.cleaned_data['Budget']
            if budget <= 0:
                raise forms.ValidationError("Budget must be a positive value. ")
            campagin.save()
            
            return HttpResponseRedirect(reverse('marketing'))
    return render(req,'campaign.html',context={'form':campagin})       

@login_required
def Make_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer_name = customer.objects.first()
    Customer = get_object_or_404(customer, cus_name=customer_name)
    crm_user = get_object_or_404(Crm_user, user=request.user)

    # Set a default campaign or handle campaign assignment logic
    default_campaign = Marketing.objects.first()  # Assuming at least one campaign exists

    if not default_campaign:
        messages.error(request, "No marketing campaigns available.")
        return redirect('product_list')  # Redirect to a page listing products or an appropriate page

    # Check if there is an existing open order for the customer
    try:
        order = Order.objects.filter(cus_name=Customer, is_ordered=False).first()
        if not order:
            order = Order.objects.create(
                cus_name=Customer,
                is_ordered=False,
                total_price=0,
                ordered_created_by=crm_user,
                campaign=default_campaign
            )
    except Order.MultipleObjectsReturned:
        messages.error(request, "Multiple open orders found. Please contact support.")
        return redirect('cart_detail')

    # Check if the order item already exists
    Order_item, created = order_item.objects.get_or_create(
        product=product,
        order=order,
        defaults={'quantity':1, 'price': product.cost, 'discount': 0}
    )

    if not created:
        Order_item.quantity += 1
        Order_item.save()

    # Update the total price of the order
    order.total_price += product.cost
    order.save()

    messages.success(request, f"Added {product.product_name} to cart.")
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    Order_items = order_item.objects.all()
    return render(request, 'cart.html', context={'Order_items': Order_items})


@login_required
def place_order(request):
    Order_items = order_item.objects.all()
    if not Order_items:
        messages.error(request, "Your cart is empty.")
        return redirect('search')

    crm_user = get_object_or_404(Crm_user, user=request.user)
    total_price = sum(item.product.MRP * item.quantity for item in Order_items)

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.ordered_created_by = crm_user
            order.total_price = total_price
            order.save()
            for item in Order_items:
                item.order = order
                item.save()
            messages.success(request, "Order placed successfully.")
            return redirect('recept')
    else:
        form = CartItemForm(initial={'total_price': total_price})

    return render(request, 'placeorder.html', {'order_items': Order_items, 'form': form})



@login_required
def recept(req):
    # Fetch all orders for the logged-in user that have been placed (is_ordered=True)
    user = req.user
    orders = Order.objects.filter(ordered_created_by__user=user, is_ordered=True)
    
    # Create a dictionary to hold order items for each order
    orders_with_items = {}
    for order in orders:
        order_items = order_item.objects.filter(order=order)
        orders_with_items[order] = order_items
    
    return render(req, 'recept.html', context={'orders_with_items': orders_with_items})



@login_required
def crm(request):
    orders =order_item.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'crm.html', context)