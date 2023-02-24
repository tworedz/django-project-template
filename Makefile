PHONY: deploy


deploy:
	: \
	&& docker compose build \
	&& docker compose up -d \
	&& docker image prune -f \
	&& docker container prune -f \
	&& :
