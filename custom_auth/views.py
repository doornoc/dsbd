from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from custom_auth.form import GroupForm
from custom_auth.models import UserGroup


@login_required
def get_groups(request):
    context = {
        "groups": request.user.groups.all()
    }
    return render(request, "group/index.html", context)


@login_required
def add_group(request):
    error = None
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if not request.user.add_group:
            error = "グループの新規登録が申請不可能です"
        elif form.is_valid():
            try:
                form.create_group(user_id=request.user.id)
                return render(request, "group/success.html", {})
            except ValueError as err:
                error = err
    else:
        form = GroupForm()
    context = {
        "form": form,
        "error": error
    }
    return render(request, "group/add.html", context)


@login_required
def edit_group(request, group_id):
    error = None
    administrator = False
    try:
        group = request.user.groups.get(id=group_id)
        group_data = {
            "name": group.name,
            "zipcode": group.zipcode,
            "address": group.address,
            "address_en": group.address_en,
            "email": group.email,
            "phone": group.phone,
            "country": group.country,
        }
        administrator = group.usergroup_set.filter(user=request.user, is_admin=True).exists()
        if request.method == 'POST' and administrator and group.is_active:
            form = GroupForm(data=request.POST)
            if form.is_valid():
                try:
                    form.update_group(group_id=group.id)
                    return render(request, "group/success.html", {})
                except ValueError as err:
                    error = err
        else:
            form = GroupForm(initial=group_data, edit=True, disable=not group.is_active)
    except:
        group = None
        form = None

    context = {
        "form": form,
        "group": group,
        "administrator": administrator,
        "error": error
    }
    return render(request, "group/edit.html", context)


@login_required
def permission_group(request, group_id):
    error = None
    administrator = False
    permission_all = False
    try:
        group = request.user.groups.get(id=group_id)
        permission_all = group.usergroup_set.all()
        administrator = group.usergroup_set.filter(user=request.user, is_admin=True).exists()
        if request.method == 'POST' and administrator and group.is_active:
            id = request.POST.get('id', 0)
            is_exists = False
            print("ID", id)
            print(request.POST)
            for permission_user in permission_all:
                if permission_user.id == int(id):
                    is_exists = True
                    break
            if not is_exists:
                error = "変更権限がありません"
            else:
                try:
                    user_group = UserGroup.objects.get(id=int(id))
                    if "no_admin" in request.POST:
                        user_group.is_admin = False
                        user_group.save()
                    elif "admin" in request.POST:
                        user_group.is_admin = True
                        user_group.save()
                except:
                    error = "アップデート処理でエラーが発生しました"
    except:
        group = None

    context = {
        "group": group,
        "permission": permission_all,
        "administrator": administrator,
        "error": error
    }
    return render(request, "group/edit_permission.html", context)
