# !/usr/bin/env python

import os
from datetime import datetime

from gitlab import Gitlab


class BuildBadgeUpdater:

    def __init__(self, gitlab_private_token, gitlab_project_id, gitlab_build_badge_id):

        # Instanciate the Gitlab session and grab the Weekly build scheduled pipeline.
        self.gitlab = Gitlab(private_token=gitlab_private_token)
        project = self.gitlab.projects.get(gitlab_project_id)
        self.badge = project.badges.get(gitlab_build_badge_id)

    def update(self):
        now = datetime.now()
        date = now.strftime(r"%Y--%m--%d")
        image_url = f"https://img.shields.io/badge/_-{date}-_?label=last%20build&color=light-green"
        self.badge.image_url = image_url
        self.badge.save()


if __name__ == "__main__":

    build_badge_updater = BuildBadgeUpdater(
        gitlab_project_id=os.environ["CI_PROJECT_ID"],
        gitlab_private_token=os.environ["WEEKLY_BUILD_PRIVATE_TOKEN"],
        gitlab_build_badge_id=os.environ["BUILD_BADGE_ID"]
    )

    build_badge_updater.update()