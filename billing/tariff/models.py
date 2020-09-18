from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class InternetTariff(models.Model):
    title = models.CharField(
        max_length=255, unique=True, default="Internet tariff")
    download_speed_kbps = models.PositiveIntegerField(
        "Download speed (kbps)", default=0)
    upload_speed_kbps = models.PositiveIntegerField("Upload speed (kbps)", default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title
