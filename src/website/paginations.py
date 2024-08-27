from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
