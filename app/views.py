import base64

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
import logging
from app.controller.DS import toDS
from app.controller.predictionImage import predictionImage
from app.controller.toimage import base64toimg, checkimg

import json

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'blog/index.html'

    def get_queryset(self):
        """
        过滤数据，并转为html格式
        Returns:

        """
        return


def InputImage(request, ):
    print("function InputImage start:")
    print("request: ", request)
    image_data = str(request.GET['image_data'])
    tag = str(request.GET['tag'])
    # 获取图片数据
    print("tag: ", tag)
    print("image_data: ", image_data)

    strg = image_data.split(',')[1]
    result = base64toimg(strg, tag)
    return HttpResponse(result)


# 参考代码
def blog_search(request, ):
    print("function start:")
    # form = ImageForm()
    # if request.method == 'post':
    #     form = ImageForm(request.POST)

    return HttpResponse("上传成功")


# 参考代码
def suggest_view(request):
    # form = SuggestForm()
    # if request.method == 'POST':
    #     form = SuggestForm(request.POST)
    #     if form.is_valid():
    #         suggest_data = form.cleaned_data['suggest']
    #         # new_record = Suggest(suggest=suggest_data)
    #         # new_record.save()
    #         # try:
    #         #     # 使用celery并发处理邮件发送的任务
    #         #     celery_send_email.delay('访客意见', suggest_data, 'haibincoder@outlook.com', ['tomming233@163.com'])
    #         # except Exception as e:
    #         #     logger.error("邮件发送失败: {}".format(e))
    #         return redirect('app:thanks')
    return render(request, 'blog/about.html')


def addImageToMNIST(request):
    print("add start")
    result = toDS()

    return HttpResponse('添加图片到数据集完成')


def check(request, ):
    print("function InputImage start:")
    print("request: ", request)
    image_data = str(request.GET['image_data'])
    tag = str(request.GET['tag'])
    # 获取图片数据
    print("tag: ", tag)
    print("image_data: ", image_data)

    strg = image_data.split(',')[1]
    result = checkimg(strg)
    print("image path: ", result)
    response = predictionImage(result)
    return HttpResponse(response)
