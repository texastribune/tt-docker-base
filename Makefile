VERSION=`cat VERSION`
GIT_BRANCH=`git rev-parse --abbrev-ref HEAD`

images: base dev

tag:
	git tag `cat VERSION`
	git push origin --tags

prepare:
	cp Dockerfile.base base/Dockerfile
	cat Dockerfile.base Dockerfile.dev > dev/Dockerfile

.PHONY: base
base: prepare
	docker build --tag=texastribune/base:base \
		--tag=texastribune/base:$(VERSION)-base \
		--tag=texastribune/base:$(GIT_BRANCH)-base \
		-f base/Dockerfile .

base-no-cache: prepare
	docker build --no-cache --tag=texastribune/base:base \
		--tag=texastribune/base:$(VERSION)-base \
		--tag=texastribune/base:$(GIT_BRANCH)-base \
		-f base/Dockerfile .

.PHONY: dev
dev: base
	docker build --tag=texastribune/base:dev \
		--tag=texastribune/base:$(VERSION)-dev \
		--tag=texastribune/base:$(GIT_BRANCH)-dev \
	-f dev/Dockerfile .

dev-no-cache: prepare
	docker build --tag=texastribune/base:dev
		--tag=texastribune/base:$(VERSION)-dev \
		--tag=texastribune/base:$(GIT_BRANCH)-dev \
	-f dev/Dockerfile .

run-base: base
	docker run -it --rm --volume=$$(pwd)/poetry.lock:/poetry.lock --volume=$$(pwd)/pyproject.toml:/pyproject.toml texastribune/base:base bash

run-dev: dev
	docker run -it --rm --volume=$$(pwd)/package.json:/package.json --volume=$$(pwd)/yarn.lock:/yarn.lock texastribune/base:dev bash
