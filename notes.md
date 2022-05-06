
docker network create jupyterhub

docker build -t jupyterhub_simple:0.1 .

docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --net jupyterhub --name jupyterhub_simple -p 8000:8000 jupyterhub_simple:0.1

# old docker file

    FROM ubuntu:latest
    RUN apt-get update && apt-get -y update \
        && apt-get install -y apt-utils dialog \
        && apt-get install -y build-essential python3.10 python3-pip python3-dev \
        && apt-get -y install nodejs npm \
        && apt-get -y install python3.10-venv

    RUN npm install -g configurable-http-proxy

    RUN mkdir src
    RUN mkdir src/jupyterhub


    ARG user=jupyterhub
    ARG home=/home/$user
    RUN addgroup --system docker
    RUN adduser \
        --disabled-password \
        --gecos "" \
        --home $home \
        --ingroup docker \
        $user

    RUN echo "jupyterhub:jupyterhub" | chpasswd

    RUN groupadd jupyterhub

    RUN usermod -aG jupyterhub jupyterhub

    RUN chgrp -R jupyterhub /src

    RUN chmod -R 2775 /src

    #USER jupyterhub

    ENV VIRTUAL_ENV=/src/venv
    RUN python3 -m venv $VIRTUAL_ENV
    ENV PATH="$VIRTUAL_ENV/bin:$PATH"

    # Install dependencies:
    #COPY requirements.txt .
    #RUN pip install -r requirements.txt


    RUN pip -q install pip --upgrade


    WORKDIR src/
    COPY . .

    RUN pip install jupyterhub
    RUN pip install jupyterlab notebook  
    RUN pip install dockerspawner

    ### this has to be done on command line or?
    VOLUME /var/run/docker.sock:/var/run/docker.sock:rw

    VOLUME /usr/local/share/jupyterhub:/usr/local/share/jupyterhub:rw

    CMD ["jupyterhub", "--port=8000", "--ip=0.0.0.0"]


# old config

    c.Application.log_datefmt = '%Y-%m-%d %H:%M:%S'
    c.Application.log_format = '[%(name)s]%(highlevel)s %(message)s'
    c.Application.log_level = 30

    c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

    c.LocalAuthenticator.create_system_users = True

    c.JupyterHub.bind_url = 'http://0.0.0.0:8000/'

    #  Default: 'jupyterhub_config.py'
    c.JupyterHub.config_file = '/src/jupyterhub_config.py'

    ## File in which to store the cookie secret.
    #  Default: 'jupyterhub_cookie_secret'
    c.JupyterHub.cookie_secret_file = '/src/jupyterhub/jupyterhub_cookie_secret'

    c.ConfigurableHTTPProxy.pid_file = '/src/jupyterhub/jupyterhub-proxy.pid'

    c.SudoSpawner.sudospawner_path = '/opt/venv/bin/sudospawner'

    c.Spawner.default_url = '/tree/home/'

    c.Spawner.notebook_dir='/src/jupyterhub/'

    c.Spawner.cmd = '/opt/venv/bin/jupyterhub-singleuser'

    ## The location of jupyterhub data files (e.g. /usr/local/share/jupyterhub)

    c.JupyterHub.data_files_path = '/opt/venv/share/jupyterhub'

    ## url for the database. e.g. `sqlite:///jupyterhub.sqlite`
    #  Default: 'sqlite:///jupyterhub.sqlite'
    c.JupyterHub.db_url = 'sqlite://///src/jupyterhub/jupyterhub.sqlite'

    ## log all database transactions. This has A LOT of output
    #  Default: False
    c.JupyterHub.debug_db = False

    #  Default: '127.0.0.1'
    c.JupyterHub.hub_ip = '127.0.0.1'

    #  Defaults to an empty set, in which case no user has admin access.
    #  Default: set()
    # c.Authenticator.admin_users = set()
    c.Authenticator.admin_users = {'jupyterhub'}

    ## Set of usernames that are allowed to log in.
    #  
    #  Use this with supported authenticators to restrict which users can log in.
    #  This is an additional list that further restricts users, beyond whatever
    #  restrictions the authenticator has in place. Any user in this list is granted
    #  the 'user' role on hub startup.
    #  
    #  If empty, does not perform any additional restriction.
    c.Authenticator.allowed_users = {'jupyterhub'}

    ##

    ## Docker spawner
    c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
    c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
    c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
    # See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
    c.JupyterHub.hub_ip = os.environ['HUB_IP']

    # user data persistence
    # see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
    #notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')
    #c.DockerSpawner.notebook_dir = notebook_dir
    #c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

    # Other stuff
    c.Spawner.cpu_limit = 1
    c.Spawner.mem_limit = '10G'
