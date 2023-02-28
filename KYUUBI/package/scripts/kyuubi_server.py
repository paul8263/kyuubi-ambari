# -*- coding: utf-8 -*-
"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from resource_management import *
from resource_management.core.resources.system import File
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import \
    check_process_status
from kyuubi_utils import *
import pwd,grp
import os


class KyuubiServer(Script):

    def install(self, env):
        import params
        env.set_params(params)

        Logger.info('Creating Kyuubi group')

        try:
            grp.getgrnam(params.kyuubi_group)
        except KeyError:
            Group(params.kyuubi_group)

        Logger.info('Creating Kyuubi user')
        try:
            pwd.getpwnam(params.kyuubi_user)
        except KeyError:
            User(params.kyuubi_user,
                 gid=params.kyuubi_group,
                 groups=[params.kyuubi_group],
                 ignore_failures=True
                 )

        Logger.info('Creating Kyuubi install directory')
        Directory([params.kyuubi_installation_path],
                  mode=0755,
                  cd_access='a',
                  owner=params.kyuubi_user,
                  group=params.kyuubi_group,
                  create_parents=True
                  )

        Logger.info('Check existing files')
        if os.path.exists(os.path.join(params.kyuubi_installation_path, 'kyuubi.tar.gz')):
            Logger.info('Kyuubi tarball exists. Delete it before downloading')
            Execute("rm -f {0}".format(os.path.join(params.kyuubi_installation_path, 'kyuubi.tar.gz')))

        if os.path.exists(params.KYUUBI_HOME):
            Logger.info('Kyuubi binary has been extracted. Delete it before installation')
            Execute("rm -rf {0}".format(params.KYUUBI_HOME))

        Logger.info('Downloading Kyuubi binaries')
        Execute("cd {0}; wget {1} -O kyuubi.tar.gz".format(params.kyuubi_installation_path, params.kyuubi_download_url),
                user=params.kyuubi_user)

        Logger.info('Extracting Kyuubi binaries')
        Execute("cd {0}; tar -zxvf kyuubi.tar.gz".format(params.kyuubi_installation_path), user=params.kyuubi_user)
        File(os.path.join(params.kyuubi_installation_path, 'kyuubi.tar.gz'), action='delete')

        Logger.info('Modify log folder access permissions')
        Execute("chmod 777 {0}/logs".format(params.KYUUBI_HOME), user=params.kyuubi_user)

        Logger.info('Delete Kyuubi tarball')
        Execute("rm -f {0}".format(os.path.join(params.kyuubi_installation_path, 'kyuubi.tar.gz')))

        self.configure(env)
        Logger.info('Kyuubi installation completed')

    def stop(self, env):
        import params
        env.set_params(params)

        Logger.info('Stopping Kyuubi server')
        Execute(get_stop_kyuubi_server_cmd(), user=params.kyuubi_user)

        Logger.info('Kyuubi server stopped')

    def start(self, env):
        import params
        env.set_params(params)

        Logger.info('Updating Kyuubi configuration')
        self.configure(env)

        Logger.info('Starting Kyuubi server')
        Execute(get_restart_kyuubi_server_cmd(), user=params.kyuubi_user)

        Logger.info('Kyuubi server successfully started')

    def status(self, env):
        import params
        env.set_params(params)
        pid_file = get_kyuubi_server_pid_file_path()
        check_process_status(pid_file)

    def configure(self, env):
        Logger.info('Configuring Kyuubi')
        import params
        env.set_params(params)
        kyuubi_conf_dir = os.path.join(params.KYUUBI_HOME, 'conf')

        File(os.path.join(kyuubi_conf_dir, 'kyuubi-defaults.conf'),
             content=Template("kyuubi-defaults.conf.j2"),
             owner=params.kyuubi_user,
             group=params.kyuubi_group
             )

        File(os.path.join(kyuubi_conf_dir, 'kyuubi-env.sh'),
             content=params.kyuubi_env,
             owner=params.kyuubi_user,
             group=params.kyuubi_group
             )

        File(os.path.join(kyuubi_conf_dir, 'log4j2.xml'),
             content=params.kyuubi_log4j2,
             owner=params.kyuubi_user,
             group=params.kyuubi_group
             )


if __name__ == '__main__':
    KyuubiServer().execute()
