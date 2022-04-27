import os
import sys
import fileinput

service_name = 'elevation_map'
service_path = f'{service_name}.service'

def replace_path(replacement, filename, exec_path):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(replacement, exec_path), end='')

def exec_commands(commands):
    for cmd in commands:
        print(cmd)
        if 0 != os.system(cmd):
            print(f'Error: {cmd} command failed')
            sys.exit(-1)

def create_service(srv_path):
    commands = [
            f'sudo cp -f {srv_path} /usr/lib/systemd/system/',
            f'sudo systemctl daemon-reload',
            f'sudo systemctl start {service_name}',
            f'sudo ln -sf {srv_path} /etc/systemd/',
    ]
    exec_commands(commands)

def install_service(exec_path):
    srv_path = exec_path.replace('app.py', f'{service_path}')
    replace_path('PY_EXEC_PWD', srv_path, os.getcwd())
    replace_path('PY_EXEC_PATH', srv_path, exec_path)
    create_service(srv_path)

def uninstall_service():
    commands = [
            f'sudo systemctl daemon-reload',
            f'sudo systemctl stop {service_name}',
            f'sudo rm -f /usr/lib/systemd/system/{service_path}',
            f'sudo rm -f /etc/systemd/{service_path}',
    ]
    exec_commands(commands)
