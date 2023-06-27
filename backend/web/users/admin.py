from cuser.admin import UserAdmin
from django.contrib import admin

from web.users.models import User

admin.site.register(User, UserAdmin)
