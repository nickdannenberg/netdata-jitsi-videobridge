# JVB

This netdata plugin monitors jitsi video bridge stats through their COLIBRI API.

The default config monitors the JVB instance on localhost via
`http://localhost/colibri/stats`. After installation, use `edit-config
python.d/jvb.conf` to configure the stats-URL, multiple instances or
other parameters.

## Installation

Copy `jvb.chart.py` to `/usr/libexec/netdata/python.d/` and copy
`jvb.conf` to `/usr/lib/netdata/conf.d/python.d/`.
