from django.http import HttpResponse
from django.shortcuts import render
import Django.IOProcess as iop
from api.network.FCMAnswer import FCMAnswer

answer = FCMAnswer.getInstance()


def hello(request):
    # 通过给定context确定页面的初始值
    # context = {'default_mode': True}
    return render(request, "index.html")


def name_submit(request):
    company_name = request.POST['company_name']
    # 在此处拿到company_name 进行相关检索分类
    print("===========", company_name, "================")
    context = {'result': company_name}
    iop.fullNameSearch(company_name)
    return render(request, "index.html", context)


def condition_submit(request):
    # 在此处拿到条件检索的输入 进行相关检索分类
    conditions = request.POST.dict()
    # print("============", conditions, "==================")
    iop.conditionSearch(conditions)
    return render(request, "index.html")
    pass


def show(request):
    return render(request, "show.html")