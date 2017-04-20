from django.shortcuts import render
from nested_tree_app.models import Category
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# Create your views here.

@cache_page(60)
def show_all(request):
    return render(request,
                  "show_categories.html",
                  {'nodes':Category.objects.all()}
                  )

def get_desc(request):

    if request.method == 'GET':
        pk = request.GET['pk']

    desc = Category.objects.get(pk=pk).description

    return HttpResponse(desc)