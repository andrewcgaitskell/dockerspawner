import oauthenticator

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

c = get_config()  # noqa

# dummy for testing. Don't use this in production!
## c.JupyterHub.authenticator_class = "dummy"

# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'

# launch with docker
# c.JupyterHub.spawner_class = "docker"

c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0'

# The docker instances need access to the Hub, so the default loopback port doesn't work:
#from jupyter_client.localinterfaces import public_ips

#c.JupyterHub.hub_ip = public_ips()[0]


#c.Authenticator.whitelist = whitelist = set()

oauthenticator.GitHubOAuthenticator.allowed_users = whitelist = set()

c.Authenticator.admin_users = admin = set()

import os

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

OAUTH_CALLBACK_URL = os.environ.get("OAUTH_CALLBACK_URL")

c.GitHubOAuthenticator.oauth_callback_url = OAUTH_CALLBACK_URL



# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
c.JupyterHub.hub_connect_ip = 'jupyterhub_simple'

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image = 'jupyter/base-notebook'

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = 'jupyterhub'

# delete containers when the stop
c.DockerSpawner.remove = True

