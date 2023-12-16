from apps.product.models import CartItem


def get_total_bill(user_id):
    """
    this method is used to get a total billed
    :param user_id
    return total billed
    """
    total_bill = 0
    cart_obj = CartItem.objects.filter(user_id=user_id)
    if cart_obj:
        for cart in cart_obj:
            sub_price = cart.quantity * cart.product.price
            total_bill += sub_price
    return total_bill
