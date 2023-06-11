from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render, redirect

from custom_auth.models import CustomGroup
from dsbd.ticket.form import TicketForm, TicketInitForm
from dsbd.ticket.models import Ticket, Template


@login_required
def index(request):
    ticket_objects = Ticket.objects.get_ticket(user=request.user)

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
    ticket_type = "user"
    template = Template.objects.get_template()
    form = TicketForm()
    init_form = TicketInitForm()
    id = 'select_init'
    groups = request.user.groups.filter(customgroup__is_active=True)
    if request.method == 'GET':
        ticket_type_template = [('user', 'ユーザチケット')]
        if groups.exists():
            for group in groups:
                ticket_type_template.append(
                    (str(group.id), 'グループチケット (Group' + str(group.id) + ': ' + group.name + ')')
                )
            init_form.fields['ticket_type'].choices = ticket_type_template

    elif request.method == 'POST':
        id = request.POST.get("id", "ticket_regist")
        template_id = int(request.POST.get("template_id", 0))
        ticket_type = request.POST.get("ticket_type", "user")
        if id == 'select_init':
            init_form = TicketInitForm(request.POST)
            id = 'select_template'
        elif id == 'select_template':
            template = Template.objects.get(id=template_id)
            form = TicketForm(initial={
                'type1': template.type1,
                'type2': template.type2,
                'title': template.title,
                'body': template.body
            })
            id = 'ticket_regist'
        else:
            group = None
            if ticket_type != 'user':
                # この場合はgroup
                if groups.exists() & groups.filter(id=int(ticket_type)).exists():
                    group = CustomGroup.objects.filter(id=int(ticket_type)).first()

            form = TicketForm(request.POST)
            if form.is_valid():
                Ticket.objects.create(
                    group=group,
                    user=request.user,
                    type1=form.cleaned_data.get('type1'),
                    type2=form.cleaned_data.get('type2'),
                    title=form.cleaned_data.get('title'),
                    body=form.cleaned_data.get('body'),
                ).save()

                return redirect('/ticket')

    context = {
        'id': id,
        'template': template,
        'init_form': init_form,
        'form': form,
        'template_id': template_id,
        'ticket_type': ticket_type
    }
    return render(request, "ticket/add.html", context)
