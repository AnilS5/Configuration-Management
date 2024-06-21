# Configuration Management:

Configuration managment is project built to setup and configure three nodes **Redis** master-client cluster, and **Kafka, Zookeper** broker-consumer cluster.

## Usage and prerequisites:
Python 2.9+
Ansible 2.9+

**Usage** 
###### Setup and configure three nodes Kafka Zookeeper cluster
**python kafka.py supplied with server ports along ansible inventory path**

The initial run of kafka.py supplied with server_ips and ports arguments is must, to prepare variables required for setup and configuration of broker-consumer using Ansible.

Once after generation of variables file for the kafka.py calls Ansible role **kafka** to make ready Kafka-zookeeper cluster available to use.


###### Setup and configuration of Zookeeper
**python zookeeper.py supplied with server_ip ports argument is must to prepare inventory file.**

###### Setup and cinfiguration Redis
**python py.py supplied with 6 server_ips and 6 ports is must to prepare inventory file along with variables required for setup and configuration of Redis master-client cluster.**

The pairs of server:port will be created as below Server1-Port2, Server2-Port3 and Server3-Port1.

|Server 1|Server 2|Server 3|
|--------|--------|--------|
| Port 1 | Port 2 | Port 3 |
