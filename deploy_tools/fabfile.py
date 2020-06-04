from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL='https://github.com/satellitestar/-TDD.git'

def depoly():
    site_folder = f'/{env.user}/sites/123.56.240.164/{env.host}'
    source_folder=site_folder+'/source'
    # _create_directory_structure_if_necessary(site_folder)
    # _get

def _create(site_folder):
    for subfolder in ('database','static','virtualenv','souce'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get(source_folder):
    if exists(source_folder+'/.git'):
        run(f'cd {source_folder} && git fetch')

    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit=local('git log -n 1 --format=%H',capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
    sp = source_folder+'/superlists/settings.py'
    sed(sp,'DEBUG = True','DEBUG = False')
    sed(sp,
        'ALLOWED_HOSTS=.+$',
        f'ALLOWED_HOSTS=["{site_name}"]'
        )
    skf = source_folder+'/superlists/secret_key.py'
    if not exists(skf):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()_+-='
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(skf, f'SECRET_KEY="{key}"')
    append(sp,'\nfrom.secret_key import SECRET_KEY')

def _update_v(source_folder):
    v=source_folder+'/../virtualenv'
    if not  exists(v+'/bin/pip'):
        run(f'python3.6 -m venv {v}' )
    run(f'{v}/bin/pip install -r {source_folder}/requirements.txt')

def _update_s(source_folder):
    run(
        f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_d(source_folder):
    run(
        f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py migrate --noinput'
    )
