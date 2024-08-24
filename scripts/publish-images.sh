# !/bin/bash

# Docker Seafile client, help you mount a Seafile library as a volume.
# Copyright (C) 2019-2020, flow.gunso@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


set -ex

raise() {
    echo $1
    exit 1
}

# Validate the required parameters.
# [[ -z "$DOCKER_HUB_BOT_USERNAME" ]] && raise "Missing DOCKER_HUB_BOT_USERNAME envvar."
# [[ -z "$DOCKER_HUB_BOT_TOKEN" ]] && raise "Missing DOCKER_HUB_BOT_TOKEN envvar."
# [[ -z "$DOCKER_HUB_OWNER_USERNAME" ]] && raise "Missing DOCKER_HUB_OWNER_USERNAME envvar."
# [[ -z "$DOCKER_HUB_OWNER_TOKEN" ]] && raise "Missing DOCKER_HUB_OWNER_TOKEN envvar."
# [[ -z "$DOCKER_HUB_IMAGE" ]] && raise "Missing DOCKER_HUB_IMAGE envvar"

# Grab version with the container
version="$(docker run --rm seafile-client:$TARGET cat -s /SEAFILE_VERSION)"
version="$(echo ${version%-*})"

# Output the version to an artifact for documentation rendering.
mkdir -p versions/
echo $version >> "versions/$TARGET"

# Generate version tags.
tags=()
[[ "$TARGET" =~ "unstable" ]] && tags+=("latest")
for version_component in $(echo $version | tr '.' '\n'); do
    tag+="$version_component"
    tags+=("$tag")
    tag+="."
done

# Tag then push to the Docker Hub registry.
echo $DOCKER_REGISTRY_TOKEN | docker login --password-stdin --username $DOCKER_REGISTRY_USERNAME
for tag in "${tags[@]}"; do
    docker tag seafile-client:$TARGET $DOCKER_REGISTRY_IMAGE_FLOWGUNSO:$tag
    docker push $DOCKER_REGISTRY_IMAGE_FLOWGUNSO:$tag
done

for tag in "${tags[@]}"; do
    docker tag seafile-client:$TARGET-flrnnc $DOCKER_REGISTRY_IMAGE_FLRNNC:$tag
    docker push $DOCKER_REGISTRY_IMAGE_FLRNNC:$tag
done