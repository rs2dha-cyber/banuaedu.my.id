import sys
project_home = "/home/USERNAME/banua_edu"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import create_app
application = create_app()
