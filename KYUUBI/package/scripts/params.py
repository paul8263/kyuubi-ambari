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
# from resource_management.core.logger import Logger
from kyuubi_utils import get_zookeeper_ensemble_str
import commands
import os
import repoin
import socket

# Package & env configuration

KYUUBI_TAR_NAME = 'apache-kyuubi-1.9.1-bin.tgz'
KYUUBI_DIR_NAME = 'apache-kyuubi-1.9.1-bin'
STACK_VERSION = '3.0.1.0-187'

# Whether Kyuubi locates in aux or HDP basic package
AUX_ENABLED = True

config = Script.get_config()

stack_root = Script.get_stack_root()

kyuubi_installation_path = os.path.join(stack_root, STACK_VERSION, 'kyuubi')
KYUUBI_HOME = os.path.join(kyuubi_installation_path, KYUUBI_DIR_NAME)

kyuubi_defaults = config['configurations']['kyuubi-defaults']

if AUX_ENABLED:
    download_url_from_aux = commands.getoutput('cat /etc/yum.repos.d/aux.repo | grep "baseurl" | head -1 | awk -F= \'{print $2"/kyuubi/' + KYUUBI_TAR_NAME + '"}\'')
    kyuubi_download_url = download_url_from_aux if kyuubi_defaults['kyuubi_download_url'] == 'DOWNLOAD_PROM_REPO' else kyuubi_defaults['kyuubi_download_url']
else:
    kyuubi_download_url = os.path.join(repoin.get_base_url(), 'kyuubi', KYUUBI_TAR_NAME) if kyuubi_defaults['kyuubi_download_url'] == 'DOWNLOAD_PROM_REPO' else kyuubi_defaults['kyuubi_download_url']

# Kyuubi user

kyuubi_user = kyuubi_defaults['kyuubi_user']
kyuubi_group = kyuubi_defaults['kyuubi_group']

# kyuubi IP port

kyuubi_frontend_bind_host = kyuubi_defaults['kyuubi_frontend_bind_host']
kyuubi_frontend_protocols = kyuubi_defaults['kyuubi_frontend_protocols']
kyuubi_frontend_thrift_binary_bind_port = kyuubi_defaults['kyuubi_frontend_thrift_binary_bind_port']
kyuubi_frontend_rest_bind_port = kyuubi_defaults['kyuubi_frontend_rest_bind_port']

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
if kyuubi_frontend_bind_host == 'USE_HOST_IP':
    kyuubi_frontend_bind_host = ip

# Kyuubi High Availability

kyuubi_ha_client_class = kyuubi_defaults['kyuubi_ha_client_class']
kyuubi_ha_addresses = kyuubi_defaults['kyuubi_ha_addresses']

# If kyuubi ha client is set to zookeeper while kyuubi ha addresses are unset, get the existing zookeeper ensemble
if 'zookeeper' in kyuubi_ha_client_class.lower() and kyuubi_ha_addresses == 'USE_CLUSTER_ZOOKEEPER':
    kyuubi_ha_addresses = get_zookeeper_ensemble_str()

kyuubi_ha_namespace = kyuubi_defaults['kyuubi_ha_namespace']
kyuubi_ha_zookeeper_auth_type = kyuubi_defaults['kyuubi_ha_zookeeper_auth_type']
kyuubi_ha_zookeeper_auth_principal = kyuubi_defaults['kyuubi_ha_zookeeper_auth_principal']
kyuubi_ha_zookeeper_auth_keytab = kyuubi_defaults['kyuubi_ha_zookeeper_auth_keytab']

# Kyuubi authentication

kyuubi_authentication = kyuubi_defaults['kyuubi_authentication']
kyuubi_kinit_principal = kyuubi_defaults['kyuubi_kinit_principal']
kyuubi_kinit_keytab = kyuubi_defaults['kyuubi_kinit_keytab']

# Kyuubi engine share level

kyuubi_engine_share_level = kyuubi_defaults['kyuubi_engine_share_level']

# Kyuubi engine type

kyuubi_engine_type = kyuubi_defaults['kyuubi_engine_type']

# Kyuubi spark master

spark_master = kyuubi_defaults['spark_master']

# spark yarn queue

spark_yarn_queue = kyuubi_defaults['spark_yarn_queue']

# Custom properties

custom_properties = kyuubi_defaults['kyuubi_custom_properties']

# kyuubi env

kyuubi_env = config['configurations']['kyuubi-env']['content']

# Kyuubi log4j2

kyuubi_log4j2 = config['configurations']['kyuubi-log4j2']['content']
