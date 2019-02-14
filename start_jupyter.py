from subprocess import Popen, PIPE, STDOUT
import random
import time


def run(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read().strip()


if __name__ == '__main__':
    start = time.time()
    token = int(random.random() * 100000000)
    ip = run('portal info deep_gpu -f ip')
    ssh_run = "ssh ubuntu@{} '{{}}'".format(ip)

    print('>>> Uploading configs')
    o = run('echo "c.NotebookApp.token = \'{}\'" >> ./jupyter_notebook_config.py &&'
            'scp ./jupyter.service ubuntu@{}:~/ &&'
            'scp ./jupyter_notebook_config.py ubuntu@{}:~/ &&'
            'rm ./jupyter_notebook_config.py'.format(token, ip, ip))
    print(o)

    print('>>> Starting jupyter')
    o = run(ssh_run.format('sudo rm -r /etc/systemd/system/jupyter.service && '
                           'sudo mv ~/jupyter.service /etc/systemd/system/ && '
                           'sudo systemctl daemon-reload && '
                           'sudo systemctl enable jupyter.service && '
                           'rm -f ~/.jupyter/jupyter_notebook_config.py && '
                           'mv ~/jupyter_notebook_config.py ~/.jupyter/ && '
                           'sudo systemctl restart jupyter'))
    print(o)
    time.sleep(2)

    print('>>> Opening browser and start sync')
    o = run('open http://{}:8888/?token={} &&'
            'portal channel deep_gpu'.format(ip, token))
    print(o)
