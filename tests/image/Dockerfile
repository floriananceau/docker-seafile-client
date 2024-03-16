ARG TARGET=unstable
FROM seafile-client:${TARGET}

COPY --chmod=755 test_binaries.sh /test.sh

CMD ["/test.sh"]
