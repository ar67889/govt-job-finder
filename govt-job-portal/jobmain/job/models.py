from django.db import models

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    last_date = models.DateField()
    apply_link = models.URLField()

    def __str__(self):
        return self.title
