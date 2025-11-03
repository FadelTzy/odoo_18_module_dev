WEB_DB_NAME = odoo_development
DOCKER = docker
DOCKER_COMPOSE = ${DOCKER} compose
COTAINER_ODOO = odoo
COTAINER_DB = odoo-postgres

help:
	@echo "Available Targets"
	@echo "  start		start the compose with daemin"
	@echo "  stop		stop the compose"
	@echo "  restart		restart the compose"
	@echo "  console		odoo interactive console"
	@echo "  psql		postgresql interactive shell"
	@echo "  logs odoo		logs the odoo container"
	@echo "  logs db		logs the db container"
	@echo "  addon <addon_name> 	Restart instance and upgrade addon"

start:
	${DOCKER_COMPOSE} up -d

stop:
	${DOCKER_COMPOSE} down

restart:
	${DOCKER_COMPOSE} restart

console:
	${DOCKER} exec -it ${COTAINER_ODOO} odoo shell --db_host=${COTAINER_DB} -d ${WEB_DB_NAME} -r ${COTAINER_ODOO} -w ${COTAINER_ODOO} 

psql:
	${DOCKER} exec -it ${COTAINER_DB} psql -U ${COTAINER_ODOO} -d ${WEB_DB_NAME}

define log_target
	@if [ "$(1)" = "odoo" ]; then \
		$(DOCKER_COMPOSE) logs -f $(COTAINER_ODOO); \
	elif [ "$(1)" = "db" ]; then \
		$(DOCKER_COMPOSE) logs -f $(COTAINER_DB); \
	else \
		echo "invalid logs target"; \
	fi
endef

logs:
	$(call log_target,$(word 2,$(MAKECMDGOALS)))

define upgrade_addon
	$(DOCKER) exec -it $(COTAINER_ODOO) odoo --no-http --db_host=$(COTAINER_DB) -d $(WEB_DB_NAME) -r $(COTAINER_ODOO) -w $(COTAINER_ODOO) -u $(1) --dev xml
#        $(DOCKER) exec -it $(COTAINER_ODOO) odoo --no-http --db_host=$(COTAINER_DB) -d $(WEB_DB_NAME) -u $(1)

endef

addon: restart
	$(call upgrade_addon,$(word 2,$(MAKECMDGOALS)))

.PHONY: start stop restart console psql logs odoo db addon
