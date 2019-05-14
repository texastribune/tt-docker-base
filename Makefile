all: base dev

tag:
	git tag `cat VERSION`
	git push origin --tags

prepare:
	cp Dockerfile.base base/Dockerfile
	cat Dockerfile.base Dockerfile.dev > dev/Dockerfile
.PHONY: base
base:
	docker build --tag=texastribune/base:base -f base/Dockerfile .

.PHONY: dev
dev: base
	docker build --tag=texastribune/base:dev -f dev/Dockerfile .

base-no-cache:
	docker build --no-cache --tag=texastribune/base:base -f base/Dockerfile .

dev-no-cache:
	docker build --tag=texastribune/base:dev -f dev/Dockerfile .

run-base: base
	docker run -it --rm --volume=$$(pwd)/poetry.lock:/poetry.lock --volume=$$(pwd)/pyproject.toml:/pyproject.toml texastribune/base:base bash

run-dev: dev
	docker run -it --rm --volume=$$(pwd)/package.json:/package.json --volume=$$(pwd)/yarn.lock:/yarn.lock texastribune/base:dev bash
