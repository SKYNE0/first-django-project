# Generated by Django 2.0 on 2017-12-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20171217_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='goods_store',
        ),
        migrations.AddField(
            model_name='goods',
            name='goods_store',
            field=models.ManyToManyField(null=True, to='app.StoreHouse', verbose_name='所属仓库名称:'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='job',
            field=models.CharField(choices=[('保管员', '保管员'), ('统计员', '统计员'), ('普通员工', '普通员工'), ('仓库主管', '仓库主管'), ('记帐员', '记帐员')], default='普通员工', max_length=10, verbose_name='职位:'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='sex',
            field=models.CharField(choices=[('female', '女'), ('male', '男')], default='女', max_length=10, verbose_name='性别:'),
        ),
    ]