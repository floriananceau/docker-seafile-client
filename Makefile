TARGET?=unstable

# Mocking
mock:
	docker compose -f tests/mock/compose.yaml up -d

unmock:
	docker compose -f tests/mock/compose.yaml down

client:
	docker compose -f tests/mock/compose.yaml rm -fs client
	docker compose -f tests/mock/compose.yaml up -d client

shell:
	docker compose -f tests/mock/compose.yaml exec client bash

logs:
	docker compose -f tests/mock/compose.yaml logs -f client

ps:
	docker compose -f tests/mock/compose.yaml ps

# Build
build:
	TARGET=${TARGET} CI_COMMIT_TAG=${CI_COMMIT_TAG} bash scripts/build-images.sh

build-test:
	docker build --build-arg TARGET=${TARGET} -t seafile-client:test tests/image

test:
	docker run seafile-client:test

# CI/CD
documents:
	python scripts/make-documents.py docker.md.j2
	python scripts/make-documents.py docker-old.md.j2
	python scripts/make-documents.py seafile.md.j2

publish-images:
	TARGET=${TARGET} \
	DOCKER_REGISTRY_USERNAME=${DOCKER_REGISTRY_USERNAME} \
	DOCKER_REGISTRY_TOKEN=${DOCKER_REGISTRY_TOKEN} \
	DOCKER_REGISTRY_IMAGE_FLOWGUNSO=${DOCKER_REGISTRY_IMAGE_FLOWGUNSO} \
	DOCKER_REGISTRY_IMAGE_FLRNNC=${DOCKER_REGISTRY_IMAGE_FLRNNC} \
		bash scripts/publish-images.sh

publish-documents:
	bash scripts/publish-documents.sh
	python scripts/update-build-badge.py

save:
	mkdir -p tarballs/
	docker save --output tarballs/${TARGET}-flowgunso.tar seafile-client:${TARGET}-flowgunso
	docker save --output tarballs/${TARGET}-flrnnc.tar seafile-client:${TARGET}-flrnnc

load:
	docker load --input tarballs/${TARGET}-flowgunso.tar
	docker load --input tarballs/${TARGET}-flrnnc.tar

schedule-weekly-build:
	python scripts/schedule-build.py

unschedule-weekly-build:
	python scripts/schedule-build.py --disable