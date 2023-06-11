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
                error = form.create_user(key)
                if not error:
                    return render(request, "sign_up_success.html", {})
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
    result = UserActivateToken.objects.activate_user_by_token(activate_token)
    message = ''
    if result["error"]:
        message = result["error"]
    else:
        if hasattr(result, 'is_active'):
            if result.is_active:
                message = 'ユーザーのアクティベーションが完了しました'
            if not result.is_active:
                message = 'アクティベーションが失敗しています。管理者に問い合わせてください'
        if not hasattr(result, 'is_active'):
            message = 'エラーが発生しました'
    return render(request, "activate.html", {"message": message})


@login_required
def index(request):
    notice_objects = Notice.objects.get_notice()

    paginator = Paginator(notice_objects, int(request.GET.get("per_page", "5")))
    page = int(request.GET.get("page", "1"))
    try:
        notices = paginator.page(page)
    except (EmptyPage, InvalidPage):
        notices = paginator.page(paginator.num_pages)

    context = {"notices": notices}
    return render(request, "menu.html", context)
