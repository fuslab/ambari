
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


from resource_management.core.resources.system import Execute
from resource_management.libraries.functions import format
from resource_management.libraries.functions import Direction
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger

def run_migration(env, upgrade_type):
  """
  If the acl migration script is present, then run it for either upgrade or downgrade.
  That script was introduced in JDP 2.3.4.0 and requires stopping all clickhouse server first.
  Requires configs to be present.
  :param env: Environment.
  :param upgrade_type: "rolling" or "nonrolling
  """
  pass