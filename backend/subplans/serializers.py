from rest_framework import serializers
from .models import SubPlan, SubPlanFeature, UserSubscription , Payment

class SubPlanFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPlanFeature
        fields = ['id', 'title']

class SubPlanSerializer(serializers.ModelSerializer):
    features = SubPlanFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = SubPlan
        fields = ['id', 'title', 'price', 'features']
        

class UserSubscriptionSerializer(serializers.ModelSerializer):
    subplan = SubPlanSerializer()
    class Meta:
        model = UserSubscription
        fields = '__all__'
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'