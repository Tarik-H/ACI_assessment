#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: aci_bd
short_description: Manage Bridge Domains (BD) objects (fv:BD)
description:
- Manages Bridge Domains (BD) on Cisco ACI fabrics.
notes:
- The C(tenant) used must exist before using this module in your playbook.
  The M(aci_tenant) module can be used for this.
- More information about the internal APIC class B(fv:BD) from
  L(the APIC Management Information Model reference,https://developer.cisco.com/docs/apic-mim-ref/).
author:
- Jacob McGill (@jmcgill298)
version_added: '2.4'
options:
  arp_flooding:
    description:
    - Determines if the Bridge Domain should flood ARP traffic.
    - The APIC defaults new Bridge Domains to C(no).
    type: bool
    default: 'no'
  bd:
    description:
    - The name of the Bridge Domain.
    aliases: [ bd_name, name ]
  bd_type:
    description:
    - The type of traffic on the Bridge Domain.
    - The APIC defaults new Bridge Domains to C(ethernet).
    choices: [ ethernet, fc ]
    default: ethernet
  description:
    description:
    - Description for the Bridge Domain.
  enable_multicast:
    description:
    - Determines if PIM is enabled
    - The APIC defaults new Bridge Domains to C(no).
    type: bool
    default: 'no'
  enable_routing:
    description:
    - Determines if IP forwarding should be allowed.
    - The APIC defaults new Bridge Domains to C(yes).
    type: bool
    default: 'yes'
  endpoint_clear:
    description:
    - Clears all End Points in all Leaves when C(yes).
    - The APIC defaults new Bridge Domains to C(no).
    - The value is not reset to disabled once End Points have been cleared; that requires a second task.
    type: bool
    default: 'no'
  endpoint_move_detect:
    description:
    - Determines if GARP should be enabled to detect when End Points move.
    - The APIC defaults new Bridge Domains to C(garp).
    choices: [ default, garp ]
    default: garp
  endpoint_retention_action:
   description:
   - Determines if the Bridge Domain should inherit or resolve the End Point Retention Policy.
   - The APIC defaults new Bridge Domain to End Point Retention Policies to C(resolve).
   choices: [ inherit, resolve ]
   default: resolve
  endpoint_retention_policy:
    description:
    - The name of the End Point Retention Policy the Bridge Domain should use when
      overriding the default End Point Retention Policy.
  igmp_snoop_policy:
    description:
    - The name of the IGMP Snooping Policy the Bridge Domain should use when
      overriding the default IGMP Snooping Policy.
  ip_learning:
    description:
    - Determines if the Bridge Domain should learn End Point IPs.
    - The APIC defaults new Bridge Domains to C(yes).
    type: bool
  ipv6_nd_policy:
    description:
    - The name of the IPv6 Neighbor Discovery Policy the Bridge Domain should use when
      overridding the default IPV6 ND Policy.
  l2_unknown_unicast:
    description:
    - Determines what forwarding method to use for unknown l2 destinations.
    - The APIC defaults new Bridge domains to C(proxy).
    choices: [ proxy, flood ]
    default: proxy
  l3_unknown_multicast:
    description:
    - Determines the forwarding method to use for unknown multicast destinations.
    - The APCI defaults new Bridge Domains to C(flood).
    choices: [ flood, opt-flood ]
    default: flood
  limit_ip_learn:
    description:
    - Determines if the BD should limit IP learning to only subnets owned by the Bridge Domain.
    - The APIC defaults new Bridge Domains to C(yes).
    type: bool
    default: 'yes'
  mac_address:
    description:
    - The MAC Address to assign to the C(bd) instead of using the default.
    default: 00:22:BD:F8:19:FF
    aliases: [ mac ]
    version_added: '2.5'
  multi_dest:
    description:
    - Determines the forwarding method for L2 multicast, broadcast, and link layer traffic.
    - The APIC defaults new Bridge Domains to C(bd-flood).
    choices: [ bd-flood, drop, encap-flood ]
    default: bd-flood
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    choices: [ absent, present, query ]
    default: present
  tenant:
    description:
    - The name of the Tenant.
    aliases: [ tenant_name ]
  vrf:
    description:
    - The name of the VRF.
    aliases: [ vrf_name ]
extends_documentation_fragment: aci
'''

EXAMPLES = r'''
- name: Add Bridge Domain
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: no
    state: present
    tenant: prod
    bd: web_servers
    mac_address: 00:22:BD:F8:19:FE
    vrf: prod_vrf

- name: Add an FC Bridge Domain
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: no
    state: present
    tenant: prod
    bd: storage
    bd_type: fc
    vrf: fc_vrf
    enable_routing: no

- name: Modify a Bridge Domain
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: yes
    state: present
    tenant: prod
    bd: web_servers
    arp_flooding: yes
    l2_unknown_unicast: flood

- name: Query All Bridge Domains
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: yes
    state: query

- name: Query a Bridge Domain
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: yes
    state: query
    tenant: prod
    bd: web_servers

- name: Delete a Bridge Domain
  aci_bd:
    host: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    validate_certs: yes
    state: absent
    tenant: prod
    bd: web_servers
'''

RETURN = r'''
current:
  description: The existing configuration from the APIC after the module has finished
  returned: success
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production environment",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
error:
  description: The error information as returned from the APIC
  returned: failure
  type: dict
  sample:
    {
        "code": "122",
        "text": "unknown managed object class foo"
    }
raw:
  description: The raw output returned by the APIC REST API (xml or json)
  returned: parse error
  type: string
  sample: '<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1"><error code="122" text="unknown managed object class foo"/></imdata>'
sent:
  description: The actual/minimal configuration pushed to the APIC
  returned: info
  type: list
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment"
            }
        }
    }
