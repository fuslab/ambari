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

print "------------------------------------"
print "hostname : %s %s" %(hostname, version)   # hostname : master 3.0.0.0-512
print "------------------------------------"

# default fusiondb parameters
fusiondb_user = config['configurations']['fusiondb-env']['fusiondb_user']
fusiondb_group = config['configurations']['cluster-env']['user_group']

root_user = 'root'

# fusiondb pid
fusiondb_pid_dir = status_params.fusiondb_pid_dir
fusiondb_pid_file = status_params.fusiondb_pid_file

# fusiondb log
fusiondb_log_dir = "/var/log/spark2"

# fusiondb bin
fusiondb_sbin_dir = "/opt/anyscale/current/fusiondb/sbin"

# Java Home and clickhouse_hosts
java64_home = config['ambariLevelParams']['java_home']

# zookeeper cluster configuratioins
zookeeper_hosts = config['clusterHostInfo']['zookeeper_server_hosts']
zookeeper_hosts.sort()

print "------------------------------------"
print "zookeeper configuratioins : %s %s"  %(java64_home, zookeeper_hosts) # zookeeper configuratioins : /usr/jdk64/jdk1.8.0_112 [u'master', u'node1', u'node2']
print "------------------------------------"

all_hosts = default("/clusterHostInfo/all_hosts", [])
all_racks = default("/clusterHostInfo/all_racks", [])

cluster_name = config["clusterName"]

# fusiondb-config.xml
fusiondb_config_json_template = config['configurations']['fusiondb-config']
fusiondb_port = config['configurations']['fusiondb-config']['fusiondb_port']

