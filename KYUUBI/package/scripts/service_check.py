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
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import \
    check_process_status
from kyuubi_utils import get_kyuubi_server_pid_file_path


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        pid_file = get_kyuubi_server_pid_file_path()
        check_process_status(pid_file)


if __name__ == "__main__":
    ServiceCheck().execute()
