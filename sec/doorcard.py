# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from .models import DoorCard
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def door(request):
    context = {}
    cards = DoorCard.objects.all()
    context['cards'] = cards
    user = request.user
    try:
        user_card = DoorCard.objects.get(owner=user)
    except Exception:
        user_card = None
    if request.method == 'POST':
        card_id = request.POST.get('card')
        user_card = DoorCard.objects.get(id=card_id)
        user_card.owner = user
        user_card.save()
    if user_card:
        if request.GET.get('status'):
            status = request.GET.get('status')
            if status == 'in':
                settings.DOOR = True
            elif status == 'out':
                settings.DOOR = False
            user_card.status = status
            user_card.save()
    context['user_card'] = user_card
    return render(request, 'doorcard.html', context)

@login_required
def close(request):
    settings.DOOR = False
    return HttpResponseRedirect('/')
