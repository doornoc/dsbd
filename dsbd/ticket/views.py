from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, redirect

from custom_auth.models import Group
from dsbd.ticket.form import TicketForm
from dsbd.ticket.models import Ticket, Template


@login_required
def index(request):
    ticket_objects = Ticket.objects.get_ticket(user=request.user)
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        if "no_solved" in request.POST:
            ticket = Ticket.objects.get_one_ticket(int(id), request.user)
            ticket.is_solved = False
            ticket.save()
        elif "solved" in request.POST:
            ticket = Ticket.objects.get_one_ticket(int(id), request.user)
            ticket.is_solved = True
            ticket.save()
        return redirect('/ticket')

    paginator = Paginator(ticket_objects, int(request.GET.get("per_page", "5")))
    page = int(request.GET.get("page", "1"))
    try:
        tickets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tickets = paginator.page(paginator.num_pages)
    context = {
        "tickets": tickets,
    }
    return render(request, "ticket/index.html", context)


@login_required
def ticket_add(request):
    template_id = None
    template = Template.objects.get_template()
    groups = request.user.groups.filter(is_active=True)
    form = TicketForm(groups, request.POST)
    id = ""

    if request.method == 'POST':
        template_id = int(request.POST.get("template_id", 0))
        if template_id != 0 and form.is_valid():
            group = None
            ticket_type = form.cleaned_data.get('ticket_type')
            if ticket_type != 'user':
                # この場合はgroup
                if groups.exists() & groups.filter(id=int(ticket_type)).exists():
                    group = Group.objects.filter(id=int(ticket_type)).first()
            if form.is_valid():
                Ticket.objects.create(
                    group=group,
                    user=request.user,
                    template=Template.objects.get(id=template_id),
                    title=form.cleaned_data.get('title'),
                    body=form.cleaned_data.get('body'),
                ).save()
                return redirect('/ticket')

        template = Template.objects.get(id=template_id)
        form = TicketForm(groups, initial={
            'type1': template.type1,
            'type2': template.type2,
            'title': template.title,
            'body': template.body
        })
        id = 'ticket_regist'

    context = {
        'id': id,
        'template': template,
        'form': form,
        'template_id': template_id,
    }
    return render(request, "ticket/add.html", context)


@login_required
def chat(request, ticket_id):
    ticket = Ticket.objects.get_one_ticket(ticket_id, request.user)

    if request.method == 'POST':
        if "no_solved" in request.POST:
            ticket.is_solved = False
            ticket.save()
        elif "solved" in request.POST:
            ticket.is_solved = True
            ticket.save()
        return redirect('/ticket/' + str(ticket_id) + '/chat')

    if not ticket:
        return render(request, "ticket/chat_error.html", {})
    context = {"ticket": ticket, "chats": ticket.chat_set.order_by('created_at').all()}
    return render(request, "ticket/chat.html", context)
