from django.shortcuts import render

from .forms import SaveForm
from .models import SaveModel, folder

# Create your views here.


def index(request):
    if request.method == "POST":
        form = SaveForm(request.POST, request.FILES)
        print("\n\n{} \n >>>>>> {}\n\n".format(form, form.is_valid()))
        if form.is_valid():
            img = form.cleaned_data["img"]
            # That's VERY IMPORTANT - pass where you want to give img >>> (img=img), DON'T DO SaveModel(img)
            img_file = SaveModel(img=img)
            img_file.save()
            
    context = get_saved_images()
    
    context["form"] = SaveForm()
    return render(request, "index.html", context=context)


def get_saved_images():
    objects = SaveModel.objects.all()
    if not objects:
        return {"message": "No photos yet"}
    
    # obj               >> SaveModel
    # obj.img           >> ImageFieldFile
    # obj.img.name      >> str | app/static/images/ava2.png
    # obj.img.field     >> app.SaveModel.img
    # obj.img.size      >> 2591196
    # obj.img.url       >> app/static/images/ava2.png
    # obj.img.file      >> full path User/.../app/static/images/ava2.png
    
    imgs = []
    for obj in objects:
        # get str path
        raw_path = obj.img.name
        # change to have only last folder + filename -> images/ava2.png
        path = folder + raw_path.split("/").pop()
        imgs.append(path)
    
    return {"all_images": imgs}