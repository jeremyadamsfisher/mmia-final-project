DOCKER_IMG=jeremy-mmia-final-project
IMG_DIR=$(PWD)/data

run:
	(mkdir ./out) ; \
	docker run \
		--rm \
		--mount type=bind,source=$(IMG_DIR),target=/radiographs \
		--mount type=bind,source=$(PWD)/out,target=/out \
		-ti $(DOCKER_IMG) \
		skeleregister --outdir ./out ./radiographs

docker:
	docker build -t $(DOCKER_IMG) .

demonstrate: docker run