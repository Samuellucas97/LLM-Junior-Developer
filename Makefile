all: run
.PHONY: all build run clean

	
build: clean
	@echo
	@echo "******************** BUILDING THE VIRTUAL MACHINE **********************************"
	docker compose build
	@echo


run: build	 
	@echo
	@echo "******************** RUNNING THE VIRTUAL MACHINE **********************************"
	docker compose up -d
	@echo
	docker ps
	@echo
	@echo "Open your browser at http://<IPAddress>:5173"
	@echo


clean:
	@echo
	@echo "******************** CLEANING ENVIRONMENT **********************************"
	docker compose down
	@echo
	docker image rm -f llm-junior-developer-llmserver llm-junior-developer-backend llm-junior-developer-init-script llm-junior-developer-frontend
	@echo
	docker volume rm -f llm-junior-developer_mongo-data
	@echo
	docker ps
	@echo