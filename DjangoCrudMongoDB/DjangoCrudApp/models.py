from djongo import models
# Create your models here.

class Posts(models.Model):
    _id=models.ObjectIdField()
    product_name=models.CharField(max_length=255)
    product_img = models.TextField(null=False)
    product_link = models.TextField(null=False)
    product_price = models.CharField(max_length=255)
    domain_name = models.CharField(max_length=255)
    objects=models.DjongoManager()

