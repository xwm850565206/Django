from django.http import HttpResponse
from django.shortcuts import render
import Django.IOProcess as iop
from api.network.FCMAnswer import FCMAnswer
import os, sys

answer = FCMAnswer.getInstance()


def hello(request):
    # 通过给定context确定页面的初始值
    # context = {'default_mode': True}
    return render(request, "index.html")


def name_submit(request):
    company_name = request.POST['company_name']
    # 在此处拿到company_name 进行相关检索分类
    print("===========", company_name, "================")
    result = iop.fullNameSearch(company_name)
    if result is None:
        return render(request, 'index.html', {'result': '没有找到该公司'})

    context = {}
    construction_description = result['construction_descrption']
    context['label_compo1'] = ""
    context['label_compo2'] = ""
    context['label_compo3'] = ""
    context['label_compo4'] = ""
    len1 = len(construction_description['enttype'])
    for item in construction_description['enttype']:
        if item != construction_description['enttype'][len1 - 1]:
            context['label_compo1'] += (item[0] + "，")
        else:
            context['label_compo1'] += item[0]

    len2 = len(construction_description['entstatus'])
    for item in construction_description['entstatus']:
        if item != construction_description['entstatus'][len2 - 1]:
            context['label_compo2'] += (item[0] + "，")
        else:
            context['label_compo2'] += item[0]

    len3 = len(construction_description['entcat'])
    for item in construction_description['entcat']:
        if item != construction_description['entcat'][len3 - 1]:
            context['label_compo3'] += (item[0] + "，")
        else:
            context['label_compo3'] += item[0]

    len4 = len(construction_description['industryphy'])
    for item in construction_description['industryphy']:
        if item != construction_description['industryphy'][len4 - 1]:
            context['label_compo4'] += (item[0] + "，")
        else:
            context['label_compo4'] += item[0]

    if 'company_name' in result:
        context['company_name'] = result['company_name']
    else:
        context['company_name'] = "公司"

    context['label0'] = result['target_construction']
    context['label1'] = result['target_credit']
    context['label2'] = result['target_technique']
    context['label3'] = result['target_comsize']
    context['label4'] = result['target_strength']
    context['label5'] = result['target_stable']

    return render(request, "show.html", context)


def condition_submit(request):
    # 在此处拿到条件检索的输入 进行相关检索分类
    conditions = request.POST.dict()
    # print("============", conditions, "==================")
    result = iop.conditionSearch(conditions)
    context = {}
    construction_description = result['construction_descrption']
    context['label_compo1'] = ""
    context['label_compo2'] = ""
    context['label_compo3'] = ""
    context['label_compo4'] = ""
    len1 = len(construction_description['enttype'])
    for item in construction_description['enttype']:
        if item != construction_description['enttype'][len1 - 1]:
            context['label_compo1'] += (item[0] + "，")
        else:
            context['label_compo1'] += item[0]

    len2 = len(construction_description['entstatus'])
    for item in construction_description['entstatus']:
        if item != construction_description['entstatus'][len2 - 1]:
            context['label_compo2'] += (item[0] + "，")
        else:
            context['label_compo2'] += item[0]

    len3 = len(construction_description['entcat'])
    for item in construction_description['entcat']:
        if item != construction_description['entcat'][len3 - 1]:
            context['label_compo3'] += (item[0] + "，")
        else:
            context['label_compo3'] += item[0]

    len4 = len(construction_description['industryphy'])
    for item in construction_description['industryphy']:
        if item != construction_description['industryphy'][len4 - 1]:
            context['label_compo4'] += (item[0] + "，")
        else:
            context['label_compo4'] += item[0]

    if 'company_name' in result:
        context['company_name'] = result['company_name']
    else:
        context['company_name'] = "公司"

    context['label0'] = result['target_construction']
    context['label1'] = result['target_credit']
    context['label2'] = result['target_technique']
    context['label3'] = result['target_comsize']
    context['label4'] = result['target_strength']
    context['label5'] = result['target_stable']
    return render(request, "show.html", context)
    pass


def show(request):
    context = {}
    context['label_compo1'] = "组成字段1"
    context['label_compo2'] = "组成字段2"
    context['label_compo3'] = "组成字段3"
    context['label_compo4'] = "组成字段4"
    context['company_name'] = "瑞星咖啡"
    context['label1'] = "标签字段2"
    context['label2'] = "标签字段2"
    context['label3'] = "标签字段2"
    context['label4'] = "标签字段2"
    context['label5'] = "标签字段2"
    return render(request, "show.html", context)


def fileUpload(request):
    HttpResponse("上传成功！")
    File = request.FILES.get("batchFile", None)
    if File is None:
        return HttpResponse("no files for upload!")
    else:
        destination = os.path.join(os.getcwd(), 'file', File.name)
        print(destination, "=============")
        # 打开特定的文件进行二进制的写操作;
        with open(destination, 'wb+') as f:
            # 分块写入文件;
            for chunk in File.chunks():
                f.write(chunk)

        # destination 为上传的路径名称 （绝对路径）
        try:
            destination = iop.mutiSearch(destination)  # 批量查询操作
        except ValueError:  # 这块有时间应该告诉详细的错误地方
            return HttpResponse("格式错误")
        
        return HttpResponse("上传成功！")
