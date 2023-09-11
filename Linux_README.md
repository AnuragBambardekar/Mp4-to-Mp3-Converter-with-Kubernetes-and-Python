**Got Access to Linux Machine**
Now that I have a Linux system. I did the following:
- Installed `docker` engine (Follow all the steps here: https://docs.docker.com/desktop/install/linux-install/)
- Installed `kubectl` (Follow all the steps here: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- Installed `minikube` (Follow all the steps here: https://minikube.sigs.k8s.io/docs/start/)
- Installed `k9s` (Follow all the steps here: https://github.com/derailed/k9s) [curl -sS https://webinstall.dev/k9s | bash]

If at some point you get the following error:
```cmd
Reading package lists... Error!
E: LZ4F: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_jammy_multiverse_binary-amd64_Packages.lz4 Unexpected end of file
E: LZ4F: /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_jammy_multiverse_binary-amd64_Packages.lz4 Read error (18446744073709551615: ERROR_GENERIC)
E: The package lists or status file could not be parsed or opened.
```

Then, the fix is:
```cmd
sudo rm /var/lib/apt/lists/* -vf
sudo apt-get clean
sudo apt-get update
```

Also do:
```cmd
sudo apt install python3.10-venv
```

To fix flask_mysqldb installation errors:
```cmd
sudo apt install pkg-config
pip install mysqlclient
pip install flask_mysqldb
```

Set Environment variable for MySQL:
```cmd
export MYSQL_HOST=localhost
```

Create DB from `init.sql` file:
```cmd
sudo mysql -uroot < init.sql
sudo mysql -uroot
```

```cmd
mysql> show databases;
mysql> use auth;
mysql> show tables;
mysql> describe user;
mysql> select * from user;
```

`To drop the Table & Database, Run:`
```cmd
mysql -uroot -e "DROP USER auth_user@localhost"
```

- create the auth directory scripts and then Dockerfile and then run:
Build docker file (not from venv):
```cmd
sudo docker build .
```

```cmd
sudo docker tag cdcb0f0188c8779ea38d2c58f3562c635f401fd48bf58 anuragb98/auth_ubuntu:latest
sudo docker image ls
```

```cmd
sudo docker login # Enter login creds
sudo docker push anuragb98/auth_ubuntu:latest
```

```cmd
native@node1-1:~/Desktop/system_design/Kubernetes-with-Python/system_design/python/src/auth$ minikube start
```

From within the auth/manifests directory run:
```cmd
kubectl apply -f ./
```

- made the gateway service folder, wrote the scripts then create Dockerfile as earlier and run (not from venv):
```cmd
/system_design/python/src/gateway$ sudo docker build .
/system_design/python/src/gateway$ sudo docker tag c9bd9267065fbcc004c16da8ee84a20208298ccb15038bfe5fd09d993ccca4dc anuragb98/gateway_ubuntu:latest
/system_design/Kubernetes-with-Python/system_design/python/src/gateway$ sudo docker push anuragb98/gateway_ubuntu:latest
```

Now back to where we got stuck while implementing this on a Windows system.

- After editing the `ingress.yaml` file, Do the following:
```cmd
sudo vim /etc/hosts
```

Then add the following line:
`127.0.0.1 mp3converter.com`

```cmd
minikube addons enable ingress
```

**Ran into a problem where I had insufficient hardware space to enable ingress**