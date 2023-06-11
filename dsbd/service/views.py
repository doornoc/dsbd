from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render

from custom_auth.models import User
from dsbd.service.models import Service


@login_required
def index(request):
    services = None
    error = None
    group_filter = request.user.groups.filter(customgroup__is_active=True)
    if group_filter.exists():
        service_objects = Service.objects.get_service(groups=group_filter.all())
    else:
        error = "Groupに所属していません"

    if not error:
        paginator = Paginator(service_objects, int(request.GET.get("per_page", "5")))
        page = int(request.GET.get("page", "1"))
        try:
            services = paginator.page(page)
        except (EmptyPage, InvalidPage):
            services = paginator.page(paginator.num_pages)
    context = {
        "services": services,
        "error": error
    }
    return render(request, "service/index.html", context)
