from json import JSONDecoder

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Warehouse, Order, CartItem

from serv.settings import DEBUG

class Market(APIView):
    JD = JSONDecoder()

    def post(self, req):
        errors = []
        order_info = req.data.get('order')
        order = Order(
            name=order_info['name'],
            phone=order_info['phone'],
            email=order_info['email'],
            address=order_info['address'],
            delivery_type=order_info['delivery_type']
        )
        order.save()

        cart = self.JD.decode(order_info['cart'])
        for each in cart:
            current = Warehouse.objects.filter(
                model=each['model'], specification=each['selected'])[0]
            if each['quantity'] <= current.quantity:
                item = CartItem(
                    model=each['model'],
                    specification=each['selected'],
                    quantity=each['quantity'],
                    order=order
                )
                item.save()
                current.quantity -= each['quantity']
                current.save()
            else:
                errors.append({'obj': each, 'type': 'quantity'})
        if not errors:
            return Response(status=201)
        else:
            return Response(status=200, data=errors)


class MarketWarehouse(APIView):
    def get(self, req):
        if DEBUG:
            print(req)
        raw_warehouse = Warehouse.objects.all()
        output_warehouse = []
        for each in raw_warehouse:
            output_warehouse.append(each.get_obj())
        return Response(status=200, data=output_warehouse)
