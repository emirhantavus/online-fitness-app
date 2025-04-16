from django.db import models
from users.models import User
from datetime import timedelta
from django.conf import settings


class SubPlan(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    
    def __str__(self) -> str:
         return self.title
     
class SubPlanFeature(models.Model):
    subplan = models.ForeignKey(SubPlan, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
         return self.title


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subplan = models.ForeignKey(SubPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super(UserSubscription, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.subplan.title}"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed')])

    
    def __str__(self) -> str:
        return f"{self.user.email} - {self.amount} - {self.status} - {self.timestamp}"