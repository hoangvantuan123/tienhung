#!/bin/bash
set -e

# Check if the password file is set and read the password from it
if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
    DB_PASSWORD=$PASSWORD
fi

# Define environment variables from Kubernetes Service
: ${DB_HOST:=103.167.198.18}  # IP Address of the PostgreSQL server
: ${DB_PORT:=5432}           # Default port for PostgreSQL
: ${DB_USER:=tienhung}       # PostgreSQL user
: ${DB_PASSWORD:=tienhung-admin@admin.com}  # PostgreSQL password

# Print the environment variables for debugging
echo "DB_HOST=${DB_HOST}"
echo "DB_PORT=${DB_PORT}"
echo "DB_USER=${DB_USER}"
echo "DB_PASSWORD=${DB_PASSWORD}"

DB_ARGS=()

# Function to check and update configuration in odoo.conf
function check_config() {
    param="$1"
    value="$2"
    if grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC"; then
        value=$(grep -E "^\s*\b${param}\b\s*=" "$ODOO_RC" | cut -d " " -f3 | sed 's/["\n\r]//g')
    fi
    DB_ARGS+=("--${param}")
    DB_ARGS+=("${value}")
}

# Update configuration parameters in odoo.conf
check_config "db_host" "$DB_HOST"
check_config "db_port" "$DB_PORT"
check_config "db_user" "$DB_USER"
check_config "db_password" "$DB_PASSWORD"


# Execute based on the first argument
case "$1" in
    -- | odoo)
        shift
        if [[ "$1" == "scaffold" ]]; then
            exec odoo "$@"
        else
            wait-for-psql.py ${DB_ARGS[@]} --timeout=30
            exec odoo "$@" "${DB_ARGS[@]}"
        fi
        ;;
    -*)
        wait-for-psql.py ${DB_ARGS[@]} --timeout=30
        exec odoo "$@" "${DB_ARGS[@]}"
        ;;
    *)
        exec "$@"
esac

exit 1
