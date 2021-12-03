from django.db import models

# Create your models here.


class Warehouse(models.Model):
    model = models.IntegerField()
    specification = models.IntegerField()
    quantity = models.IntegerField()
    name = models.TextField()
    distributor = models.TextField()
    info = models.TextField()
    price = models.IntegerField()
    selector = models.TextField()
    src = models.TextField()

    def get_obj(self):
        return {
            'model': self.model,
            'specification': self.specification,
            'title': self.name,
            'distributor': self.distributor,
            'info': self.info,
            'price': self.price,
            'selector': self.selector,
            'src': 'static/img/' + self.src,
            'quantity': self.quantity
        }


class Order(models.Model):
    name = models.TextField()
    phone = models.TextField()
    email = models.TextField()
    address = models.TextField()
    delivery_type = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def get_obj(self):
        return{
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'delivery_type': self.delivery_type
        }


class CartItem(models.Model):
    model = models.IntegerField()
    quantity = models.IntegerField()
    specification = models.IntegerField()
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)

    def get_obj(self):
        return {
            'model': self.model,
            'quantity': self.quantity,
            'specification': self.specification
        }
