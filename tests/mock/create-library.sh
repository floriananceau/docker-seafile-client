#!/usr/bin/env bash

until curl --output /dev/null --silent --head --fail http://seafile-${TARGET}; do
    printf '.'
    sleep 5
done