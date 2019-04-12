all: base dev

tag:
	git tag `cat VERSION`
	git push origin --tags

.PHONY: base
base:
	docker build --tag=texastribune/base -f base/Dockerfile .

.PHONY: dev
dev: base
	docker build --tag=texastribune/dev -f dev/Dockerfile .
