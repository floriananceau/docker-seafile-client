> ⚠️ Please consider sponsoring this project to help me maintaining and improving it. As of right now, you can support me through Liberay, available in the project badges

> This project is switching namespaces. The sources previously in [flwgnso-docker/docker-seafile-client](https://gitlab.com/flwgns-docker/seafile-client) are now in [flrnnc-oss/docker-seafile-client](https://gitlab.com/flrnnc-oss/docker-seafile-client). The Docker image can still be found at [flowgunso/seafile-client](https://hub.docker.com/r/flowgunso/seafile-client) but it will be deprecated, the image [flrnnc/seafile-client](https://hub.docker.com/r/flrnnc/seafile-client) should be used instead.

# Quick informations

_Docker Seafile client_ is a Docker image that provides a Seafile client to sync one or more library as volumes to other containers.

## Features
* Synchronize one or more Seafile libraries.
* Support password protected librairies.
* Support two factor authentication.
* Configure upload and download limits.
* Skip SSL certificates.
* Set file ownership with user/group ID

## Quick links

* Check out the [roadmap](https://gitlab.com/flrnnc-oss/docker-seafile-client/-/wikis/home#roadmap) to see what is anticipated.
* Check out how to [contribute](CONTRIBUTING.md).
* Report issues on [Gitlab](https://gitlab.com/flrnnc-oss/docker-seafile-client/).
* Ask questions on [Seafile forum](https://forum.seafile.com/t/docker-client-to-sync-files-with-containers/8573).


# Usage

## Start a Seafile client

### Docker command-line
The following command start the Seafile client with one library:
```bash
docker run \ 
    -e SEAF_SERVER_URL="https://seafile.example/" \
    -e SEAF_USERNAME="a_seafile_user" \
    -e SEAF_PASSWORD="SoMePaSSWoRD" \
    -e SEAF_LIBRARY="an-hexadecimal-library-uuid" \
    -v path/to/library:/library \
    -v path/to/client/data:/seafile \
    flrnnc/seafile-client:latest
```

### Docker Compose
The following Docker Compose start a Seafile client with two libraries, with one password protected:
```yaml
version: "3"

services:

  seafile-client:
    image: flrnnc/seafile-client:latest
    volumes:
      - audio:/library/audio
      - documents:/library/documents
      - client:/seafile
    environment:
      SEAF_SERVER_URL: "https://seafile.example/"
      SEAF_USERNAME: "a_seafile_user"
      SEAF_PASSWORD: "SoMePaSSWoRD"
      SEAF_LIBRARY_AUDIO: "audio-library-uuid"
      SEAF_LIBRARY_AUDIO_PASSWORD: "auDioLiBRaRyPaSSWoRD"
      SEAF_LIBRARY_DOCUMENTS: "documents-library-uuid"

volumes:
  audio:
  documents:
  client:
```

## Librairies
Environment variables allows librairies configuration, as shown in the examples above.

You can configure either a single librairy or multiple librairies.

### Single library
To synchronize a single library, use the environment variables `SEAF_LIBRARY` and `SEAF_LIBRARY_PASSWORD`. The library will be synchronized in _/library_.

### Multiple librairies
To synchronise multiple librairies, use the same environment variable as above but suffixed with a single identifier word. That word will be used for the library password and it's synchronization path as well.

Hence, to synchronise a library identified as **audio**, the environment variables would be `SEAF_LIBRARY_AUDIO` for the library UUID and `SEAF_LIBRARY_AUDIO_PASSWORD` for the library password. The library will be then synchronized in _/library/audio_.

Identifiers allows to add as many libraries as possible. Identifier are single word only.

## Environment variables
Environment variable allows you to configure the Seafile client.

### `SEAF_SERVER_URL`
> This variable is mandatory.

The Seafile server URL.

### `SEAF_USERNAME`
> This variable is mandatory.

The username for the Seafile account.

### `SEAF_PASSWORD`
> This variable is mandatory.

The password for the Seafile account.

### `SEAF_LIBRARY`, `SEAF_LIBRARY_[IDENTIFIER]`
> This variable is mandatory.

The UUID of the library, libraries to synchronize.
Replace `[IDENTIFIER]` with the a unique single word identifier for each library you want to synchronize.

### `SEAF_LIBRARY_PASSWORD`, `SEAF_LIBRARY_[IDENTIFIER]_PASSWORD`
The password of the library, libraries to synchronize.
Replace `[IDENTIFIER]` with the a unique single word identifier for each library you want to synchronize corresponding to the `SEAF_LIBRARY_[IDENTIFIER]`.

### `SEAF_2FA_SECRET`
_Two factor authentication is supported but your secret key must be provided._ That key can be found on your Seafile web interface, only at the 2FA setup, when the QR code is shown. The secret key is embedded in the QR or available as a cookie.

### `SEAF_UPLOAD_LIMIT`, `SEAF_DOWNLOAD_LIMIT`
Set upload and download speeds limits. Limits are in bytes.

### `SEAF_SKIP_SSL_CERT`  
Skip SSL certificates verifications.

> Any string is considered true, omit the variable to set to false. Enable this if you have synchronization failures regarding SSL certificates.

### `UID`, `GID`  
Override the _UID_ and _GID_ for user running the Seafile client, hence the volume ownership.

## Docker Secrets
All environments variable supports Docker Secrets, as environment variable variant suffixed with `_FILE` as files.

## Full example
```bash
version: "3"

services:

  seafile-client:
    image: flrnnc/seafile-client:latest
    volumes:
      - audio:/library/audio
      - documents:/library/documents
      - client:/seafile
    environment:
      SEAF_SERVER_URL: "https://seafile.example/"
      SEAF_USERNAME: "a_seafile_user"
      SEAF_PASSWORD: "SoMePaSSWoRD"
      SEAF_LIBRARY_AUDIO: "audio-library-uuid"
      SEAF_LIBRARY_AUDIO_PASSWORD: "auDioLiBRaRyPaSSWoRD"
      SEAF_LIBRARY_DOCUMENTS: "documents-library-uuid"
      SEAF_2FA_SECRET: "JBSWY3DPEHPK3PXPIXDAUMXEDOXIUCDXWC32CS"
      SEAF_UPLOAD_LIMIT: "1000000"
      SEAF_DOWNLOAD_LIMIT: "1000000"
      SEAF_SKIP_SSL_CERT: "true"
      UID: "1000"
      GID: "1000"

volumes:
  audio:
  documents:
  client:
```
