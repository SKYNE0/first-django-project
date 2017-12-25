from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User

from django.contrib import messages

from app.forms import UserInfoForm, UserForm, InfoChange

from app.models import UserInfo, StoreHouse, Supplier, Goods, StockOut, WaveHousing

# Create your views here.
# 改视图函数无意义，只是单纯重定向到登录界面
def index(request):
    return redirect(to= 'login')

def index_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 判断用户是否存在
            user = authenticate(username= username, password= password)
            print(user)
            if user:
                login(request, user)
                return redirect(to= 'infomanage')
            else:
                messages.add_message(request, messages.ERROR, "账号或密码错误，请重新输入！")
                return redirect (to='login')
    else:
        form = UserForm()
        return render(request, 'login.html', {'form' : form})


def index_logout(request):
    logout(request)
    messages.add_message (request, messages.ERROR, "退出登录成功,请您重新登陆！")
    return redirect(to='login')


def register(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_exist = User.objects.filter(username= username)
            if user_exist:
                messages.add_message(request, messages.ERROR, "用户名已存在,请更换！")
                return redirect(to= 'register')
            else:
                user = UserInfo()
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
                user.sex = form.cleaned_data['sex']
                user.job = form.cleaned_data['job']
                user.job_num = form.cleaned_data['job_num']
                user.save()
                login(request, user)
                return redirect(to= 'infomanage')

    elif request.method == 'GET':
        form = UserInfoForm
        return render(request, 'register.html', {'form' : form})


def infochange(request):
    if request.method == 'POST':
        form = InfoChange(request.POST)
        if form.is_valid():
            oldusername = form.cleaned_data['oldusername']
            user = User.objects.filter(username= oldusername)
            print(oldusername, user)
            if user:
                user = User.objects.get(username= oldusername)
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
                user.sex = form.cleaned_data['sex']
                user.save()
                messages.add_message (request, messages.ERROR, "信息更改成功，请重新登录！")
                return redirect(to= 'login')

            else:
                messages.add_message(request, messages.ERROR, "用户名不存在,请先注册！")
                return redirect(to= 'register')

    elif request.method == 'GET':
        form = InfoChange
        return render(request, 'infochange.html', {'form' : form})

@login_required(login_url='/', redirect_field_name='login')
def infomanage(request):
    context = {}
    query = None
    flag = None
    if request.method == 'GET':
        page = request.GET.get('page')
        if request.GET.get('query'):
            query = request.GET.get('query')
            print(query)
        else:
            for i in ['goodsstore','storagestore','stockoutstore','wavestore']:
                if request.GET.get(i):
                    query = i
                    print(i, request.GET.get(i))
                    break

        if query == 'storehouse':
            context['store_inver'] = 'inverted'
            context['name'] = query
            each_object = StoreHouse.objects.all()
            print(each_object)
            paginator = Paginator(each_object,7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        if query == 'supplier':
            context['sup_inver'] = 'inverted'
            context['name'] = query
            each_object = Supplier.objects.all()
            print(each_object)
            paginator = Paginator(each_object,7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts
        # a = ['goodsstore','storagestore','stockoutstore','wavestore']
        elif query == 'goods':
            context['goods_inver'] = 'inverted'
            context['name'] = 'goods'
            each_object = Goods.objects.all()
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'goodsstore':
            context['goods_inver'] = 'inverted'
            context['name'] = 'goods'
            goods_store = request.GET.get('goodsstore')
            goodsInfo = request.GET.get('goodsInfo')
            print(goodsInfo)
            if goodsInfo:
                try:
                    each_object = Goods.objects.filter(goods_name__contains=goodsInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    pass

                try:
                    each_object = Goods.objects.filter(goodsID = goodsInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    pass

                if flag:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
            else:
                if goodsInfo:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
                else:
                    each_object = Goods.objects.filter(goods_store=goods_store)
                    if each_object and goods_store:
                        context['each_object'] = each_object
                    else:
                        messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")


        # elif query == 'storage':
        #     context['storage_inver'] = 'inverted'
        #     context['name'] = query
        #     each_object = Storage.objects.all()
        #     paginator = Paginator(each_object, 7)
        #     try:
        #         contacts = paginator.page(page)
        #     except PageNotAnInteger:
        #         contacts = paginator.page(1)
        #     except EmptyPage:
        #         contacts = paginator.page(Paginator.num_pages)
        #
        #     context['each_object'] = contacts
        #     print(dir(context['each_object']))
        #
        # elif query == 'storagestore':
        #     context['storage_inver'] = 'inverted'
        #     context['name'] = 'storage'
        #     goods_store = request.GET.get('storagestore')
        #     goodsID = request.GET.get('goodsID')
        #     goodsName = request.GET.get('goodsName')
        #     print(goodsName)
        #     if goodsName:
        #         try:
        #             each_object = Goods.objects.filter(goods_name__contains=goodsName)
        #             if each_object:
        #                 context['each_object'] = each_object
        #                 flag = True
        #         except ValueError:
        #             pass
        #
        #     else:
        #         if goodsID:
        #             try:
        #                 each_object = Goods.objects.filter(goodsID=goodsID)
        #                 if each_object:
        #                     context['each_object'] = each_object
        #                     flag = True
        #             except ValueError:
        #                 pass
        #             if not flag:
        #                 messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
        #         else:
        #             each_object = Storage.objects.filter(goods_store=goods_store)
        #             if each_object and goods_store:
        #                 context['each_object'] = each_object
        #                 flag = True
        #             if not flag:
        #                 messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")

        elif query == 'stockout':
            context['stockout_inver'] = 'inverted'
            context['name'] = query
            each_object = StockOut.objects.all()
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'stockoutstore':
            context['stockout_inver'] = 'inverted'
            context['name'] = 'stockout'
            goods_store = request.GET.get('stockoutstore')
            goodsInfo = request.GET.get('goodsInfo')
            supInfo = request.GET.get('supInfo')
            print(goodsInfo,supInfo)
            if goodsInfo:
                try:
                    each_object = StockOut.objects.filter(goods_name__contains=goodsInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    pass

                if not flag:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
            elif supInfo:
                try:
                    each_object = StockOut.objects.filter(sup_name=supInfo)
                    print(each_object, supInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    print(ValueError)

                if not flag:
                    messages.add_message(request, messages.ERROR, "未找到供应商，请联系管理员！")

            else:
                if goodsInfo or supInfo:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
                else:
                    each_object = StockOut.objects.filter(sto_name=goods_store)
                    print(goods_store)
                    if each_object and goods_store:
                        context['each_object'] = each_object
                    else:
                        messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")



        elif query == 'wavehousing':
            context['wavehouse_inver'] = 'inverted'
            context['name'] = query
            each_object = WaveHousing.objects.all()
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'wavestore':
            context['wavehouse_inver'] = 'inverted'
            context['name'] = 'wavehousing'
            goods_store = request.GET.get('stockoutstore')
            goodsInfo = request.GET.get('goodsInfo')
            supInfo = request.GET.get('supInfo')
            print(goodsInfo,supInfo)
            if goodsInfo:
                try:
                    each_object = WaveHousing.objects.filter(goods_name__contains=goodsInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    pass

                if not flag:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
            elif supInfo:
                try:
                    each_object = WaveHousing.objects.filter(sup_name=supInfo)
                    print(each_object, supInfo)
                    if each_object:
                        context['each_object'] = each_object
                        flag = True
                except ValueError:
                    print(ValueError)

                if not flag:
                    messages.add_message(request, messages.ERROR, "未找到供应商，请联系管理员！")

            else:
                if goodsInfo or supInfo:
                    messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")
                else:
                    each_object = StockOut.objects.filter(sto_name=goods_store)
                    print(goods_store)
                    if each_object and goods_store:
                        context['each_object'] = each_object
                    else:
                        messages.add_message(request, messages.ERROR, "未找到商品，请联系管理员！")

        elif query == 'querysearch':
            context['goods_inver'] = 'inverted'
            context['name'] = 'goods'
            each_object = Goods.objects.filter(goods_name__contains=query)
            if each_object:
                context['each_object'] = each_object
            else:
                messages.add_message (request, messages.ERROR, "未找到商品，请联系管理员！")
            # context['stockout_inver'] = 'inverted'
            # context['name'] = 'stockout'
            # each_object = StockOut.objects.filter(sup_name=query)
            # print(query, each_object)
            # if each_object:
            #     context['each_object'] = each_object
            # else:
            #     messages.add_message (request, messages.ERROR, "未找到商品，请联系管理员！")


        return render(request, 'infomanage.html', context= context)

