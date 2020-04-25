DOCKER_IMG="jeremy-mmia-final-project"
IMG_DIR=

docker:
	docker build -t $(DOCKER_IMG) .

poke: docker
	docker run --rm -ti $(DOCKER_IMG) \
		--outdir ./out \
		"UAB007-LF.jpg" \
		"UAB006-RF.jpg" \
		"UAB012-LH.jpg" \
		"UAB013-RH.jpg" \
		/radiographs \

