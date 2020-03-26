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
    status = requests.get(api_url).json()['status']['indicator']
    if status == "none":
        return OutageStatus.NO_OUTAGE
    elif status == "minor":
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
    elif status == 2:
        return OutageStatus.PARTIAL_OUTAGE
    else:  # TODO: Verify that full outage status code is not 2
        return OutageStatus.FULL_OUTAGE


def discord_status_checker():
    return statuspage_io_interface('srhpyqt94yxb')


def instagram_status_checker():
    return downdetector_interface('instagram')


def snapchat_status_checker():
    return downdetector_interface('snapchat')


def github_status_checker():
    return statuspage_io_interface('kctbh9vrtdwd')


def netflix_status_checker():
    status_url = "https://help.netflix.com/en/is-netflix-down"
    response = requests.get(status_url)
    result = BeautifulSoup(response.text, "html.parser").findAll("div", {"class": "down-notification-content"})
    if len(result) != 1:
        return downdetector_interface('netflix')
    if "Netflix is up!" in result[0].text:
        return OutageStatus.NO_OUTAGE
    else:
        return OutageStatus.FULL_OUTAGE


def twitter_status_checker():
    return statuspage_io_interface('zjttvm6ql9lp')


def zoom_status_checker():
    return statuspage_io_interface('14qjgk812kgk')


def google_status_checker():
    return downdetector_interface('google')
