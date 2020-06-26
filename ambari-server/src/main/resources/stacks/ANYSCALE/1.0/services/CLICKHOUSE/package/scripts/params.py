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
import os
from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.get_stack_version import get_stack_version
from resource_management.libraries.functions.is_empty import is_empty
import status_params
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
import utils

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()
stack_name = default("/clusterLevelParams/stack_name", None)

stack_version_unformatted = str(config['clusterLevelParams']['stack_version'])
stack_version_formatted = format_stack_version(stack_version_unformatted)

print "------------------------------------"
print "server configuratioins : %s %s" %(stack_root, stack_name) 
print "------------------------------------"

# Version being upgraded/downgraded to
version = str(config['clusterLevelParams']['stack_version'])

hostname = config['agentLevelParams']['hostname']

bindir='/usr/bin'

crondir='/etc/cron.d'

print "------------------------------------"
print "hostname : %s %s" %(hostname, version)   # hostname : master 3.0.0.0-512
print "------------------------------------"

# default clickhouse parameters
clickhouse_bin = '/usr/bin/clickhouse-manager.sh'
conf_dir = "/etc/clickhouse-server/conf"
limits_conf_dir = "/etc/security/limits.d"

clickhouse_user_nofile_soft = config['configurations']['clickhouse-env']['clickhouse_user_nofile_soft']
clickhouse_user_nofile_hard = config['configurations']['clickhouse-env']['clickhouse_user_nofile_hard']
clickhouse_user = config['configurations']['clickhouse-env']['clickhouse_user']
clickhouse_group = config['configurations']['cluster-env']['user_group']

root_user = 'root'

clickhouse_pid_dir = status_params.clickhouse_pid_dir
clickhouse_pid_file = clickhouse_pid_dir+"/clickhouse-server.pid"

clickhouse_managed_pid_dir = "/var/run/clickhouse-server"
clickhouse_managed_log_dir = "/var/log/clickhouse-server"

# clickhouse log configuratioins
clickhouse_log_dir = config['configurations']['clickhouse-env']['clickhouse_log_dir']
clickhouse_log_level = default('/configurations/clickhouse-env/clickhouse_log_level','trace')

clickhouse_log_file = default('/configurations/clickhouse-env/clickhouse_log_file',clickhouse_log_dir+'/server.log')
clickhouse_errorlog_file = default('/configurations/clickhouse-env/clickhouse_errorlog_file',clickhouse_log_dir+'/error.log')

clickhouse_log_size = default('/configurations/clickhouse-env/clickhouse_log_size','1000M')
clickhouse_log_count = default('/configurations/clickhouse-env/clickhouse_log_count',10)

# Java Home and clickhouse_hosts
java64_home = config['ambariLevelParams']['java_home']

# clickhouse cluster configurations
clickhouse_hosts = config['clusterHostInfo']['clickhouse_hosts']
clickhouse_hosts.sort()
remote_servers = config['configurations']['clickhouse-config']['remote_servers']

print "------------------------------------"
print "clickhouse configuratioins : %s %s"  %(java64_home,clickhouse_hosts) # clickhouse configuratioins : /usr/jdk64/jdk1.8.0_112 [u'master', u'node1', u'node2']
print "------------------------------------"

# zookeeper cluster configuratioins
zookeeper_server = config['configurations']['clickhouse-config']['zookeeper']
zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()

print "------------------------------------"
print "zookeeper configuratioins : %s %s"  %(java64_home, zookeeper_hosts) # zookeeper configuratioins : /usr/jdk64/jdk1.8.0_112 [u'master', u'node1', u'node2']
print "------------------------------------"

all_hosts = default("/clusterHostInfo/all_hosts", [])
all_racks = default("/clusterHostInfo/all_racks", [])

cluster_name = config["clusterName"]

# clickhouse-config.xml
clickhouse_config_json_template = config['configurations']['clickhouse-config']
tcp_port = config['configurations']['clickhouse-config']['tcp_port']
users_config = config['configurations']['clickhouse-config']['users_config']
clickhouse_data_path = config['configurations']['clickhouse-config']['path']

# clickhouse-metrika cluster configurations
clickhouse_metrika_json_template = config['configurations']['clickhouse-metrika']

# clickhouse-user configurations
clickhouse_users_json_template = config['configurations']['clickhouse-users']['clickhouse_users']

user_admin = config['configurations']['clickhouse-users']['user_admin']

user_admin_password = config['configurations']['clickhouse-users']['user_admin_password']
user_admin_password_sha256 = utils.sha256_checksum(user_admin_password)

user_ck = config['configurations']['clickhouse-users']['user_ck']

user_ck_password = config['configurations']['clickhouse-users']['user_ck_password']
user_ck_password_sha256 = utils.sha256_checksum(user_ck_password)
