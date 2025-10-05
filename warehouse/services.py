import requests
from datetime import datetime


HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.cdek.ru/ru/tracking',
            'Origin': 'https://www.cdek.ru',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Dnt': '1',
            'X-Requested-With': 'XMLHttpRequest',
            }

def _parse_iso_date(date_string):
    if not date_string: return None
    try:
        return datetime.fromisoformat(date_string.replace('Z', '+00:00')).date()
    except (ValueError, TypeError):
        return None


class PochtaRuTracker:
    BASE_URL = "https://www.pochta.ru/api/tracking/api/v1/trackings/by-barcodes"

    @staticmethod
    def track(tracking_number):
        try:
            response = requests.get(
                PochtaRuTracker.BASE_URL,
                params={'language': 'ru', 'track-numbers': tracking_number},
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if not data.get('detailedTrackings'):
                return None, f"Почта: 'detailedTrackings' не найден. Ответ: {response.text}"

            tracking_details = data['detailedTrackings'][0]
            operation_groups = tracking_details.get('trackingItem', {}).get('trackingItemOperationGroupStatuses', [])

            for group in operation_groups:
                if group.get('code') == 'GIVING':
                    return _parse_iso_date(group.get('date')), None

            return None, None
        except requests.exceptions.RequestException as e:
            err_text = str(e.response.text) if e.response else str(e)
            return None, f"Почта: Ошибка сети: {err_text}"
        except Exception as e:
            return None, f"Почта: Ошибка парсинга: {str(e)}"


class CdekTracker:
    BASE_URL = "https://www.cdek.ru/api-site/track/info/"

    @staticmethod
    def track(tracking_number):
        try:
            url = f"{CdekTracker.BASE_URL}?track={tracking_number}&locale=ru"
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('success') and 'data' in data and data['data']:
                status_info = data['data'].get('status')
                if status_info and status_info.get('code') == 'DELIVERED':
                    delivery_date_str = status_info.get('date')
                    if delivery_date_str:
                        return datetime.strptime(delivery_date_str, '%Y-%m-%d').date(), None

            return None, None
        except requests.exceptions.RequestException as e:
            err_text = str(e.response.text) if e.response else str(e)
            return None, f"СДЭК: Ошибка сети/доступа. Ответ: {err_text}"
        except Exception as e:
            return None, f"СДЭК: Ошибка обработки ответа: {str(e)}"


def check_delivery_status(tracking_number):
    if not tracking_number or not tracking_number.isdigit():
        return None, "Неверный формат номера"

    if len(tracking_number) == 14:
        return PochtaRuTracker.track(tracking_number)
    elif len(tracking_number) == 11:
        return CdekTracker.track(tracking_number)

    return None, "Неизвестный формат трек-номера"