from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    SubPlanView,
    SubPlanViewById,
    SubPlanPurchaseView,
    SubscriptionPurchaseView,
    TrainerSubscriptionView,
    PaymentViewSet,
)

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('subplans/', SubPlanView.as_view(), name='subplans-list'),
    path('subplans/<int:pk>/', SubPlanViewById.as_view(), name='subplan-detail'),
    path('subplans/purchase/', SubPlanPurchaseView.as_view(), name='subplan-subscription-purchase'),
    path('subplans/<int:pk>/purchase/', SubPlanPurchaseView.as_view(), name='subplan-purchase'),
    path('subscriptions/purchase/', SubscriptionPurchaseView.as_view(), name='subscription-purchase'),
    path('trainer-subscription/purchase/', TrainerSubscriptionView.as_view(), name='trainer-subscription-purchase'),
]

urlpatterns += router.urls
