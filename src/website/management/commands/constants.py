from products.models import Comment, Product, StoreProduct, Coupon, Discount, Color
from orders.models import Order, OrderItem
from vendors.models import Staff, Store

PERMISSIONS = {
    1: 'view',
    2: 'add',
    3: 'change',
    4: 'delete'
}

OWNER = 'owner'
MANAGER = 'manager'
OPERATOR = 'operator'

GROUPS = {
    OWNER: {
        # owner specific
        Store: [1, 3],
        Staff: [1, 2, 3, 4],

        # others
        StoreProduct: [1, 2, 3, 4],
        Discount: [1, 2, 3, 4],
        Order: [1, 2, 3, 4],
        OrderItem: [1, 2, 3, 4],
    },
    MANAGER: {
        Store: [1, ],
        StoreProduct: [1, 2, 3, 4],
        Discount: [1, 2, 3, 4],
        Order: [1, 2, 3, 4],
        OrderItem: [1, 2, 3, 4],
    },
    OPERATOR: {
        Store: [1, ],
        StoreProduct: [1, ],
        Discount: [1, ],
        Order: [1, ],
        OrderItem: [1, ],

    }

}
