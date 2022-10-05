# Cloud Sec Task

The goal of this repo was to use Ansible to automate the deployment of simple services for ssh attempts matrices. The following are the primary services:
  - alpha_server.py
  - alpha_client.py
  - alpha_report.py


## Setup
- The repo includes an Ansible inventory file, which is located in **ansible/hosts**. Add the IP of nodeABC (client) and nodeXYZ (server) there. 

```bash
$ nano hosts

        [client]
        10.x.x.x #nodeABC

        [server]
        10.x.x.x #nodeXYZ

        [all:vars]
        server_address=10.x.x.x #nodeXYZ_IP
        server_port=8888
        mysql_host=10.x.x.x  #nodeXYZ_IP
        mysql_username=<PUT_MYSQL_USER_HERE>
        mysql_password=<PUT_MYSQL_PASS_HERE>

$ ansible-playbook playbook.yml -i hosts
```

- And using Ansible roles for seperate every task that we want automate, which located in **ansible/roles**.


```bash
ansible/roles
├── appclient
├── appserver
├── initconfig
├── mysql
├── testingclient
└── testingserver
```

## Show the matrices
- Run the script `alpha_report.py` with periodically program such as `watch`
```bash
watch -n1 python3 alpha_report.py
```

