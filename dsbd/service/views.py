from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render

from custom_auth.models import User
from dsbd.service.models import Service


@login_required
def index(request):
    services = None
    try:
        service_objects = Service.objects.get_service(
            groups=request.user.groups.filter(customgroup__is_active=True).all())

    except ValueError as e:
        error = "サービスが存在しません"

    if not service_objects:
        paginator = Paginator(service_objects, int(request.GET.get("per_page", "5")))
        page = int(request.GET.get("page", "1"))
        try:
            services = paginator.page(page)
        except (EmptyPage, InvalidPage):
            services = paginator.page(paginator.num_pages)
    context = {
        "services": services,
    }
    return render(request, "service/index.html", context)
