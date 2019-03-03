"""
Push notification service

send_message_android and send_message_ios are pretty similar, but this is intentional, in order
to support any future different conditions for both platforms, different keys or any additional parameters.
Shit happens sometimes, ROFL!
"""

from django.conf import settings
import requests


def send_message_android(destination, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "data": {
            "title": settings.TITLE_PUSH_NOTIFICATIONS,
            "detail": message
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print(request.text)


def send_message_ios(destination, message):
    headers = {
        'Authorization': 'key=' + settings.FIREBASE_SERVER_KEY,
        'Content - Type': 'application/json'
    }
    payload = {
        "to": destination,
        "priority": "high",
        "badge": 0,
        "notification": {
            "title": settings.TITLE_PUSH_NOTIFICATIONS,
            "text": message,
            "sound": "default",
        }
    }
    request = requests.post(
        settings.FIREBASE_API_URL,
        json=payload,
        headers=headers
    )
    print(request.text)


def send_push_notification_to_devices_list(devices, message):
    try:
        for device in devices:
            if device.type == 'android':
                send_message_android(device.device_code, message)
            if device.type == 'ios':
                send_message_ios(device.device_code, message)
        return True
    except Exception as e:
        print(e)
        return False


def send_push_notification_to_one_device(device_code, device_os, message):
    try:
        if device_os == 'android':
            send_message_android(device_code, message)
        elif device_os == 'ios':
            send_message_ios(device_code, message)
        return True
    except Exception as e:
        print(e)
        return False
