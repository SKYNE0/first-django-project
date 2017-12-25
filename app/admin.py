
from django.contrib import admin


from app.models import UserInfo, StoreHouse, Goods, Supplier, WaveHousing, StockOut
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = '欢迎来到仓库管理系统'
    site_title = '仓库管理系统'


admin_site = MyAdminSite(name='myadmin')


admin.site.register(UserInfo)

admin.site.register(StoreHouse)

admin.site.register(Goods)

admin.site.register(Supplier)

# admin.site.register(Storage)

admin.site.register(WaveHousing)

admin.site.register(StockOut)