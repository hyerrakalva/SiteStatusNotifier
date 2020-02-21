import sys
if sys.platform == 'win32':
    from win10toast_persist import ToastNotifier
elif sys.platform == 'linux':
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify, GdkPixbuf
else:
    raise NotImplementedError("The Site Status Notifier only works on Windows and Linux at the moment. Support for "
                              "macOS will arrive in the near future!")


def send_notification(title, message):
    if sys.platform == 'win32':
        notify = ToastNotifier()
        notify.show_toast(title, message, icon_path='data/app_icon.ico', duration=None)
    elif sys.platform == 'linux':
        Notify.init("Site Status Notifier")
        notify = Notify.Notification.new(summary=title, body=message, icon='data/app_icon.png')
        icon = GdkPixbuf.Pixbuf.new_from_file("data/app_icon.png")
        notify.set_image_from_pixbuf(icon)
        notify.set_timeout(10000)
        notify.show()
