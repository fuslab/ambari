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
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.validate import call_and_match_output
from resource_management.core.resources.system import Execute
from resource_management.libraries.functions.format import format
from resource_management.core.logger import Logger
from resource_management.core import sudo

class ServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

    # TODO, ClickHouse Service check should be more robust , It should get all the broker_hosts
    # Produce some messages and check if consumer reads same no.of messages.
    
    clickhouse_hosts_config = self.read_clickhouse_config()

    create_local_table = 'CREATE TABLE ambari_clickhouse_service_check_local (FlightDate Date,Year UInt16) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192)'
    create_all_table = 'CREATE TABLE ambari_clickhouse_service_check_all AS ambari_clickhouse_service_check_local ENGINE = Distributed(ck_cluster, default, ambari_clickhouse_service_check_local, rand())'

    # delete all node table
    for host in clickhouse_hosts_config:
      table_list_sql = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q 'show tables' ")
      
      import os

      table_list = os.popen(table_list_sql).read().split("\n")

      if 'ambari_clickhouse_service_check_local' in table_list:
        drop_table_sql_local = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q 'drop table ambari_clickhouse_service_check_local' ")
        Logger.info("Running clickhouse-client drop table {host} command: %s" % drop_table_sql_local)
        
        Execute(
        drop_table_sql_local,
        user=params.clickhouse_user,
        timeout=900,
        logoutput=True)

      if 'ambari_clickhouse_service_check_all' in table_list:
        drop_table_sql_all = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q 'drop table ambari_clickhouse_service_check_all' ")
        Logger.info("Running clickhouse-client drop table  {host} command: %s" % drop_table_sql_all)
        
        Execute(
        drop_table_sql_all,
        user=params.clickhouse_user,
        timeout=900,
        logoutput=True)

    # create table for all node
    for host in clickhouse_hosts_config:

      create_sql_cmd_local = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q '{create_local_table}' ")

      Execute(
        create_sql_cmd_local,
        user=params.clickhouse_user,
        timeout=900,
        logoutput=True)

      create_sql_cmd_all = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q '{create_all_table}' ")

      Execute(
        create_sql_cmd_all,
        user=params.clickhouse_user,
        timeout=900,
        logoutput=True)

      insert_sql_cmd_all = format("/usr/bin/clickhouse-client -h {host} -d default -m -u admin --password admin -q 'insert into ambari_clickhouse_service_check_local (FlightDate,Year) values(now(),toYear(now()))' ")

      Execute(
        insert_sql_cmd_all,
        user=params.clickhouse_user,
        timeout=900,
        logoutput=True)

      command = create_sql_cmd_local + ";" + create_sql_cmd_all + ";" + insert_sql_cmd_all
      Logger.info("Running clickhouse-client create and insert command: %s" % command)
    
    statistics_sql = format("/usr/bin/clickhouse-client -h 127.0.0.1 -d default -m -u admin --password admin -q 'select count(*) from ambari_clickhouse_service_check_all' ")
    
    call_and_match_output(statistics_sql, format(str(len(clickhouse_hosts_config))), "SERVICE CHECK FAILED: statistics_sql exec failed.", user=params.clickhouse_user)
    
  def read_clickhouse_config(self):
    import params
    
    clickhouse_clusters_hosts = params.clickhouse_hosts
    
    return clickhouse_clusters_hosts

if __name__ == "__main__":
    ServiceCheck().execute()
