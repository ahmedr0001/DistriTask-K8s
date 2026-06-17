kubectl --namespace distritask get secrets monitoring-stack-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
