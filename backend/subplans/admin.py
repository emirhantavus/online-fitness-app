from django.contrib import admin
from .models import SubPlan, SubPlanFeature, UserSubscription, Payment

@admin.register(SubPlan)
class SubPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

@admin.register(SubPlanFeature)
class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('subplan', 'title')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subplan', 'start_date', 'end_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'timestamp')
