TARGET?=oldstable  # or stable, unstable

mock:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml up --remove-orphans -d

unmock:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml down

client:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml rm -fs client
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml up --remove-orphans -d client

shell:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml run --rm client bash

logs:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml logs -f client

ps:
	TARGET=${TARGET} docker compose -f tests/mock/compose.yaml ps

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

save:
	mkdir -p tarballs/
	docker save --output tarballs/${TARGET}.tar seafile-client:${TARGET}

load:
	docker load --input tarballs/${TARGET}.tar

schedule-weekly-build:
	python scripts/schedule-build.py

unschedule-weekly-build:
	python scripts/schedule-build.py --disable