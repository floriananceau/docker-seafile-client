# !/usr/bin/env python

from pathlib import Path
import argparse

from jinja2 import Environment, FileSystemLoader


REPOSITORY_PATH = Path(__file__).parent.parent

# Argument parsing.
parser = argparse.ArgumentParser(prog="Seafile Docker client documentation renderer")
parser.add_argument("template", type=str)
args = parser.parse_args()

# Setup Jinja2 templater
documentations_path = REPOSITORY_PATH.joinpath("documentations")
loader = FileSystemLoader(documentations_path)
environment = Environment(loader=loader)
template = environment.get_template(args.template)


buffer=[]
for path in Path("versions").iterdir():
    with open(path, "rt") as fo:
        buffer.append(fo.read().strip())
buffer.sort(reverse=True)

# Prepare the render context.
latest = True
versions = []
for line in buffer:
    version = line.strip()
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
    versions.append(blocks)

# Render
content = template.render(versions=versions)
#content = template.render()  # When version/ is unavailable.
filename = Path(args.template).with_suffix("")
document = documentations_path.joinpath(filename)

# Write to file
with open(document, mode="w") as fo:
    fo.write(content)
