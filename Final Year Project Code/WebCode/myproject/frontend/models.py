from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    phone = models.CharField(max_length=15)
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)   

    class Meta:
        db_table = 'Bookings'

    def __str__(self):
        return f"Booking by {self.name} on {self.date}"