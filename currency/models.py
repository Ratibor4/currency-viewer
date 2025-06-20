from django.db import models

class ExchangeRate(models.Model):
    base = models.CharField(max_length=3)
    target = models.CharField(max_length=3)
    rate = models.FloatField()
    date = models.DateField()

    class Meta:
        unique_together = ('base', 'target', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.base} → {self.target} @ {self.date}: {self.rate}"
