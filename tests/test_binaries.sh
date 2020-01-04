#!/bin/bash

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

failures=()
binaries=(seaf-cli cron oathtool)

for binary in "${binaries[@]}"; do
    if ! [ -x "$(command -v $binary)" ]; then
        echo "$binary was not found"
        failures+=($binary)
    fi
done

if [ ${#failures[@]} -ne 0 ]; then
    exit 1
fi
