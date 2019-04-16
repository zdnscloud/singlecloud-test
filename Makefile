build-image:
	docker build -t tanxu/many-logs:0.1.0 .
	docker image prune -f

docker: build-image
	docker push tanxu/many-logs:0.1.0