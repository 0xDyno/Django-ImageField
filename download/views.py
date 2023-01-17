from django.core.files.base import ContentFile
from django.shortcuts import render

import requests

from .forms import SaveFromPcForm, SaveFromUrlForm
from .models import SaveModel, folder

# Create your views here.


def index(request):
    if request.method == "POST":
        form_pc = SaveFromPcForm(request.POST, request.FILES)
        form_url = SaveFromUrlForm(request.POST)
        
        if form_pc.is_valid():
            img = form_pc.cleaned_data["img"]
            # That's VERY IMPORTANT - pass where you want to give img >>> (img=img), DON'T DO SaveModel(img)
            img_file = SaveModel(img=img)
            img_file.save()
            
        if form_url.is_valid():
            url = form_url.cleaned_data.get("url")
            name = url.split("/").pop()
            
            r = requests.request(url=url, method="GET")
            content = ContentFile(r.content)
            
            save_model = SaveModel()
            save_model.img.save(content=content, name=name)
            save_model.save()
            
            
    context = {
        "form_pc": SaveFromPcForm(),
        "form_url": SaveFromUrlForm(),
        "all_images": get_saved_images(),
    }
    
    return render(request, "index.html", context=context)


def get_saved_images():
    objects = SaveModel.objects.all()
    if not objects:
        return {"message": "No photos yet"}
    
    # obj               >> SaveModel
    # obj.img           >> ImageFieldFile
    # obj.img.name      >> str | /static/images/ava2.png
    # obj.img.field     >> download.SaveModel.img
    # obj.img.size      >> 2591196
    # obj.img.url       >> download/static/images/ava2.png
    # obj.img.file      >> full path User/.../download/static/images/ava2.png
    
    imgs = []
    for obj in objects:
        # get str path
        raw_path = obj.img.name
        # change to have only last folder + filename -> images/ava2.png
        path = folder + raw_path.split("/").pop()
        imgs.append(path)
    
    return imgs