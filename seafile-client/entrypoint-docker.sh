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

#!/bin/bash

set -e

groupmod -g $GID seafile &> /dev/null
usermod -u $UID -g $GID seafile &> /dev/null


if [ "$IMAGE" == "flowgunso" ]; then
    echo
    echo -e "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    echo -e "┃  \e[1mPlease use \e[4mflrnnc/seafile-client\e[24m instead of \e[4mflowgunso/seafile-client\e[24m which will be deprecated...\e[0m      ┃"
    echo -e "┃  See the information notices at:                                                                       ┃"
    echo -e "┃  \thttps://forum.seafile.com/t/docker-client-to-sync-files-with-containers/8573                     ┃"
    echo -e "┃  \thttps://gitlab.com/flrnnc-oss/docker-seafile-client                                              ┃"
    echo -e "┃  \thttps://hub.docker.com/r/flowgunso/seafile-client                                                ┃"
    echo -e "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    echo
fi

sudo \
    -HE \
    -u seafile \
    -- "$@"