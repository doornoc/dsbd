import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render, redirect

from dsbd.service.wireguard.api import wg_overwrite, wg_get
from dsbd.service.wireguard.models import Server as WireguardServer
from dsbd.ticket.models import Ticket


@login_required
@staff_member_required
def index(request):
    context = {
        "tickets": Ticket.objects.all()
    }
    return render(request, "custom_admin/index.html", context)


@login_required
@staff_member_required
def ticket_list(request):
    ticket_objects = Ticket.objects.all()
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        ticket = Ticket.objects.get(id=int(id))
        if "no_solved" in request.POST:
            ticket.is_solved = False
            ticket.save()
        elif "solved" in request.POST:
            ticket.is_solved = True
            ticket.save()
        return redirect('/admin/custom/ticket')

    paginator = Paginator(ticket_objects, int(request.GET.get("per_page", "5")))
    page = int(request.GET.get("page", "1"))
    try:
        tickets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tickets = paginator.page(paginator.num_pages)
    context = {
        "tickets": tickets,
    }
    return render(request, "custom_admin/ticket/index.html", context)


@login_required
@staff_member_required
def chat(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if not ticket:
        return render(request, "ticket/chat_error.html", {})
    context = {"ticket": ticket, "chats": ticket.chat_set.order_by('created_at').all()}
    return render(request, "custom_admin/ticket/chat.html", context)


@login_required
@staff_member_required
def wireguard_list(request):
    wireguard_server_objects = WireguardServer.objects.all()
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        server = WireguardServer.objects.get(id=int(id))
        if "inactive" in request.POST:
            server.is_active = False
            server.save()
        elif "active" in request.POST:
            server.is_active = True
            server.save()
        elif "register" in request.POST:
            wg_overwrite(server)
        elif "list" in request.POST:
            res = wg_get(server)
            return render(request, "custom_admin/wireguard/list.html", {'res': res})
        return redirect('/admin/custom/wireguard')

    paginator = Paginator(wireguard_server_objects, int(request.GET.get("per_page", "5")))
    page = int(request.GET.get("page", "1"))
    try:
        servers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        servers = paginator.page(paginator.num_pages)
    context = {
        "servers": servers,
    }
    return render(request, "custom_admin/wireguard/index.html", context)
