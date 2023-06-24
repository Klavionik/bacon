from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import exceptions

User = get_user_model()


def filter_userproducts_by_username(queryset: QuerySet, username: str, current_user: User):
    if not (username == current_user.get_username() or current_user.is_staff):
        raise exceptions.PermissionDenied(f"You are not allowed to filter by {username=}.")

    return queryset.filter(user__username=username)


class UserProductFilter(filters.FilterSet):
    username = filters.CharFilter(method="by_username")

    def by_username(self, queryset, name, value):
        return filter_userproducts_by_username(queryset, value, self.request.user)
