import requests
from bs4 import BeautifulSoup
from enum import Enum


class OutageStatus(Enum):
    NO_OUTAGE = 0
    PARTIAL_OUTAGE = 1
    FULL_OUTAGE = 2


# Common function to be used for services that use statuspage.io to report outages
# Current services include Reddit and Discord
def statuspage_io_interface(service_id):
    api_url = 'https://' + service_id + '.statuspage.io/api/v2/status.json'
    status = requests.get(api_url).json()['status']['description']
    if status == "All Systems Operational":
        return OutageStatus.NO_OUTAGE
    elif status == "Partial System Outage":
        return OutageStatus.PARTIAL_OUTAGE
    else:
        return OutageStatus.FULL_OUTAGE


# Common function to be used for services that do not provide their own status checker API
def downdetector_interface(service_name):
    downdetector_url = "https://downdetector.com/status/" + service_name
    response = requests.get(downdetector_url)
    result = BeautifulSoup(response.text, "html.parser").findAll("div", {"class": "entry-title"})
    if len(result) != 1:
        raise LookupError(
            "An error has occurred. This may be due to changes to the structure of the Downdetector website.")
    if "No problems" in result[0].text:
        return OutageStatus.NO_OUTAGE
    elif "Possible problems" in result[0].text:
        return OutageStatus.PARTIAL_OUTAGE
    elif "Problems" in result[0].text:
        return OutageStatus.FULL_OUTAGE
    else:
        raise LookupError(
            "An error has occurred. This may be due to changes to the structure of the Downdetector website."
        )


def reddit_status_checker():
    return statuspage_io_interface('2kbc0d48tv3j')


def facebook_status_checker():
    api_url = "https://www.facebook.com/platform/api-status/"
    status = requests.get(api_url).json()['current']['health']
    if status == 1:
        return OutageStatus.NO_OUTAGE
    else:  # TODO: Account for partial outage
        return OutageStatus.FULL_OUTAGE


def discord_status_checker():
    return statuspage_io_interface('srhpyqt94yxb')


def instagram_status_checker():
    return downdetector_interface('instagram')


def snapchat_status_checker():
    return downdetector_interface('snapchat')
