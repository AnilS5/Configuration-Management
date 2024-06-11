import os
import sys
import re
import shutil
import fileinput
from datetime import datetime

class port_check():
    def __init__(self, ports):
        self.ports = ports

    def ports_check(self):
        globals()['servers'] = filter(lambda ser: re.findall('\d+.\d+.\d+', ser), self.ports)
        globals()['port_range'] = filter(lambda por: por not in servers, self.ports)
        if len(port_range) % len(servers) == 0:
            port_count = len(port_range) / len(servers)
            globals()['server_port'] = map(lambda por: dict(zip(servers[por:],[port_range[por*port_count:(por*port_count)+port_count]])), range(len(servers)))
        
        master = ''
        slave = ''
        for ser_por in server_port:
            for key, value in ser_por.items():                
                master = master + key + ':' + value[0] + ' '              
                slave = slave + key + ':' + value[1] + ' '
        masters = master.split()
        slaves = slave.split()
        slaves.append(slaves[0])
        del slaves[0]
        vars_main = 'vars/main.yml'
        ri_b = r'{{'
        lf_b = r'}}'
        with open(vars_main, 'r') as file:            
            red_fi = file.readlines()
            red_pa = re.compile('(.*)#\sredis$')
            
            try:
                red_ma = filter(lambda r: red_pa.findall(r), red_fi)
                red_no = filter(lambda r: r not in red_ma, red_fi)
                red_or = open(vars_main, 'wt')
                for l in red_no:
                    if l != '\n':
                       red_or.write(l)                    
                red_or.close()
            
            finally:
                with open(vars_main, 'a') as file:
                    file.write('ports: # redis\n')           
                    for p in range(len(port_range)/port_count):
                        file.write('  {}:  {} # redis\n'.format(p,port_range[p*port_count:(p*port_count)+port_count]))
                    file.write('portdirs: # redis\n')
                    for d in range(len(port_range)/port_count):
                        file.write('  {0}: "{1} ports.{0}[item|int] {2}" # redis\n'.format(d, ri_b, lf_b))
                    file.write('redis_logs_dirs: # redis\n')                   
                    for p in range(len(port_range)/port_count):
                        file.write('  {0}: "{1} dirs_path[2] {2}/{1} portdirs.{0} {2}/redis-server-{1} env {2}-m1-{1} portdirs.{0} {2}-logs" # redis\n'.format(p, ri_b, lf_b))
                    file.write('redis_pid_dirs: # redis\n')
                    for q in range(len(port_range)/port_count):
                        file.write('  {0}: "{1} dirs_path[2] {2}/{1} portdirs.{0} {2}/redis-server-{1} env {2}-m1-{1} portdirs.{0} {2}" # redis\n'.format(q, ri_b, lf_b)) 
        
                    file.write('\nmaster: "{}" # redis\n\nslave: "{}" # redis\n'.format(master,slave))
                    for s in range(len(slaves)):
                        file.write('masters{0}: "{1} {2}" # redis\n'.format(s, slaves[s], masters[s]))
                        
                         
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
        or_file = shutil.copyfile(inventory_path, 'hosts')
        # Zookeper group verification.
        with open('hosts', 'r') as file:
            text = file.readlines()
            pattern = re.compile('(.*)redi\w+(.*)(.*)|^\d+.{3}(.*)anisble(.*)#redis$')
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
                    file.write('[redis]\n')
                    for hosts in servers:
                        file.write(hosts + ' ansible_connection=ssh ansible_ssh_user=user ansible_ssh_pass=pass ansible_become_pass=pass ' +' #redis' + '\n' )
       
        with open('templates/lines.txt') as file:
             lines = file.read()
        vailue=''

        fi_in = open('templates/test.yml', 'rt')
        fi_ou = open('tasks/main.yml', 'wt')
        for line in fi_in:
            text = re.search('#Redis', line)
            if text:
                for i in range(len(servers)):
                    fi_ou.write(line.replace('#Redis', lines.format(i, ri_b, lf_b, (len(servers)))))
            else:
                fi_ou.write(line)

        fi_in.close()
        fi_ou.close()
     
        with open('templates/line.txt') as file:
             line = file.read()
        vailue1=''

        f_ou = open('tasks/cluster.yml', 'wt')
        for i in range(len(servers)):
            f_ou.write(line.format(i, ri_b, lf_b, (len(servers))) + '\n')

        f_ou.close()        

D = port_check(sys.argv[1:])
D.ports_check()
