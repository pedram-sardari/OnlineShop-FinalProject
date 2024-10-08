from orders.models import Order, OrderItem
from products.models import Comment, StoreProduct, Discount, StoreDiscount, Rating, Product
from vendors.models import Staff, Store
from .constants import UserType

PERMISSIONS = {
    1: 'view',
    2: 'add',
    3: 'change',
    4: 'delete'
}

GROUPS = {
    UserType.OWNER: {
        # owner specific
        Store: [1, 3],
        Staff: [1, 2, 3, 4],

        # others
        Product: [1, 2, 3, 4],
        StoreProduct: [1, 2, 3, 4],
        Discount: [1, 2, 3, 4],
        StoreDiscount: [1, 2, 3, 4],
        Order: [1, 2, 3, 4],
        OrderItem: [1, 2, 3, 4],
    },
    UserType.MANAGER: {
        Staff: [1, ],
        Store: [1, ],
        Product: [1, 2, 3, 4],
        StoreProduct: [1, 2, 3, 4],
        Discount: [1, 2, 3, 4],
        StoreDiscount: [1, 2, 3, 4],
        Order: [1, 2, 3, 4],
        OrderItem: [1, 2, 3, 4],
    },
    UserType.OPERATOR: {
        Staff: [1, ],
        Store: [1, ],
        StoreProduct: [1, ],
        Discount: [1, ],
        StoreDiscount: [1, ],
        Order: [1, ],
        OrderItem: [1, ],

    },
    UserType.CUSTOMER: {
        Comment: [1, 2],
        Rating: [1, 2],
        Order: [1, ],
        OrderItem: [1, ],
    }

}
