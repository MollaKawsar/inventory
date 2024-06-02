from django.urls import path
from crm import views

urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_out,name='logout'),
    path('product_upload/',views.product_add,name='product_uplaod'),
    path('deshborad/',views.deshborad,name='deshborad'),
    
    #path('order/<int:pk>/', views.Make_order, name='order'),
    path('search/',views.search,name='search'),
    #path('cart_view/',views.cart_view,name='cart_view'),
    path('recept/',views.recept,name='recept'),
    path('marketing/',views.marketing,name='marketing'),
    path('campaign/',views.campagin,name='campaign'),
    path('cart/add/<int:product_id>/', views.Make_order, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('place_order/', views.place_order, name='place_order'),
    path('crm/',views.crm,name='crm'),
]

