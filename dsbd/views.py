from django.contrib.auth import logout as user_logout, authenticate, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from custom_auth.models import UserActivateToken, SignUpKey, User
from dsbd.form import LoginForm, ForgetForm, NewSetPasswordForm, SignUpForm
from dsbd.notice.models import Notice
from dsbd.service.models import Service
from dsbd.ticket.models import Ticket


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                user_login(request, user)
                return redirect("/")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, "sign_in.html", context)


@login_required
def sign_out(request):
    user_logout(request)
    context = {}
    return render(request, "sign_out.html", context)


def sign_up(request):
    key = ''
    key_error = ''
    error = ''
    form = SignUpForm()
    if request.method == 'POST':
        id = request.POST.get("id", "input_key")
        key = request.POST.get("key", "")
        form = SignUpForm(request.POST)
        if id == "input_key":
            if not SignUpKey.objects.check_key(key):
                key_error = '認証キーが異なります'

        else:
            if form.is_valid():
                try:
                    form.create_user(key)
                    return render(request, "sign_up_success.html", {})
                except ValueError as error:
                    print(error)
                    error = error
                except:
                    error = '何かしらのエラーが発生しました'
    context = {'form': form, 'key': key, 'key_error': key_error, 'error': error}
    print(context)

    return render(request, "sign_up.html", context)


class PasswordReset(PasswordResetView):
    subject_template_name = 'mail/password_reset/subject.txt'
    email_template_name = 'mail/password_reset/message.txt'
    template_name = 'forget.html'
    form_class = ForgetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'forget_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = NewSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'forget_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'forget_complete.html'


def activate_user(request, activate_token):
    message = 'ユーザーのアクティベーションが完了しました'
    try:
        UserActivateToken.objects.activate_user_by_token(activate_token)
    except ValueError as error:
        message = error
    except:
        message = 'エラーが発生しました。管理者に問い合わせてください'
    return render(request, "activate.html", {"message": message})


@login_required
def index(request):
    notice_objects = Notice.objects.get_notice()
    ticket_objects = Ticket.objects.get_ticket(user=request.user).filter(is_solved=False)

    notice_paginator = Paginator(notice_objects, int(request.GET.get("notice_per_page", "5")))
    notice_page = int(request.GET.get("notice_page", "1"))
    try:
        notices = notice_paginator.page(notice_page)
    except (EmptyPage, InvalidPage):
        notices = notice_paginator.page(notice_paginator.num_pages)

    ticket_paginator = Paginator(ticket_objects, int(request.GET.get("ticket_per_page", "3")))
    ticket_page = int(request.GET.get("ticket_page", "1"))
    try:
        tickets = ticket_paginator.page(ticket_page)
    except (EmptyPage, InvalidPage):
        tickets = ticket_paginator.page(ticket_paginator.num_pages)

    services = None

    group_filter = request.user.groups.filter(is_active=True)
    if group_filter.exists():
        service_objects = Service.objects.get_service(groups=group_filter.all()).filter(is_active=True)
        service_paginator = Paginator(service_objects, int(request.GET.get("ticket_per_page", "3")))
        service_page = int(request.GET.get("ticket_page", "1"))
        try:
            services = service_paginator.page(service_page)
        except (EmptyPage, InvalidPage):
            services = service_paginator.page(service_paginator.num_pages)

    context = {"notices": notices, "tickets": tickets, "services": services}
    return render(request, "menu.html", context)
