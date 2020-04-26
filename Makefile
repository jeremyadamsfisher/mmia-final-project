DOCKER_IMG=jeremy-mmia-final-project
IMG_DIR=/Users/jeremyfisher/ra2challenge/data/raw/images

docker:
	docker build -t $(DOCKER_IMG) .

poke: docker
	docker run \
		--rm \
		--mount type=bind,source=$(IMG_DIR),target=/radiographs,readonly \
		--mount type=bind,source=$(PWD)/out,target=/out \
		-ti $(DOCKER_IMG) \
		skeleregister --outdir ./out ./radiographs

