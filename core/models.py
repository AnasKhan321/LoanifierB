from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Creating Models for Loan

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField(null=True)
    term = models.IntegerField(null=True)
    installment = models.IntegerField(null=True)
    date = models.DateField(blank=True)
    status = models.CharField(default="", max_length=300)

    def __str__(self):
        return self.user.username
