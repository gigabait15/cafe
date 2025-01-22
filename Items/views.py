from typing import Any, Dict

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import generic

from Carts.models import Cart
from Items.models import Item
from Orders.models import Order


class ItemListView(generic.ListView):
    """
    Представление для отображения списка доступных блюд.
    """
    model = Item
    template_name = 'Items/item_list.html'


def add_to_cart(request, item_id: int) -> JsonResponse:
    """
    Добавляет блюдо в корзину, используя данные из сессии.
    :param request: Объект HTTP-запроса.
    :param item_id: ID блюда, которое добавляется в корзину.

    :return: JsonResponse: Ответ с сообщением о добавлении блюда в корзину.
    """
    cart: Dict[str, int] = request.session.get('cart', {})
    item: Item = Item.objects.get(id=item_id)

    # Проверка наличия блюда в корзине
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1

    request.session['cart'] = cart
    return JsonResponse({'message': f"Блюдо '{item.name}' добавленo в заказ"})


def view_cart(request) -> JsonResponse:
    """
    Возвращает содержимое корзины в формате JSON.
    :param request: Объект HTTP-запроса.

    :return: JsonResponse: JSON-ответ с деталями корзины и общим количеством товаров.
    """
    cart: Dict[str, int] = request.session.get('cart', {})
    items = Item.objects.filter(id__in=cart.keys())
    total_item_count: int = sum(cart.values())

    return JsonResponse({
        'items': [{
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': cart.get(str(item.id), 0)
        } for item in items],
        'total_item_count': total_item_count
    })


def cart_items(request) -> render:
    """
    Отображает содержимое корзины с деталями каждого блюда.
    :param request: Объект HTTP-запроса.

    :return: render: HTML-ответ с отображением содержимого корзины.
    """
    cart: Dict[str, int] = request.session.get('cart', {})
    items = Item.objects.filter(id__in=cart.keys())
    total_item_count: int = sum(cart.values())

    items_cart: list[Dict[str, Any]] = [{
        'name': item.name,
        'quantity': cart.get(str(item.id), 0),
        'price': item.price,
        'item_price': item.price * cart.get(str(item.id), 0),
    } for item in items]

    total_price: float = sum(item['item_price'] for item in items_cart)

    return render(request, 'Items/cart.html', {
        'items': items_cart,
        'total_item_count': total_item_count,
        'total_price': total_price,
    })


def clear_cart(request) -> JsonResponse:
    """
    Очищает содержимое корзины.
    :param request: Объект HTTP-запроса.

    :return: JsonResponse: Ответ с сообщением об очистке корзины.
    """
    request.session['cart'] = {}
    return JsonResponse({'message': 'Корзина очищена'})


def confirm_order(request) -> redirect:
    """
    Подтверждает текущую корзину как заказ и очищает корзину.
    :param request: Объект HTTP-запроса.

    :return:redirect: Перенаправление на страницу меню или корзины, если корзина пуста.
    """
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        cart: Dict[str, int] = request.session.get('cart', {})
        # если корзина пуста
        if not cart:
            return redirect('Items:cart_items')

        # Создаем экземпляра заказа и позиций связанных с заказом в БД
        order = Order.objects.create(table_number=table_number)

        for item_id, quantity in cart.items():
            item = Item.objects.get(id=item_id)
            Cart.objects.create(
                order=order,
                item_name=item.name,
                quantity=quantity,
                price=item.price,
            )
        # Чистка корзины
        request.session['cart'] = {}

        return redirect('Items:menu')
