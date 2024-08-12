from products.models import StoreProduct
from vendors.models import Owner, Manager, Operator


def header_section_parameters(request):
    is_owner = Owner.is_owner(request.user)
    is_manager = Manager.is_manager(request.user)
    is_operator = Operator.is_operator(request.user)
    is_staff = is_owner or is_manager or is_operator
    is_superuser = request.user.is_superuser and request.user.is_staff
    is_customer = not (is_staff or is_superuser)
    context = {
        'is_customer': is_customer,
        'is_owner': is_owner,
        'is_manager': is_manager,
        'is_operator': is_operator,
        'is_superuser': is_superuser,
        'is_staff': is_staff
    }
    return context


def store_products_list(request):
    context = {"store_product_list": StoreProduct.objects.filter(inventory__gt=0)}
    return context
