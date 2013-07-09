import os
import sys

from django.db.backends import BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    executable_name = 'mongo'

    def runshell(self):
        settings_dict = self.connection.settings_dict
        args = [self.executable_name]
        if settings_dict['USER']:
            args += ["-u", settings_dict['USER']]
        if settings_dict['HOST']:
            args.extend(["--host", settings_dict['HOST']])
        if settings_dict['PORT']:
            args.extend(["--p", str(settings_dict['PORT'])])
        args += [settings_dict['NAME']]
        if os.name == 'nt':
            sys.exit(os.system(" ".join(args)))
        else:
            os.execvp(self.executable_name, args)

