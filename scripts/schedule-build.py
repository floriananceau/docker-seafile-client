# !/usr/bin/env python

import os
import argparse
import sys
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from gitlab import Gitlab


class Scheduler:

    WATTTIME_SIGNAL_TYPE="co2_moer"

    def __init__(self, watttime_username, watttime_password, gitlab_private_token,
                 gitlab_project_id, gitlab_scheduled_pipeline_id):
        # Instanciate the WattTime session.
        url = "https://api.watttime.org/login"
        response = requests.get(url, auth=HTTPBasicAuth(watttime_username, watttime_password))
        payload = response.json()
        token = payload["token"]
        headers = {"Authorization": f"Bearer {token}"}
        self.watttime = requests.session()
        self.watttime.headers = headers

        # Instanciate the Gitlab session and grab the Weekly build scheduled pipeline.
        self.gitlab = Gitlab(private_token=gitlab_private_token)
        project = self.gitlab.projects.get(gitlab_project_id)
        self.pipeline = project.pipelineschedules.get(gitlab_scheduled_pipeline_id)

    def geolocate(self):
        url = "https://ipinfo.io"
        response = requests.get(url)
        payload = response.json()
        geolocation = payload["loc"]
        self.latitude, self.longitude = geolocation.split(",")

    def load_shift(self):

        # Get region from geolocation.
        # TODO: uncomment once premium plan
        # url = "https://api.watttime.org/v3/region-from-loc"
        # params = {
        #     "latitude": self.latitude,
        #     "longitude": self.longitude,
        #     "signal_type": self.WATTTIME_SIGNAL_TYPE}
        # response = self.watttime.get(url, params=params)
        # payload = response.json()
        # region = payload["region"]

        # Get the forecast for said region.
        # TODO: don't override the region, get a premium plan
        url = "https://api.watttime.org/v3/forecast"
        region = "CAISO_NORTH"  # Override the region until I get a premium plan
        params = {"region": region, "signal_type": self.WATTTIME_SIGNAL_TYPE}
        response = self.watttime.get(url, params=params)
        payload = response.json()
        data = payload["data"]

        # Look for the lowest value and it's datetime. Store the current value to know improvements.
        lowest_value: float = None
        for obj in data:
            value = obj["value"]
            point_time = datetime.fromisoformat(obj["point_time"])

            if not lowest_value:
                self.now_value = self.lowest_value = value
                self.now = self.then = point_time
                continue

            if value < lowest_value:
                lowest_value = value
                self.then = point_time

    def metrics(self):
        # Write WattTime metrics.
        metrics = {}
        metrics["watttime_now"] = self.now_value
        metrics["watttime_lowest"] = self.lowest_value
        metrics["now"] = self.now
        metrics["self.then"] = self.then
        with open("metrics.txt", "wt") as fileobject:
            for metric, value in metrics.items():
                fileobject.write(f"{metric} {value}\n")
        # TODO: track the metrics of energy cost/gain

    def schedule(self):
        # Test ownership prior to overtaking ownership.
        self.gitlab.auth()
        if self.pipeline.owner["id"] != self.gitlab.user.id:
            self.pipeline.take_ownership()

        # Set pipeline cron schedule to WattTime's Load Shift best moment.
        cron = f"{self.then.minute} {self.then.hour} {self.then.day} {self.then.month} *"
        self.pipeline.cron = cron
        self.pipeline.active = True
        self.pipeline.save()

    def unschedule(self):
        self.pipeline.active = False
        self.pipeline.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="",
        description="",
        epilog=""
    )
    parser.add_argument("--disable", action="store_true")
    args = parser.parse_args()
    disable = args.disable

    scheduler = Scheduler(
        watttime_username=os.environ["WATTTIME_USERNAME"],
        watttime_password=os.environ["WATTTIME_PASSWORD"],
        gitlab_project_id=os.environ["CI_PROJECT_ID"],
        gitlab_private_token=os.environ["WEEKLY_BUILD_PRIVATE_TOKEN"],
        gitlab_scheduled_pipeline_id=os.environ["WEEKLY_BUILD_PIPELINE_ID"]
    )

    if disable:
        scheduler.unschedule()
        sys.exit()

    scheduler.geolocate()
    scheduler.load_shift()
    scheduler.metrics()
    scheduler.schedule()