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
    print(
        run(
            f"""echo "c.NotebookApp.token = \'{token}\'" >> ./jupyter_notebook_config.py && scp ./jupyter.service ubuntu@{ip}:~/ && scp ./jupyter_notebook_config.py ubuntu@{ip}:~/ && rm ./jupyter_notebook_config.py"""
        )
    )

    print('>>> Starting jupyter')
    print(run(ssh_run.format('mkdir -p ~/ext_mount/notebooks ~/ext_mount/repo && '
                             'sudo rm -f /etc/systemd/system/jupyter.service && '
                             'sudo mv ~/jupyter.service /etc/systemd/system/ && '
                             'sudo systemctl daemon-reload && '
                             'sudo systemctl enable jupyter.service && '
                             'rm -f ~/.jupyter/jupyter_notebook_config.py && '
                             'mv ~/jupyter_notebook_config.py ~/.jupyter/ && '
                             'sudo systemctl restart jupyter')))

    print('>>> Opening browser and start sync')
    print(run(f'open http://{ip}:8888/?token={token} && portal channel deep_gpu'))
