import requests
from datetime import datetime


class PochtaRuTracker:
    BASE_URL = "https://www.pochta.ru/api/tracking/api/v1/trackings/by-barcodes"

    @staticmethod
    def track(tracking_number):
        try:
            response = requests.get(
                f"{PochtaRuTracker.BASE_URL}",
                params={
                    'language': 'ru',
                    'track-numbers': tracking_number
                },
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                delivery_date = PochtaRuTracker._extract_delivery_date(data)
                return delivery_date
            return None

        except Exception:
            return None

    @staticmethod
    def _extract_delivery_date(data):
        try:
            if not data.get('detailedTrackings'):
                return None

            tracking_data = data['detailedTrackings'][0]

            # Ищем статус "Вручено" (GIVING)
            if 'trackingItemOperationGroupStatuses' in tracking_data:
                for status_group in tracking_data['trackingItemOperationGroupStatuses']:
                    if status_group.get('code') == 'GIVING' and status_group.get('date'):
                        delivery_date_str = status_group['date']
                        return PochtaRuTracker._parse_date(delivery_date_str)

            # Альтернативный способ - через историю операций
            if 'trackingHistoryItemList' in tracking_data.get('trackingItem', {}):
                history = tracking_data['trackingItem']['trackingHistoryItemList']
                for operation in history:
                    if (operation.get('humanStatus') == 'Вручение адресату' or
                            operation.get('operationType') == 2):
                        delivery_date_str = operation['date']
                        return PochtaRuTracker._parse_date(delivery_date_str)

            return None

        except (KeyError, IndexError, TypeError):
            return None

    @staticmethod
    def _parse_date(date_string):
        try:
            if date_string:
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                return dt.date()
        except (ValueError, AttributeError):
            return None
        return None


class CdekTracker:
    @staticmethod
    def track(tracking_number):
        # Заглушка для СДЭК
        return None


def check_delivery_status(tracking_number):
    if not tracking_number:
        return None

    if tracking_number.startswith(('1560', '1960')):
        return PochtaRuTracker.track(tracking_number)
    elif tracking_number.startswith(('10', '11')):
        return CdekTracker.track(tracking_number)
    return None