previous:
  description: The original configuration from the APIC before the module has started
  returned: info
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
proposed:
  description: The assembled configuration from the user-provided parameters
  returned: info
  type: dict
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment",
                "name": "production"
            }
        }
    }
filter_string:
  description: The filter string used for the request
  returned: failure or debug
  type: string
  sample: ?rsp-prop-include=config-only
method:
  description: The HTTP method used for the request to the APIC
  returned: failure or debug
  type: string
  sample: POST
response:
  description: The HTTP response from the APIC
  returned: failure or debug
  type: string
  sample: OK (30 bytes)
status:
  description: The HTTP status from the APIC
  returned: failure or debug
  type: int
  sample: 200
url:
  description: The HTTP url used for the request to the APIC
  returned: failure or debug
  type: string
  sample: https://10.11.12.13/api/mo/uni/tn-production.json
'''

from ansible.module_utils.network.aci.aci import ACIModule, aci_argument_spec
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(
        arp_flooding=dict(type='bool'),
        bd=dict(type='str', aliases=['bd_name', 'name']),  # Not required for querying all objects
        bd_type=dict(type='str', choices=['ethernet', 'fc']),
        description=dict(type='str'),
        enable_multicast=dict(type='bool'),
        enable_routing=dict(type='bool'),
        endpoint_clear=dict(type='bool'),
        endpoint_move_detect=dict(type='str', choices=['default', 'garp']),
        endpoint_retention_action=dict(type='str', choices=['inherit', 'resolve']),
        endpoint_retention_policy=dict(type='str'),
        igmp_snoop_policy=dict(type='str'),
        ip_learning=dict(type='bool'),
        ipv6_nd_policy=dict(type='str'),
        l2_unknown_unicast=dict(choices=['proxy', 'flood']),
        l3_unknown_multicast=dict(choices=['flood', 'opt-flood']),
        limit_ip_learn=dict(type='bool'),
        mac_address=dict(type='str', aliases=['mac']),
        multi_dest=dict(choices=['bd-flood', 'drop', 'encap-flood']),
        state=dict(choices=['absent', 'present', 'query'], type='str', default='present'),
        tenant=dict(type='str', aliases=['tenant_name']),  # Not required for querying all objects
        vrf=dict(type='str', aliases=['vrf_name']),
        gateway_ip=dict(type='str', removed_in_version='2.4'),  # Deprecated starting from v2.4
        scope=dict(type='str', removed_in_version='2.4'),  # Deprecated starting from v2.4
        subnet_mask=dict(type='str', removed_in_version='2.4'),  # Deprecated starting from v2.4
        method=dict(type='str', choices=['delete', 'get', 'post'], aliases=['action'], removed_in_version='2.6'),  # Deprecated starting from v2.6
        protocol=dict(type='str', removed_in_version='2.6'),  # Deprecated in v2.6
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['bd', 'tenant']],
            ['state', 'present', ['bd', 'tenant']],
        ],
    )

    aci = ACIModule(module)

    arp_flooding = aci.boolean(module.params['arp_flooding'])
    bd = module.params['bd']
    bd_type = module.params['bd_type']
    if bd_type == 'ethernet':
        # ethernet type is represented as regular, but that is not clear to the users
        bd_type = 'regular'
    description = module.params['description']
    enable_multicast = aci.boolean(module.params['enable_multicast'])
    enable_routing = aci.boolean(module.params['enable_routing'])
    endpoint_clear = aci.boolean(module.params['endpoint_clear'])
    endpoint_move_detect = module.params['endpoint_move_detect']
    if endpoint_move_detect == 'default':
        # the ACI default setting is an empty string, but that is not a good input value
        endpoint_move_detect = ''
    endpoint_retention_action = module.params['endpoint_retention_action']
    endpoint_retention_policy = module.params['endpoint_retention_policy']
    igmp_snoop_policy = module.params['igmp_snoop_policy']
    ip_learning = aci.boolean(module.params['ip_learning'])
    ipv6_nd_policy = module.params['ipv6_nd_policy']
    l2_unknown_unicast = module.params['l2_unknown_unicast']
    l3_unknown_multicast = module.params['l3_unknown_multicast']
    limit_ip_learn = aci.boolean(module.params['limit_ip_learn'])
    mac_address = module.params['mac_address']
    multi_dest = module.params['multi_dest']
    state = module.params['state']
    tenant = module.params['tenant']
    vrf = module.params['vrf']

    # Give warning when fvSubnet parameters are passed as those have been moved to the aci_subnet module
    if module.params['gateway_ip'] or module.params['subnet_mask'] or module.params['scope']:
        module._warnings = ["The support for managing Subnets has been moved to its own module, aci_subnet. \
                            The new modules still supports 'gateway_ip' and 'subnet_mask' along with more features"]

    aci.construct_url(
        root_class=dict(
            aci_class='fvTenant',
            aci_rn='tn-{0}'.format(tenant),
            filter_target='eq(fvTenant.name, "{0}")'.format(tenant),
            module_object=tenant,
            target_filter={'name': tenant},
        ),
        subclass_1=dict(
            aci_class='fvBD',
            aci_rn='BD-{0}'.format(bd),
            filter_target='eq(fvBD.name, "{0}")'.format(bd),
            module_object=bd,
            target_filter={'name': bd},
        ),
        child_classes=['fvRsCtx', 'fvRsIgmpsn', 'fvRsBDToNdP', 'fvRsBdToEpRet', 'fvSubnet'],
    )

    aci.get_existing()

    if state == 'present':
        aci.payload(
            aci_class='fvBD',
            class_config=dict(
                arpFlood=arp_flooding,
                descr=description,
                epClear=endpoint_clear,
                epMoveDetectMode=endpoint_move_detect,
                ipLearning=ip_learning,
                limitIpLearnToSubnets=limit_ip_learn,
                mac=mac_address,
                mcastAllow=enable_multicast,
                multiDstPktAct=multi_dest,
                name=bd,
                type=bd_type,
                unicastRoute=enable_routing,
                unkMacUcastAct=l2_unknown_unicast,
                unkMcastAct=l3_unknown_multicast,
            ),
            child_configs=[
                {'fvRsCtx': {'attributes': {'tnFvCtxName': vrf}}},
                {'fvRsIgmpsn': {'attributes': {'tnIgmpSnoopPolName': igmp_snoop_policy}}},
                {'fvRsBDToNdP': {'attributes': {'tnNdIfPolName': ipv6_nd_policy}}},
                {'fvRsBdToEpRet': {'attributes': {'resolveAct': endpoint_retention_action, 'tnFvEpRetPolName': endpoint_retention_policy}}},
            ],
        )

        aci.get_diff(aci_class='fvBD')

        aci.post_config()

    elif state == 'absent':
        aci.delete_config()

    aci.exit_json()


if __name__ == "__main__":
    main()
