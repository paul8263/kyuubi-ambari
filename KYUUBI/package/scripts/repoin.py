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
import commands
import os


# Tools for retrieving HDP Repository URL

def _has_yum():
    return os.path.exists("/etc/yum.conf")


def _get_base_url_from_config():
    try:
        from resource_management.libraries.script.script import Script
        from resource_management.libraries.functions.default import default
        from resource_management.core.logger import Logger

        config = Script.get_config()
        repositories = config['repositoryFile']['repositories']
        stack_name = default("/clusterLevelParams/stack_name", None)
        stack_name_uppercase = stack_name.upper()
        baseurl = None

        Logger.info("repositories: {0}".format(repositories))
        for repo in repositories:
            if repo['repoName'] == stack_name_uppercase:
                baseurl = repo['baseUrl']
                Logger.info("baseUrl: {0}".format(baseurl))
        return baseurl
    except Exception:
        return None


def _get_colon_separated_value(s):
    start_pos = s.find(":") + 1
    return s[start_pos:].strip()


def _get_base_url_from_yum():
    if not _has_yum():
        print("Yum is not available")
        return None

    package_name = "zookeeper"
    repo_line = commands.getoutput("yum --disablerepo '*' --enablerepo  'HD*' info {} 2>/dev/null | grep 'Repo'".format(package_name))
    repo_name = _get_colon_separated_value(repo_line)
    if repo_name == "":
        print("ERROR: Cannot find repo for {}".format(package_name))
        return None

    print("Repo name: {}".format(repo_name))
    baseurl_line = commands.getoutput("yum repolist {} -v | grep baseurl".format(repo_name))
    baseurl = _get_colon_separated_value(baseurl_line)
    print("Base URL: {}".format(baseurl))
    return baseurl


def get_base_url():
    return _get_base_url_from_config() or _get_base_url_from_yum()
