from subprocess import Popen, PIPE, STDOUT
import subprocess
import random
import time


def run(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()


if __name__ == '__main__':
    start = time.time()
    remote = '`portal info deep_gpu -f remote`'
    ssh_run = "ssh {} '{{}}'".format(remote)
    token = int(random.random() * 100000000)

    # copy service file
    print('{} >>>> Pushing service file'.format(time.time() - start))
    subprocess.call('scp ./jupyter.service {}:/home/ubuntu/'.format(remote), shell=True)

    # setting jupyter auth token
    print('{} >>>> Set jupyter token'.format(time.time() - start))
    subprocess.call(ssh_run.format("echo \"c.NotebookApp.token = '{}'\" >> ~/.jupyter/"
                                   "jupyter_notebook_config.py".format(token)),
                    shell=True)

    # start the service
    print('{} >>>> Running jupyter notebook'.format(time.time() - start))
    cmd = 'sudo mv jupyter.service /etc/systemd/system/ &&\
     sudo systemctl daemon-reload &&\
     sudo systemctl enable jupyter.service &&\
     sudo systemctl start jupyter'
    subprocess.call(ssh_run.format(cmd), shell=True)

    # fetch instance ip
    print('{} >>>> Fetching the ip'.format(time.time() - start))
    ip = run("portal info deep_gpu -f ip").strip()

    # open in browser and run sync
    print('{} >>>> Opening in browser and starting sync'.format(time.time() - start))
    url = 'http://{}:8888/?token={}'.format(ip, token)
    subprocess.call("open {} && portal channel deep_gpu".format(url), shell=True)
