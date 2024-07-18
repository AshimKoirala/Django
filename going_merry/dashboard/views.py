from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from item.models import Item


@login_required
def index(request):
    items = Item.objects.filter(created_By=request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
    })


def edit_profile(request):
    return render(request, 'dashboard/editprofile.html')
