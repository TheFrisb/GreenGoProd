up:
	sudo docker compose up -d

down:
	sudo docker compose down

clean-volumes:
	sudo docker compose down -v


format:
	black .
	ruff check . --select I,F401 --fix