from .cart import Cart


def cart(request):
    """Контекстный процессор, необходимый для отображения корзины покупателя на всех вкладках нашего сайта."""
    context = {'cart': Cart(request)}
    return context

