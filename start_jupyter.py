from subprocess import Popen, PIPE, STDOUT
import subprocess
import random

remote = '`portal info deep_gpu -f remote`'
ssh_run = "ssh {} '{{}}'".format(remote)
token = int(random.random() * 100000000)


def run(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()


# copy service file
print('>>>> Pushing service file')
subprocess.call('scp ./jupyter.service {}:/home/ubuntu/'.format(remote), shell=True)

# setting jupyter auth token
print('>>>> Set jupyter token')
subprocess.call(ssh_run.format("echo 'export JUPYTER_TOKEN={}' >> ~/.bashrc".format(token)),
                shell=True)

# start the service
print('>>>> Running jupyter notebook')
cmd = 'sudo mv jupyter.service /etc/systemd/system/ &&\
 sudo systemctl daemon-reload &&\
 sudo systemctl enable jupyter.service &&\
 sudo systemctl start jupyter'
subprocess.call(ssh_run.format(cmd), shell=True)

# fetch instance ip
print('>>>> Fetching the ip')
ip = run("portal info deep_gpu -f ip").strip()

# open in browser and run sync
print('>>>> Opening in browser and starting sync')
url = 'http://{}:8888/?token={}'.format(ip, token)
subprocess.call("open {} && portal channel deep_gpu".format(url), shell=True)
