VERSION=`cat VERSION`
GIT_BRANCH=`git rev-parse --abbrev-ref HEAD`

images: base-image dev-image

tag:
	git tag `cat VERSION`
	git push origin --tags master

prepare:
	cp Dockerfile.base base/Dockerfile
	cat Dockerfile.base Dockerfile.dev > dev/Dockerfile

base-image: prepare
	docker build --tag=texastribune/base:base \
		--tag=texastribune/base:$(GIT_BRANCH)-base \
		-f base/Dockerfile .

base-image-no-cache: prepare
	docker build --no-cache --tag=texastribune/base:base \
		--tag=texastribune/base:$(GIT_BRANCH)-base \
		-f base/Dockerfile .

dev-image: base-image
	docker build --tag=texastribune/base:dev \
		--tag=texastribune/base:$(GIT_BRANCH)-dev \
	-f dev/Dockerfile .

dev-image-no-cache: prepare
	docker build --tag=texastribune/base:dev
		--tag=texastribune/base:$(GIT_BRANCH)-dev \
	-f dev/Dockerfile .

base-shell: base-image
	docker run -it --rm --volume="$$(pwd)/poetry.lock:/poetry.lock" --volume="$$(pwd)/pyproject.toml:/pyproject.toml" texastribune/base:base bash

dev-shell: dev-image
	docker run -it --rm --volume=$$(pwd)/node:/node texastribune/base:dev bash
