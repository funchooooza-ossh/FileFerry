# ==== Конфигурация ====
APP_NAME := fileferry
DOCKER_IMAGE := $(APP_NAME):local
K8S_DIR := k8s
K8S_BASE := k8s/base
K8S_LOCAL := k8s/overlays/local
KIND_CLUSTER_NAME := fileferry-local
KIND_CONFIG := kind/kind-config.yaml

# ==== Билд образа ====
build:
	docker build -t $(DOCKER_IMAGE) ./fileferry
	kind load docker-image $(DOCKER_IMAGE) --name $(KIND_CLUSTER_NAME)
# ==== Подготовка окружения для kustomize ====
prepare:
	@echo "[PREPARE] Обновляем fileferry.env..."
	@rm -f $(K8S_LOCAL)/fileferry.env
	@cat ./environments/*.env > $(K8S_LOCAL)/fileferry.env

	@echo "[PREPARE] Копируем конфигурации Prometheus..."
	@cp ./prometheus/prometheus.yml $(K8S_BASE)/prometheus/prometheus.yml
	@cp ./prometheus/alerts.yml $(K8S_BASE)/prometheus/alerts.yml

# ==== Kind cluster ====
kind-up:
	kind create cluster --name $(KIND_CLUSTER_NAME) --config $(KIND_CONFIG)

kind-down:
	kind delete cluster --name $(KIND_CLUSTER_NAME)

# ==== Kubernetes ====
deploy:
	kubectl apply -k $(K8S_LOCAL)

destroy:
	kubectl delete -k $(K8S_LOCAL)

logs:
	kubectl logs -l io.kompose.service=$(APP_NAME) --tail=100

ps:
	kubectl get pods

exec:
	kubectl exec -it $$(kubectl get pod -l io.kompose.service=$(APP_NAME) -o jsonpath="{.items[0].metadata.name}") -- sh
migrate:
	kubectl exec -it $$(kubectl get pod -l io.kompose.service=$(APP_NAME) -o jsonpath="{.items[0].metadata.name}") -- \
	alembic upgrade head
# ==== Полная перезагрузка ====
restart: destroy prepare build deploy

start: prepare build deploy

.PHONY: build kind-up kind-down deploy destroy logs exec restart
