# Microservice Architecture & System Design with Python & Kubernetes

# Install
- docker [Reference to Installation Guide: `https://docs.docker.com/desktop/install/windows-install/`]
- minikube [Reference to Installation Guide: `https://minikube.sigs.k8s.io/docs/start/`]
- k9s [Reference to Installation Guide: `https://k9scli.io/topics/install/`]
- Python 3.x
- MySQL

# Tutorial

1. Creating our first service
```cmd
cd .\system_design\python\src\auth\
```
- Create a virtual environment
```cmd
python -m venv venv
```
- Activate the virtual environment
```cmd
.\venv\Scripts\activate
```
- Download libraries inside venv
```cmd
pip install pylint
pip install jedi
pip install pyjwt, jwt
pip install flask_mysqldb
```
- Create a `server.py`
- Set the environment variable for MySQL in venv:
```cmd
$env:MYSQL_HOST = 'localhost'
```
- Create a `init.sql`
- Download MySQL server and add it to System Path. (environment variables).
- Run command in venv:
```cmd
mysql -u root -p
```

# References
- https://www.youtube.com/watch?v=hmkF77F9TLw - Microservice Architecture and System Design with Python & Kubernetes