from fabric.api import local, run, env, get, cd


def free():
    env.hosts = ["35.161.133.251"]
    env.user = "ubuntu"
    env.key_filename = "/home/kike/.ssh/aws2016pem.pem"
    env.working_dir = "/home/ubuntu/tesis-final"


def get_file(filename):
    with cd(env.working_dir):
        get(filename)
