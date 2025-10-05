from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .services import check_delivery_status


@require_GET
@csrf_exempt
def check_delivery_api(request):
    tracking_number = request.GET.get('tracking_number')
    if not tracking_number:
        return JsonResponse({
            'success': False,
            'error': 'Не указан номер для отслеживания'
        }, status=400)

    try:
        delivery_date = check_delivery_status(tracking_number)

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
            'error': f'Ошибка сервера'
        }, status=500)