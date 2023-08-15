# Kyuubi Ambari integration

This project enables Ambari to setup Kyuubi cluster.

# Environment

* OS: CentOS/Redhat
* Ambari: 2.7.5
* HDP: 3.0.1.0.187
* Kyuubi: 1.7.0

# How to use

Copy `KYUUBI` folder to `/var/lib/ambari-server/resources/stacks/HD/{stack_version}/services` folder in Ambari Server host and then restart Ambari Server.

Then clean the cache of all Ambari Agent by running the following:

```shell
rm -rf /var/lib/ambari-agent/cache/*
ambari-agent restart
```
