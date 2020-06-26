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
from resource_management import Script
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, File
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import Direction
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.show_logs import show_logs
from clickhouse import ensure_base_directories

from clickhouse import clickhouse

class ClickhouseServer(Script):

  def install(self, env):
    import params
    self.install_packages(env)
    Logger.info(format("Install clickhouse server success"))

  def configure(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    clickhouse(upgrade_type=upgrade_type)
    Logger.info(format("Configure clickhouse server success"))

  def start(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    self.configure(env, upgrade_type=upgrade_type)
    
    daemon_cmd = format('{params.clickhouse_bin} start')
    no_op_test = format('ls {params.clickhouse_pid_file} >/dev/null 2>&1 && ps -p `cat {params.clickhouse_pid_file}` >/dev/null 2>&1')
    try:
      Execute(daemon_cmd,
              user=params.root_user,
              not_if=no_op_test
      )
    except:
      show_logs(params.clickhouse_log_dir, params.root_user)
      raise

    Logger.info(format("Start clickhouse server success"))

  def stop(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    # clickhouse stop flowing
    ensure_base_directories()
    daemon_cmd = format('{params.clickhouse_bin} stop')
    try:
      Execute(daemon_cmd,
              user=params.root_user,
      )
    except:
      show_logs(params.clickhouse_log_dir, params.root_user)
      raise
    File(params.clickhouse_pid_file,
          action = "delete"
    )

    Logger.info(format("stop clickhosue server success"))
    

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.clickhouse_pid_file)
    
  def get_log_folder(self):
    import params
    return params.clickhouse_log_dir
  
  def get_user(self):
    import params
    return params.clickhouse_user

if __name__ == "__main__":
  ClickhouseServer().execute()
