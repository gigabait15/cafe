from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from Carts.models import Cart
from Orders.models import Order


class OrderListView(generic.ListView):
    """
    Представление для отображения списка заказов с поддержкой поиска.
    """

    model = Order
    template_name = 'Orders/order_list.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Добавляет в контекст данные о заказах, связанных корзинах и результатах поиска.
        :param kwargs: Дополнительные аргументы контекста.

        :return:dict: Расширенный контекст с деталями заказов.
        """
        context = super().get_context_data(**kwargs)

        search_query: str = self.request.GET.get('search', '')
        # В случае поиска по id или статусу
        if search_query:
            status_mapping = {
                'в ожидании': 1,
                'готово': 2,
                'оплачено': 3
            }

            if search_query.isdigit():
                orders = Order.objects.filter(
                    Q(id__icontains=search_query)
                )
            else:
                status_value = status_mapping.get(search_query.lower())
                if status_value:
                    orders = Order.objects.filter(status=status_value)
                else:
                    orders = Order.objects.none()
        else:
            orders = Order.objects.all()

        order_details: dict = {}
        for order in orders:
            carts = Cart.objects.filter(order=order.id)
            total_order_price: float = sum(cart.total_price for cart in carts)
            order_details[order] = {
                'carts': carts,
                'total_order_price': total_order_price
            }

        context['order_details'] = order_details
        context['search_query'] = search_query
        return context


class OrderUpdateView(generic.UpdateView):
    """
    Представление для обновления статуса заказа.
    """
    model = Order
    template_name = 'Orders/form.html'
    fields = ['status']
    success_url = reverse_lazy('Orders:order-list')


class OrderDeleteView(generic.DeleteView):
    """
    Представление для удаления заказа.
    """
    model = Order
    template_name = 'Orders/confirm_delete.html'
    success_url = reverse_lazy('Orders:order-list')


def calculation_revenue(request) -> render:
    """
    Вычисляет общую выручку от оплаченных заказов.
    :param request: Объект HTTP-запроса.

    :return: render: HTML-ответ с отображением общей выручки.
    """
    orders = Order.objects.all()
    revenue: float = 0

    for order in orders:
        if order.status == 3:
            carts = Cart.objects.filter(order=order.id)
            order_price: float = sum(cart.total_price for cart in carts)
            revenue += order_price

    return render(request, 'Orders/revenue.html', {'revenue': revenue})
