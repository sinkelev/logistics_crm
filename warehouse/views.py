from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
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
        delivery_date, debug_info = check_delivery_status(tracking_number)

        if debug_info:
            return JsonResponse({
                'success': False,
                'error': debug_info
            })

        if delivery_date:
            return JsonResponse({
                'success': True,
                'status': 'delivered',
                'delivery_date': delivery_date.strftime('%Y-%m-%d'),
                'message': f'Доставлено {delivery_date.strftime("%d.%m.%Y")}'
            })
        else:
            return JsonResponse({
                'success': True,
                'status': 'not_delivered',
                'delivery_date': None,
                'message': 'Доставка не найдена или отправление еще в пути'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Внутренняя ошибка сервера: {str(e)}'
        }, status=500)