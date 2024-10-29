---

# Flask App Deployment with Gunicorn and Nginx in Production

This project automates the deployment of a Flask application connected to a MySQL database, using Gunicorn as the WSGI HTTP server and Nginx as a reverse proxy. The deployment is managed via an Ansible playbook that includes roles for setting up the necessary components.

## Project Structure

```plaintext
.
├── app.py                # Flask application source file
├── playbook.yml          # Main Ansible playbook to deploy the application
├── group_vars/           # Directory containing encrypted Ansible group variables
│   └── db_and_web_servers.yml  # Encrypted database and app credentials (using Ansible Vault)
├── roles/                # Ansible roles to manage different components of the deployment
│   ├── mysql_db/         # Role to configure and set up MySQL database
│   │   └── tasks/
│   │       └── main.yml  # MySQL database setup tasks
│   ├── flask_web/        # Role to configure Flask app deployment
│   │   └── tasks/
│   │       └── main.yml  # Flask app setup tasks
│   ├── nginx/            # Role to configure Nginx as reverse proxy
│   │   └── tasks/
│   │       └── main.yml  # Nginx setup tasks
│   └── packages/         # Role to ensure all required packages are installed
│       └── tasks/
│           └── main.yml  # Package installation tasks
└── README.md             # Project documentation
```

## Pre-Requisites

1. **Ansible**: Ensure Ansible is installed on the control machine.
2. **Ansible Vault**: Sensitive credentials are stored in an encrypted file using Ansible Vault.
3. **Inventory File**: The `inventory` file is encrypted and must be decrypted using Ansible Vault before use.

## Flask Application (`app.py`)

The Flask app connects to a MySQL database using MySQL configurations set in environment variables. It offers basic endpoints to test database connectivity and fetch data:

- **GET /** - Welcome message.
- **GET /how_are_you** - Returns a sample response.
- **GET /read_from_database** - Fetches employee names from the `employees` table in MySQL.

## Playbook (`playbook.yml`)

The `playbook.yml` file is the main entry point for the deployment. It includes the following roles:

- **mysql_db**: Installs and configures MySQL server, sets up the database, user, and grants privileges.
- **flask_web**: Configures the Flask application in the production environment.
- **nginx**: Configures Nginx as a reverse proxy to handle incoming HTTP requests to Gunicorn.
- **packages**: Ensures all necessary packages (e.g., Python, Gunicorn, Nginx, MySQL) are installed on the servers.

## How to Run the Playbook

1. **Decrypt Inventory and Variable Files**: 
   Ensure you have decrypted the `inventory` and `group_vars/db_and_web_servers.yml` files:

   ```bash
   ansible-vault decrypt inventory
   ansible-vault decrypt group_vars/db_and_web_servers.yml
   ```

2. **Run the Playbook**:
   Execute the playbook with the following command:

   ```bash
   ansible-playbook -i inventory --ask-vault-pass playbook.yml
   ```

   You will be prompted for the Ansible Vault password used to encrypt sensitive information.

## Security Considerations

- **Ansible Vault**: All sensitive data, including database passwords and host information, is stored in encrypted files.
- **Environment Variables**: Database credentials are passed securely to the Flask app via environment variables configured within the Ansible roles.

## Additional Information

The deployment configures:

- **MySQL Database**: Initialized with an `employees` table.
- **Gunicorn**: Configured as the WSGI server to serve the Flask app.
- **Nginx**: Configured to reverse proxy requests to Gunicorn on port 5000, handling HTTP requests at port 80.

Ensure that your server’s firewall allows traffic on ports 80 (HTTP) and 5000 (Flask app port for testing) if accessed directly.
