#!/bin/bash

# Docker Seafile client, help you mount a Seafile library as a volume.
# Copyright (C) 2019-2024, florian.anceau@gmail.com
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

# Prepare the build arguments
build_args=(CREATED=$(date -u +"%Y-%m-%dT%H:%M:%SZ"))
[[ "$CI_COMMIT_SHA" ]] && build_args+=(REVISION=$CI_COMMIT_SHA)
[[ "$CI_COMMIT_TAG" ]] && build_args+=(VERSION=$CI_COMMIT_TAG)
[[ "$TARGET" ]] && build_args+=(TARGET=$TARGET)

# Build the build argumets string.
build_arguments=""
for build_arg in "${build_args[@]}"; do
    build_arguments+="--build-arg $build_arg "
done

docker build \
    $build_arguments \
    --build-arg IMAGE=flowgunso \
    --tag seafile-client:$TARGET-flowgunso \
    seafile-client/

docker build \
    $build_arguments \
    --build-arg IMAGE=flrnnc \
    --tag seafile-client:$TARGET-flrnnc \
    seafile-client/
