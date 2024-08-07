from accounts.models import Staff


def header_section_parameters(request):
    is_manager = False
    if request.user.is_superuser and request.user.is_staff:
        is_manager = True
    elif qs := Staff.objects.filter(id=request.user.id):
        staff = qs.first()
        if staff.role == 'manager':
            is_manager = True
    context = {
        'is_manager': is_manager,
        'is_staff': request.user.is_staff,
    }
    return context
