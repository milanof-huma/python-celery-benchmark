
IMAGE ?= "humaoss/python-celery-benchmark:v0.0.1"

app/setup-venv:
	@echo '+ Setting up venv'
	@python3 -m venv venv
	@. ./venv/bin/activate && pip install wheel && pip install -r requirements.txt

app/run-deps:
	@echo '+ Running deps including redis...'
	@docker-compose up start_dependencies

app/build-docker:
	@echo '+ Building docker image $(IMAGE)'
	@docker build ./docker/Dockerfile -t $(IMAGE)

app/run-docker: app/build-docker
	@echo '+ Running docker image on port 5001'
	@docker run -it -p5001:5000 $(IMAGE)

app/push-to-docker-hub: app/build-docker
	@echo 'NOTE: login to docker by $ docker login'
	@docker push $(IMAGE)