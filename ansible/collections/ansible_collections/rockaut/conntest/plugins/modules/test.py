
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

import ansible_collections.rockaut.conntest.plugins.module_utils.helpers as helpers

def main():
  ptvsd.wait_for_attach()
  ptvsd.break_into_debugger()
  module = AnsibleModule(argument_spec=[], supports_check_mode=False)
  module.exit_json(changed=False, state="present", msg="All done!")


if __name__ == '__main__':
    main()
