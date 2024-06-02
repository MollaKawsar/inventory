from django.contrib import admin
from crm.models import*


admin.site.register(Crm_user)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(order_item)
admin.site.register(customer)


@admin.register(Markting_campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'start_date', 'End_date',)

@admin.register(Marketing)
class marketingAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'channel_name', 'Engaged','Reach','Budget','created_at')


# Register your models here.
