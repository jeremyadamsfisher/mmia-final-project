DOCKER_IMG=jeremy-mmia-final-project
IMG_DIR=$(shell pwd)/data
OUT_DIR=$(shell pwd)/out

default: demonstrate

run:
	(mkdir ./out) ; \
	docker run \
		--rm \
		--mount type=bind,source=$(IMG_DIR),target=/data \
		--mount type=bind,source=$(OUT_DIR),target=/out \
		-ti $(DOCKER_IMG) \
		skeleregister --outdir ./out ./data

docker:
	docker build -t $(DOCKER_IMG) .

demonstrate: docker run