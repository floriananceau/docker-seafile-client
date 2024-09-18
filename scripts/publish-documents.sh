# Get a token from hub.docker.com with the owner credentials.
token=$(curl -s \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"username": "'"$DOCKER_REGISTRY_USERNAME"'", "password": "'"$DOCKER_REGISTRY_TOKEN"'"}' \
        https://hub.docker.com/v2/users/login/ | jq -r .token)

# Generate a JSON with the README.md as the full_description.
json=$(jq -n \
    --arg readme "$(<documentations/docker.md)" \
    '{"full_description": $readme,"description": "'"$DOCKER_REGISTRY_DESCRIPTION_FLRNNC"'"}')

jsonOld=$(jq -n \
    --arg readme "$(<documentations/docker-old.md)" \
    '{"full_description": $readme,"description": "'"$DOCKER_REGISTRY_DESCRIPTION_FLOWGUNSO"'"}')

# Update the Docker Hub repository's full_description.
curl -siL \
    -X PATCH \
    -d "$jsonOld" \
    -H "Content-Type: application/json" \
    -H "Authorization: JWT $token" \
    "https://hub.docker.com/v2/repositories/$DOCKER_REGISTRY_IMAGE_FLOWGUNSO/"

curl -siL \
    -X PATCH \
    -d "$json" \
    -H "Content-Type: application/json" \
    -H "Authorization: JWT $token" \
    "https://hub.docker.com/v2/repositories/$DOCKER_REGISTRY_IMAGE_FLRNNC/"