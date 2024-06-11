import os
import sys
import re
import shutil
from datetime import datetime

class zookeeper_config():
    def __init__(self, inventory):
        self.inventory = inventory

    def host_entry(self):
          
        # Copy inventory file.
        with open('/etc/ansible/ansible.cfg', 'r') as file:
    	    inv_path= file.readlines()
            inv_compile = re.compile('(.*)\s=\s/etc/ansible/hosts$')
            inv_str = filter(lambda j: inv_compile.findall(j), inv_path)
    	    if not inv_str[0].startswith('#'):
                inventory_path = inv_strt[0].split('=')[2]
            else:
                inventory_path = '/etc/ansible/hosts'

        inventory_path = '/etc/ansible/hosts'
        d = datetime.today()
        today = d.strftime('%d%b%Y')
        #or_file = shutil.copyfile(inventory_path, inventory_path + '_' + today)
        or_file = shutil.copyfile(inventory_path, 'hosts')
        # Kafka group verification.
        with open('/etc/ansible/roles/kafka/hosts', 'r') as file:
            text = file.readlines()
            pattern = re.compile('(.*)kaf\w+(.*)(.*)|^\d+.{3}(.*)anisble(.*)#kafka$')
            try:
                globals()['text1'] = filter(lambda j: pattern.findall(j), text)
                text = filter(lambda j: j not in text1, text)
                src_out = open(inventory_path, 'wt')
                for l in text:
                    src_out.write(l)
                src_out.close()

            finally:            
                #Prepare inventory for zookeeper remote servers group.
                with open(inventory_path, 'a') as file:
                    file.write('[kafka]\n')
                    for hosts in self.inventory:
                        file.write(hosts + ' ansible_connection=ssh ansible_ssh_user=<user> ansible_ssh_pass=<password> ansible_become_pass=<password>' +' #kafka' + '\n' )

zoo_keep = zookeeper_config(sys.argv[1:])
zoo_keep.host_entry()
