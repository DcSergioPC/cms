# Usa la imagen base de Keycloak
FROM quay.io/keycloak/keycloak:22.0

# Establece las variables de entorno

ENV KEYCLOAK_ADMIN=admin
ENV KC_DB=postgres
ENV KC_DB_URL=jdbc:postgresql://192.168.100.250:5432/
ENV KC_DB_USERNAME=postgres

# Comando de entrada para iniciar Keycloak en modo desarrollo
ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev"]
