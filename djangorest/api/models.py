from django.db import models


# Create your models here.

class Bucketlist(models.Model):
    """ buckectlist model """
    title = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def ___str__(self):
        return "{}".format(self.title)
