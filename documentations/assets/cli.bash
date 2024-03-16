docker run \ 
    -e SEAF_SERVER_URL="https://seafile.example/" \
    -e SEAF_USERNAME="a_seafile_user" \
    -e SEAF_PASSWORD="SoMePaSSWoRD" \
    -e SEAF_LIBRARY="an-hexadecimal-library-uuid" \
    -v path/to/library:/library \
    -v path/to/client/data:/seafile \
    flowgunso/seafile-client:latest
