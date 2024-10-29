# Flask App Deployment with Ansible

This project deploys a Flask application connected to a MySQL/MariaDB database in a production environment using Ansible. The app is served by Gunicorn, with Nginx as a reverse proxy, ensuring a production-ready setup.

## Project Structure

- **`ansible.cfg`**: Ansible configuration file, setting options for privilege escalation, host key checking, and other default behaviors.
- **`app.py`**: The Flask application that connects to a MySQL database. It provides basic API endpoints to interact with the database.
- **`inventory.txt`**: Inventory file specifying target hosts (IP addresses) and SSH credentials for running the Ansible playbook.
- **`playbook.yml`**: The main Ansible playbook that orchestrates the entire deployment by calling individual roles or tasks.
- **`group_vars/`**: Contains variables specific to host groups, allowing centralized configuration management for `db_and_web_servers`.
- **`tasks/`**: Houses individual task files, each dedicated to setting up specific components like `deploy_db.yml` (for the database), `deploy_nginx.yml` (for Nginx), and `deploy_web.yml` (for the Flask app with Gunicorn).

## File Details

### `app.py`

This file contains the Flask app code. Key functionalities include:

- **MySQL Configuration**: Reads environment variables for MySQL configuration, defaulting to:
  - `host`: `127.0.0.1`
  - `user`: `db_user`
  - `password`: `Passw0rd`
  - `database`: `employee_db`

- **Routes**:
  - `/`: Basic welcome message.
  - `/how_are_you`: Returns a friendly message.
  - `/read_from_database`: Connects to the database and retrieves employee names from the `employees` table, returning them in a list format.

### `playbook.yml`

This is the primary Ansible playbook that automates the deployment process by calling individual tasks from `tasks/`, such as:

1. **Database Setup (`tasks/deploy_db.yml`)**:
   - Creates the database `employee_db`.
   - Sets up a user (`db_user`) with access permissions to the database.
   - Creates an `employees` table and inserts sample data.

2. **Gunicorn Setup (`tasks/deploy_web.yml`)**:
   - Configures Gunicorn as a systemd service to serve the Flask app.

3. **Nginx Configuration (`tasks/deploy_nginx.yml`)**:
   - Configures Nginx as a reverse proxy, forwarding requests to Gunicorn on `127.0.0.1:5000`.

### `inventory.txt`

The inventory file defines the remote servers to configure. 

```plaintext
[db_and_web_servers]
db_and_web_server1 ansible_host=10.10.0.115 ansible_ssh_pass=Passw0rd
db_and_web_server2 ansible_host=10.10.0.116 ansible_ssh_pass=Passw0rd
```

Each entry includes:
- `ansible_host`: IP address of the server.
- `ansible_ssh_pass`: Password for SSH access.

### `group_vars/db_and_web_servers.yml`

Contains group-specific variables for the `db_and_web_servers` group, centralizing configuration for the database and web server settings used in `playbook.yml`.

### `ansible.cfg`

This file configures Ansible settings:
- **`host_key_checking = False`**: Disables SSH host key checking.
- **Privilege Escalation**:
  - `become = True`
  - `become_method = sudo`
  - `become_user = adrian`

## Prerequisites

- Ansible installed on the control machine (your local or another machine).
- SSH access to the target servers specified in `inventory.txt`.

## Running the Playbook

1. **Test Connection**:
   Test the connection to your servers with:

   ```bash
   ansible -i inventory.txt -m ping all
   ```

   This should return a successful `pong` response from each server.

2. **Run the Playbook**:
   Execute the playbook to deploy the app:

   ```bash
   ansible-playbook playbook.yml -i inventory --ask-vault-pass
   ```

   The playbook will:
   - Install and configure all necessary software on each server.
   - Set up the database and insert sample data.
   - Deploy and start the Flask application with Gunicorn and Nginx.

3. **Access the Application**:
   Open a web browser and go to the IP address of any configured server (without specifying port 5000). For example:

   ```
   http://10.10.0.115
   ```

   Nginx will forward requests to Gunicorn, which serves the Flask app.
