# Kyuubi Ambari integration

This project enables Ambari to setup Kyuubi cluster.

# Environment

* OS: CentOS/Redhat
* Ambari: 2.7.5
* HDP: 3.0.1.0.187
* Kyuubi: 1.9.1

# How to use

You might change kyuubi_download_url, KYUUBI_TAR_NAME, KYUUBI_DIR_NAME and STACK_VERSION in `params.py` in order to keep them capable with your environment.

Copy `KYUUBI` folder to `/var/lib/ambari-server/resources/stacks/HD/{stack_version}/services` folder in Ambari Server host and then restart Ambari Server.

Then clean the cache of all Ambari Agent by running the following:

```shell
rm -rf /var/lib/ambari-agent/cache/*
ambari-agent restart
```

# Author

Paul Zhang
