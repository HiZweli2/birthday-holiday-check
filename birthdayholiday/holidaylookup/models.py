from django.db import models

# Create your models here.

class SAIDRecord(models.Model):
    id_number= models.CharField(max_length=13, unique=True)
    date_of_birth= models.DateField()
    gender= models.CharField(max_length=6)
    is_sa_citizen = models.BooleanField()
    search_count=  models.PositiveBigIntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SA ID {self.id_number} - Searched {self.search_count} times"

class PublicHoliday(models.Model):
    said_record= models.ForeignKey("SAIDRecord", on_delete=models.CASCADE, related_name="public_holidays")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True , null=True)
    date = models.DateField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.date})"
