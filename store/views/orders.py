from django.shortcuts import render
from django.views import View
from store.models.orders import Order


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        # total_customers = customer.count()
        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()

        print(orders)
        return render(request, 'orders.html',
                      {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending})
