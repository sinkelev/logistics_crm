from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PostalRecord, Order
from .forms import PostalRecordForm
from .services import check_delivery_status


@require_GET
@login_required
def check_delivery_api(request):
    tracking_number = request.GET.get('tracking_number')
    if not tracking_number:
        return JsonResponse({
            'success': False,
            'error': 'Не указан номер для отслеживания'
        }, status=400)

    try:
        delivery_date, shipping_date, debug_info = check_delivery_status(tracking_number)

        if debug_info:
            return JsonResponse({
                'success': False,
                'error': debug_info
            })

        response_data = {
            'success': True,
            'delivery_date': delivery_date.strftime('%Y-%m-%d') if delivery_date else None,
            'shipping_date': shipping_date.strftime('%Y-%m-%d') if shipping_date else None,
        }

        messages = []
        if delivery_date:
            messages.append(f'Доставлено {delivery_date.strftime("%d.%m.%Y")}')
        if shipping_date:
            messages.append(f'Отправлено {shipping_date.strftime("%d.%m.%Y")}')

        if not messages:
            messages.append('Информация о доставке/отправке не найдена')

        response_data['message'] = '. '.join(messages)

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }, status=500)


class PostalRecordListView(LoginRequiredMixin, ListView):
    template_name = "frontend/postal_list.html"
    context_object_name = "orders"
    paginate_by = 20

    def get_queryset(self):
        return Order.objects.all().prefetch_related("postal_records").order_by("-date_order")

class PostalRecordCreateView(LoginRequiredMixin, CreateView):
    model = PostalRecord
    form_class = PostalRecordForm
    template_name = "frontend/postal_form.html"
    success_url = reverse_lazy("warehouse:postal_list")

    def get_initial(self):
        initial = super().get_initial()
        order_id = self.request.GET.get("order")
        if order_id:
            initial["order"] = order_id
        return initial

class PostalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = PostalRecord
    form_class = PostalRecordForm
    template_name = "frontend/postal_form.html"

    def get_success_url(self):
        return reverse_lazy("warehouse:postal_list")

class PostalRecordDetailView(LoginRequiredMixin, DetailView):
    model = PostalRecord
    template_name = "frontend/postal_detail.html"
    context_object_name = "postal"
