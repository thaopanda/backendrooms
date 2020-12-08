from django.contrib import admin
from Account.models import MyUser, Renter, Host

admin.site.register(MyUser)
admin.site.register(Renter)
admin.site.register(Host)
