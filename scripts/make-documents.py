# !/usr/bin/env python

from pathlib import Path
import argparse
import os

from jinja2 import Environment, FileSystemLoader
from gitlab import Gitlab


REPOSITORY_PATH = Path(__file__).parent.parent

class DocumentMaker:

    def __init__(self, filename: str) -> None:
        # Intanciate the Jinja2 renderer.
        self.directory = REPOSITORY_PATH.joinpath("documentations")
        loader = FileSystemLoader(self.directory)
        environment = Environment(loader=loader)
        self.filename = filename
        self.template = environment.get_template(filename)

        # Instanciate the Gitlab session.
        gitlab_project_id=os.environ["CI_PROJECT_ID"]
        gitlab_private_token=os.environ["WEEKLY_BUILD_PRIVATE_TOKEN"]
        self.gitlab = Gitlab(private_token=gitlab_private_token)
        self.project = self.gitlab.projects.get(gitlab_project_id)

        self.versions = []
        self.badges = {}

    def get_versions(self):
        versions = []
        for path in Path("versions").iterdir():
            with open(path, "rt") as fo:
                versions.append(fo.read().strip())
        versions.sort(reverse=True)

        # Prepare the render context.
        latest = True
        self.versions = []
        for version in versions:
            version = version.strip()
            parts = version.split(".")
            
            increments = []
            blocks = []
            for part in parts:
                increments.append(part)
                section = ".".join(increments)
                blocks.append(f"`{section}`")
            
            if latest:
                blocks.append("`latest`")
                latest = False
            
            self.versions.append(blocks)


    def get_badges(self):
        badges = self.project.badges.list()

        for badge in badges:
            name = badge.name
            link = badge.rendered_link_url
            image = badge.rendered_image_url
            links = {"link": link, "image": image}
            self.badges[name] = links


    def render(self):
        # Render
        # TODO: read and adapt the CHANGELOG and insert into the render.
        content = self.template.render(versions=self.versions, badges=self.badges)
        #content = template.render()  # When version/ is unavailable.
        filename = Path(self.filename).with_suffix("")
        path = self.directory.joinpath(filename)

        # Write to file
        with open(path, mode="w") as fo:
            fo.write(content)

if __name__ == "__main__":

    # Argument parsing.
    parser = argparse.ArgumentParser(prog="Seafile Docker client documentation renderer")
    parser.add_argument("template", type=str)
    args = parser.parse_args()

    maker = DocumentMaker(args.template)
    maker.get_versions()
    maker.get_badges()
    maker.render()