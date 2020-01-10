# Site Status Notifier

A tool powered by Python that notifies you when a website or service is back online after an outage.

## Requirements
- Python 3.7.x
- An internet connection!
- Operating Systems:
    - Windows 10
    - Linux with the `libnotify` package installed (known as `libnotify-bin` in certain distros)

## Using the Site Status Notifier

### Setting Up the Tool

To start off, clone this repository onto your computer using the following commands:

```bash
git clone https://github.com/hyerrakalva/SiteStatusNotifier.git
cd SiteStatusNotifier
```

Next, create a new Python virtual environment in the cloned repository by running the following command:

```bash
python -m venv --system-site-packages venv
```

You can activate the virtual environment once you create it. On Windows, this can be achieved by the following command:

```bash
venv\Scripts\activate
```

On Linux, this can be achieved by the following command:

```bash
source venv/bin/activate
```

Finally, install all of the Python modules required to run this tool using this `pip` command:

```bash
pip install --ignore-installed -r requirements.txt
```

Now you are all set to run the Site Status Notifier on your computer!

### Using the Tool

First, make sure that you have activated the virtual environment that you have created earlier. Then, you can run the Site Status Notifier using a variant of the command below:

```bash
python status_notifier.py [--help] [--delay min] [--timeout hrs] site
```

The `site` argument is required and is where you specify the name of the [service](https://github.com/hyerrakalva/SiteStatusNotifier#supported-services) you want to track. This argument is case-insensitive, and you just have to specify the name of the service, not its website address. Some abbrevations may work (i.e. `fb` in place of `facebook`, `ig` in place of `instagram`), but if there is a common abbreviation for a supported service that doesn't seem to work, feel free to create an issue or even submit a pull request!

The `--delay` (or `-d`) argument allows you to set a delay in minutes before the Site Status Notifier starts checking if a service is back online. This is useful if a site has just gone down and you want to run the tool in the background before the site's outage has not yet been acknowledged online. This way, the tool will not exit right away and will instead give online status trackers a chance to acknowledge this outage before beginning to fetch status data. If this argument is not specified, there will be no delay.

The `--timeout` (or `-t`) argument allows you to set a certain number of hours after which the Site Status Notifier exits even if the selected service is not back online. If this argument is not specified, the tool will continue to track the service's status for an indefinite amount of time.

The `--help` (or `-h`) argument prints out information in the command line showing how to use this tool.

## Supported Services
- Discord
- Facebook
- GitHub
- Instagram
- Netflix
- Reddit
- Snapchat