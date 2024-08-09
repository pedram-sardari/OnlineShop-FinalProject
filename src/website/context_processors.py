from customers.models import Customer
from vendors.models import Owner, Manager, Operator


def header_section_parameters(request):
    is_owner = Owner.objects.filter(id=request.user.id).exists()
    is_manager = Manager.objects.filter(id=request.user.id).exists()
    is_operator = Operator.objects.filter(id=request.user.id).exists()
    is_vendor = is_owner or is_manager or is_operator
    is_superuser = request.user.is_superuser and request.user.is_staff
    is_customer = not (is_owner or is_manager or is_operator)
    context = {
        'is_customer': is_customer,
        'is_owner': is_owner,
        'is_manager': is_manager,
        'is_operator': is_operator,
        'is_superuser': is_superuser,
        'is_vendor': is_vendor
    }
    return context
