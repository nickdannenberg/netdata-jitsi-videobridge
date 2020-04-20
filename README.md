# Netdata Jitsi Monitoring

This netdata plugin monitors jicofo and jitsi video bridge stats
through their privtae REST API. The JVB stats contain more detailled
call- and network-related stats, while jicofo monitors all bridges in
a cluster and also collects information about bridge-selection
decisions (currently not collected by this tool).

The default config monitors the JVB instance on localhost via
`http://localhost:8080/colibri/stats`. The Jicofo instance monitored
is `http://localhost:8888/stats`. After installation, use `edit-config
python.d/jvb.conf` or `edit-config python.d/jicofo.conf` to configure
the stats-URL, multiple instances or other parameters.

## Installation

Copy `jvb.chart.py`/`jicofo.chart.py` to
`/usr/libexec/netdata/python.d/` and `jvb.conf`/`jicofo.conf` to
`/usr/lib/netdata/conf.d/python.d/`.
