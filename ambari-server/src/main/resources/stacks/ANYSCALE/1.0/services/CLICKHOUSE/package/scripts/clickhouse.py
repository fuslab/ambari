#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import collections
import os

from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.resources.properties_file import PropertiesFile
from resource_management.libraries.resources.template_config import TemplateConfig
from resource_management.core.resources.system import Directory, Execute, File, Link
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions import format
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions import Direction

from resource_management.core.logger import Logger

def clickhouse(upgrade_type=None):
    import params
    ensure_base_directories()

    # clickhouse server all configuration, return result type dict
    clickhouse_config_template = mutable_config_dict(params.clickhouse_config_json_template)
    clickhouse_metrika_template = mutable_config_dict(params.clickhouse_metrika_json_template)
    
    effective_version = params.stack_version_formatted if upgrade_type is None else format_stack_version(params.version)
    Logger.info(format("Effective stack version: {effective_version}"))

    # listeners and advertised.listeners are only added in 2.3.0.0 onwards.
    if effective_version is not None and effective_version != "":
       clickhouse_server_host = clickhouse_config_template['interserver_http_host'] = params.hostname
       Logger.info(format("clickhouse interserver_http_host: {clickhouse_server_host}"))
    else:
       listeners = clickhouse_config_template['interserver_http_host'].replace("localhost", params.hostname)
       Logger.info(format("clickhouse interserver_http_host: {listeners}"))

    #format convert
    import clickhouse_utils

    clickhouse_config = clickhouse_utils.clickhouseConfigToXML(clickhouse_config_template)
    clickhouse_metrika = clickhouse_utils.clickhouseMetrikaToXML(params.tcp_port,params.user_admin,params.user_admin_password,params.clickhouse_hosts,params.zookeeper_hosts,params.remote_servers,params.hostname,params.zookeeper_server,clickhouse_metrika_template)
    
    Directory(params.clickhouse_log_dir,
              mode=0755,
              cd_access='a',
              owner=params.clickhouse_user,
              group=params.clickhouse_group,
              create_parents = True,
              recursive_ownership = True,
    )

    Directory(params.conf_dir,
              mode=0755,
              cd_access='a',
              owner=params.clickhouse_user,
              group=params.clickhouse_group,
              create_parents = True,
              recursive_ownership = True,
    )

    File(format("{conf_dir}/config.xml"),
                      owner=params.clickhouse_user,
                      group=params.clickhouse_group,
                      content=InlineTemplate(clickhouse_config)
    )

    File(format("{conf_dir}/metrika.xml"),
          owner=params.clickhouse_user,
          group=params.clickhouse_group,
          content=InlineTemplate(clickhouse_metrika)
     )

    File(format("{conf_dir}/users.xml"),
          owner=params.clickhouse_user,
          group=params.clickhouse_group,
          content=Template("clickhouse-users.xml.j2")
     )

    # On some OS this folder could be not exists, so we will create it before pushing there files
    Directory(params.limits_conf_dir,
              create_parents = True,
              owner='root',
              group='root'
    )

    File(os.path.join(params.limits_conf_dir, 'clickhouse.conf'),
         owner='root',
         group='root',
         mode=0644,
         content=Template("clickhouse.conf.j2")
    )

    File(os.path.join(params.bindir, 'clickhouse-manager.sh'),
         owner='root',
         group='root',
         mode=0755,
         content=Template("clickhouse-manager.sh.j2")
    )
    
    File(os.path.join(params.crondir, 'clickhouse-server'),
         owner='root',
         group='root',
         mode=0755,
         content=Template("clickhouse-server-cron.j2")
    )

def mutable_config_dict(clickhouse_config):
    clickhouse_server_config = {}
    for key, value in clickhouse_config.iteritems():
        clickhouse_server_config[key] = value
    return clickhouse_server_config

def ensure_base_directories():
  import params
  Directory([params.clickhouse_log_dir, params.clickhouse_pid_dir, params.conf_dir, params.clickhouse_data_path],
            mode=0755,
            cd_access='a',
            owner=params.clickhouse_user,
            group=params.clickhouse_group,
            create_parents = True,
            recursive_ownership = True,
            )
