TARGET?=unstable

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

build:
	TARGET=${TARGET} CI_COMMIT_TAG=${CI_COMMIT_TAG} bash scripts/build-images.sh

build-test:
	docker build --build-arg TARGET=${TARGET} -t seafile-client:test tests/image

test:
	docker run seafile-client:test

documents:
	python scripts/make-documents.py docker.md.j2
	python scripts/make-documents.py seafile.md.j2

publish-images:
	TARGET=${TARGET} \
	DOCKER_HUB_BOT_USERNAME=${DOCKER_HUB_BOT_USERNAME} \
	DOCKER_HUB_BOT_TOKEN=${DOCKER_HUB_BOT_TOKEN} \
	DOCKER_HUB_OWNER_USERNAME=${DOCKER_HUB_OWNER_USERNAME} \
	DOCKER_HUB_OWNER_TOKEN=${DOCKER_HUB_OWNER_TOKEN} \
	DOCKER_HUB_IMAGE=${DOCKER_HUB_IMAGE} \
		bash scripts/publish-images.sh

publish-documents:
	bash scripts/publish-documents.sh
	python scripts/update-build-badge.py

save:
	mkdir -p tarballs/
	docker save --output tarballs/${TARGET}.tar seafile-client:${TARGET}

load:
	docker load --input tarballs/${TARGET}.tar

schedule-weekly-build:
	python scripts/schedule-build.py

unschedule-weekly-build:
	python scripts/schedule-build.py --disable