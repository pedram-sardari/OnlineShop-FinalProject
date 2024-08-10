from django.contrib.auth.mixins import UserPassesTestMixin

from vendors.models import Owner


class IsAddressForLoggedInUser(UserPassesTestMixin):
    def test_func(self):
        selected_address = self.get_object()  # NOQA
        return self.request.user.addresses.contains(selected_address)  # NOQA


class IsOwner(UserPassesTestMixin):
    def test_func(self):
        return Owner.is_owner(self.request.user)  # NOQA


class IsStaffOfOwnerStore(UserPassesTestMixin):
    """Is the selected staff one of staffs of the owner's store?"""

    def test_func(self):
        if owner := Owner.get_owner(self.request.user):  # NOQA
            selected_staff = self.get_object()  # NOQA
            return owner.store.staffs.contains(selected_staff)
        return False
