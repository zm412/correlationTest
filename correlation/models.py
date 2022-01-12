from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

import datetime
from django.urls import reverse


class User(AbstractUser):
    pass

class Data_type(models.Model):
    type_name = models.CharField(max_length=10)

    def __str__(self):
        return "id:{}, type_name: {}".format(
            self.id,
            self.type_name,
        )

class Correlation_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    x_data = models.ForeignKey(Data_type, on_delete=models.CASCADE, related_name='x_data_type')
    y_data = models.ForeignKey(Data_type, on_delete=models.CASCADE, related_name='y_data_type')
    correlation = models.FloatField()
    correlation_p = models.FloatField()
    day_name = models.CharField(max_length=10)

    def __str__(self):
        return "user: {}, x_data: {}, y_data:{}, corr:{}, corrP: {},  day: {}".format(
            self.user.username,
            self.x_data.type_name,
            self.y_data.type_name,
            self.correlation,
            self.correlation_p,
            self.day_name,
        )

    def serialize(self):
        return {
            "user_id": self.user.id,
            "x_data_type": self.x_data.type_name,
            "y_data_type": self.y_data.type_name,
            "correlation": {
                "value": self.correlation,
                "p_value": self.correlation_p,
                    }
        }


