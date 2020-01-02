import sys
if sys.platform == 'win32':
    from win10toast_persist import ToastNotifier
else:
    raise NotImplementedError("The Site Status Notifier only works on Windows at the moment. Support for Linux and "
                              "macOS will arrive in the near future!")


def send_notification(title, message):
    if sys.platform == 'win32':
        notify = ToastNotifier()
        notify.show_toast(title, message, icon_path='data/app_icon.ico', duration=None)
