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
from resource_management.core.logger import Logger
import os


def get_restart_kyuubi_server_cmd():
    import params
    KYUUBI_CMD = os.path.join(params.KYUUBI_HOME, 'bin/kyuubi')
    return KYUUBI_CMD + ' restart'


def get_stop_kyuubi_server_cmd():
    import params
    KYUUBI_CMD = os.path.join(params.KYUUBI_HOME, 'bin/kyuubi')
    return KYUUBI_CMD + ' stop'


def get_status_kyuubi_server_cmd():
    import params
    KYUUBI_CMD = os.path.join(params.KYUUBI_HOME, 'bin/kyuubi')
    return KYUUBI_CMD + ' status'


def get_kyuubi_server_pid_file_path():
    import params
    return os.path.join(params.KYUUBI_HOME, 'pid', 'kyuubi-' + params.kyuubi_user + '-org.apache.kyuubi.server.KyuubiServer.pid')


def get_zookeeper_ensemble_str():
    zookeeper_port = default('/configurations/zoo.cfg/clientPort', None)
    zookeeper_hosts = default('/clusterHostInfo/zookeeper_server_hosts', [])

    if zookeeper_port is None:
        Logger.error("Cannot get zookeeper port. Use default port 2181")
        return '2181'

    if not zookeeper_hosts:
        Logger.error("Cannot get zookeeper hosts")
        return ''

    zookeeper_port_host = map(lambda host: host + ":" + zookeeper_port, zookeeper_hosts)
    zookeeper_ensemble_str = ','.join(zookeeper_port_host)
    Logger.info("Zookeeper ensemble str: " + zookeeper_ensemble_str)
    return zookeeper_ensemble_str
