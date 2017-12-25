from django.db import models

from django.contrib.auth.models import User

# Create your models here.
#员工信息表
class UserInfo(models.Model):
    # related_name  会在request.user.中使用，也就是别名。
    account = models.OneToOneField(to= User, verbose_name='用户名:', null=True, related_name='userinfo', on_delete=models.CASCADE)
    sex_choice = {('male', '男'), ('female', '女'), }
    job_choice = {(u'保管员', '保管员'), (u'记帐员','记帐员'), (u'仓库主管','仓库主管'),(u'统计员','统计员'),(u'普通员工','普通员工')}
    sex = models.CharField(verbose_name='性别:', null=False, blank=False, max_length=10, choices= sex_choice, default='女')
    job = models.CharField(verbose_name='职位:', null=False, blank=False, max_length=10, choices= job_choice, default= u'普通员工')
    job_num = models.IntegerField(verbose_name='工号:', null=False, blank=False)

    def __str__(self):
        return self.account.username

    class Meta:
        # 管理界面显示中文
        verbose_name = verbose_name_plural = "员工信息管理"

# 仓库信息表
class StoreHouse(models.Model):
    stoID = models.IntegerField(primary_key=True, verbose_name='仓库编号:', null=False, blank=False,default= 100000)
    sto_name = models.CharField(verbose_name='仓库名称:', null=False, blank=False, max_length=20, default='请输入仓库名称')
    sto_locat = models.CharField(verbose_name='仓库地址:', null=False, blank=False, max_length=50, default='请输入仓库地址')
    sto_ps = models.TextField(verbose_name='备注:', null=True, blank= True, max_length= 500)

    @property
    def name(self):
        return self.sto_name

    def __str__(self):
        return self.sto_name

    class Meta:
        verbose_name = verbose_name_plural = '仓库信息管理'

# 供应商表
class Supplier(models.Model):
    supID = models.IntegerField(primary_key=True, verbose_name='供应商编号:', null=False, blank=False, default=300000)
    sup_name = models.CharField(verbose_name='供应商名称:', null=False, blank=False, max_length=20, default='请输入供应商名称')
    sup_tel = models.IntegerField(verbose_name='供应商电话:', null=True, blank=False)

    def __str__(self):
        return self.sup_name

    class Meta:
        verbose_name = verbose_name_plural = "供应商管理"


# 货物表
class Goods(models.Model):
    goods_store = models.ForeignKey(to=StoreHouse,null=True, verbose_name='所属仓库名称:', on_delete=models.CASCADE)
    goods_sup = models.ForeignKey(to=Supplier, null=True, verbose_name='供应商名称', on_delete=models.CASCADE)
    goodsID = models.IntegerField(primary_key=True, verbose_name='货物编号:', null=False, blank=False,default= 200000)
    goods_name = models.CharField(verbose_name='货物名称:', null=False, blank=False, max_length=20, default='请输入货物名称')
    goods_price =  models.IntegerField(verbose_name='货物价格:', null=False, blank=False, default= 0)
    good_amount = models.IntegerField(verbose_name='货物数量:', null=False, blank=False, default= 0)
    goods_max = models.IntegerField(verbose_name='最大库存量:', null=True, blank= False, default= 0)
    choice = {('台','台'),('颗','颗'),('千克','千克'),('斤','斤'),('袋','袋'),('箱','箱'),('瓶','瓶')}
    goods_mens = models.CharField(verbose_name='计量单位:', null=False, blank=False, choices=choice, max_length=20, default='请输入计量单位')
    create_date = models.DateTimeField(verbose_name= '更新日期:', null=True,blank=False)

    def __str__(self):
        return self.goods_name

    @property
    def name(self):
        return self.goods_name

    class Meta:
        verbose_name = verbose_name_plural = "货物信息管理"

# # 库存状况表
# class Storage(models.Model):
#     goods_store = models.ForeignKey(to=StoreHouse, verbose_name='所属仓库名称:',null=True,on_delete= models.CASCADE)
#     goods_name = models.ForeignKey(to=Goods, verbose_name='货物名称:', related_name='storage', primary_key= True,on_delete= models.CASCADE)
#     storage_amount = models.IntegerField(verbose_name='现有库存:', null=True, blank= False, default= 0)
#     storage_max = models.IntegerField(verbose_name='最大库存量:', null=True, blank= False, default= 0)
#     create_date = models.DateTimeField(verbose_name= '更新日期:', null=True,blank=False)
#
#     def __str__(self):
#         return str(self.goods_store)
#     class Meta:
#         verbose_name = verbose_name_plural = "货物库存管理"

# 入库表
class WaveHousing(models.Model):
    sto_name = models.ForeignKey(to=StoreHouse, verbose_name='所属仓库名称:', on_delete=models.CASCADE)
    sup_name = models.ForeignKey(to=Supplier, verbose_name='供应商名称:', on_delete= models.CASCADE)
    goods_name = models.OneToOneField(to=Goods, related_name='wave_goods', primary_key= True, verbose_name='货物名称:', on_delete= models.CASCADE)
    res_person = models.ForeignKey(to= UserInfo, verbose_name='经办人姓名:', on_delete= models.CASCADE)
    in_date = models.DateTimeField(verbose_name= '入库时间', null=False ,blank=False)
    in_price = models.FloatField(verbose_name='入库价格:', null=False,blank=False)
    in_amount = models.IntegerField(verbose_name='入库数量:', null=False,blank=False)
    in_ps = models.TextField(verbose_name='备注:', null=True, blank= True, max_length= 500)

    def __str__(self):
        return self.goods_name.name

    class Meta:
        verbose_name = verbose_name_plural = "入库单管理"

# 出库表
class StockOut(models.Model):
    sto_name = models.ForeignKey(to=StoreHouse, verbose_name='所属仓库名称:', on_delete=models.CASCADE)
    sup_name = models.ForeignKey(to=Supplier, verbose_name='供应商名称:', on_delete=models.CASCADE)
    goods_name = models.OneToOneField( to=Goods, related_name='stock_goods', primary_key= True, verbose_name='货物名称:',on_delete= models.CASCADE)
    res_person = models.ForeignKey(to= UserInfo, verbose_name='经办人姓名:', on_delete= models.CASCADE)
    out_date = models.DateTimeField (verbose_name='出库时间:', null=False, blank=False)
    out_price = models.FloatField (verbose_name='出库价格:', null=False, blank=False)
    out_amount = models.IntegerField (verbose_name='出库数量:', null=False, blank=False)
    out_ps = models.TextField (verbose_name='备注:', null=True, blank=True, max_length=500)

    def __str__(self):
        return self.goods_name.name

    class Meta:
        verbose_name = verbose_name_plural = "出库单管理"
