# Get a token from hub.docker.com with the owner credentials.
token=$(curl -s \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"username": "'"$DOCKER_HUB_OWNER_USERNAME"'", "password": "'"$DOCKER_HUB_OWNER_TOKEN"'"}' \
        https://hub.docker.com/v2/users/login/ | jq -r .token)

# Generate a JSON with the README.md as the full_description.
json=$(jq -n \
    --arg readme "$(<documentations/docker.md)" \
    '{"full_description": $readme,"description":"Synchronize a Seafile library. Support password protected librairies and 2FA authentication."}')

# Update the Docker Hub repository's full_description.
curl -siL \
    -X PATCH \
    -d "$json" \
    -H "Content-Type: application/json" \
    -H "Authorization: JWT $token" \
    "https://hub.docker.com/v2/repositories/$DOCKER_HUB_IMAGE/"
