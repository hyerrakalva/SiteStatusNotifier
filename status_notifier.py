import argparse
import json
import time
from checker_functions import *
from notification import send_notification


def status_notifier(cli_args):
    try:
        with open("data/service_mappings.json") as f:
            service_mappings: dict = json.load(f)
        try:
            service = service_mappings['synonyms'][cli_args.service_name[0].lower()]
        except KeyError:
            send_notification("Site Status Notifier", 'Sorry, but the service "' + cli_args.service_name[0]
                              + '" is not supported at the moment.')
            print('Sorry, but the service "' + cli_args.service_name[0] + '" is not supported at the moment.')
            return -2
        func = eval(service_mappings['functions'][service])

        time.sleep(cli_args.delay * 60)
        status = func()  # 0 indicates no outage, 1 indicates partial outage, and 2 indicates full outage.
        if status == OutageStatus.NO_OUTAGE:
            send_notification(service + " Status Notifier", service + " seems to be online already!")
            print(service + " seems to be online already. If " + service +
                  " has just gone down, please try rerunning with a specified --delay argument.")
            return -1

        print(service + " - " + ("partial outage" if status == OutageStatus.PARTIAL_OUTAGE else "major outage"))
        print("Waiting for " + service + " to get fully back online...")

        running_time = cli_args.timeout * 3600
        while status != OutageStatus.NO_OUTAGE:
            if running_time <= 0:
                send_notification(service + " Status Notifier", service + " Status Notifier will now exit as "
                                  + service + " was unable to come back online within " + str(cli_args.timeout)
                                  + " hour." if cli_args.timeout == 1 else " hours.")
                return -3
            time.sleep(60)
            running_time -= 60
            try:
                new_status = func()
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                try:
                    new_status = func()
                except requests.exceptions.ConnectionError:
                    time.sleep(2)
                    new_status = func()
            if status == OutageStatus.FULL_OUTAGE and new_status == OutageStatus.PARTIAL_OUTAGE:
                send_notification(service + " Status Notifier", service + "'s status seems to have improved, but there "
                                  "may still be some issues.")
            status = new_status

        send_notification(service + " Status Notifier", "Looks like " + service + " is back online!")
        time.sleep(5)
        return 0
    except requests.exceptions.ConnectionError:
        send_notification(service + " Status Notifier", "Oops, " + service + " Status Notifier was unable to connect to"
                          " the Internet. Please check your Internet connection and try again.")
        raise
    except:
        send_notification("Site Status Notifier",
                          "Oops, something went wrong. Please check the command line for more info.")
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Notifies when a website or service is back online.")
    parser.add_argument('service_name', metavar='site', type=str, nargs=1,
                        help='name of the website or service to track')  # TODO: add choices parameter
    parser.add_argument('--delay', '-d', metavar='min', type=float, default=0,
                        help="number of minutes to delay for before beginning to check status, useful when a site's"
                             " outage has not yet been reflected by outage detectors")
    parser.add_argument('--timeout', '-t', metavar='hrs', type=float, default=float('inf'), help="number of hours to"
                        " track site's status for before exiting")
    # TODO: add argument that allows user to change refresh rate
    args = parser.parse_args()
    exit_code = status_notifier(args)
    exit(exit_code)
