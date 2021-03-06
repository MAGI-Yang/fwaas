#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from oslo_config import cfg
from oslo_service import service

from neutron.agent.common import config
from neutron.agent.l3 import ha
from neutron.agent.linux import external_process
from neutron.agent.linux import interface
from neutron.agent.linux import pd
from neutron.agent.linux import ra
from neutron.agent.metadata import config as metadata_config
from neutron.common import config as common_config
from neutron.common import topics
from neutron.conf.agent.l3 import config as l3_config
from neutron import service as neutron_service


FWAAS_AGENT = (
    'neutron_fwaas.services.firewall.agents.'
    'l3reference.firewall_l3_agent.L3WithFWaaS'
)


def register_opts(conf):
    conf.register_opts(l3_config.OPTS)
    conf.register_opts(metadata_config.DRIVER_OPTS)
    conf.register_opts(metadata_config.SHARED_OPTS)
    conf.register_opts(ha.OPTS)
    config.register_interface_driver_opts_helper(conf)
    config.register_agent_state_opts_helper(conf)
    conf.register_opts(interface.OPTS)
    conf.register_opts(external_process.OPTS)
    conf.register_opts(pd.OPTS)
    conf.register_opts(ra.OPTS)
    config.register_availability_zone_opts_helper(conf)


def main(manager=FWAAS_AGENT):
    register_opts(cfg.CONF)
    common_config.init(sys.argv[1:])
    config.setup_logging()
    server = neutron_service.Service.create(
        binary='neutron-l3-agent',
        topic=topics.L3_AGENT,
        report_interval=cfg.CONF.AGENT.report_interval,
        manager=manager)
    service.launch(cfg.CONF, server).wait()
