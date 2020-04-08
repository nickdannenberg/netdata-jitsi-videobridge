#!/usr/bin/env python3


from bases.FrameworkServices.UrlService import UrlService
from json import loads

ORDER = [
    'overview',
    #"conferences",
    #"participants",
    #"largest_conference",
    #"audiochannels",
    #"videochannels",
    #"videostreams",

    'bitrate',
    #"bit_rate_download",
    #"bit_rate_upload",

    'packetrate',
    #"packet_rate_download",
    #"packet_rate_upload",
    #"loss_rate_download",
    #"loss_rate_upload",
    # not shown, old: "rtp_loss",

    'rtt',
    #"rtt_aggregate",

    'conference_events',
    # "total_conferences_completed",
    # "total_conferences_created",
    # "total_failed_conferences",
    # "total_partially_failed_conferences",

    'participant_problems',
    # "total_loss_controlled_participant_seconds",
    # "total_loss_degraded_participant_seconds",
    # "total_loss_limited_participant_seconds",

    'connections_created',
    # "total_tcp_connections",
    # "total_udp_connections",

    "threads",

    # not shown:
    # not shown, experimental: #"jitter_aggregate",
    # "cpu_usage",
    # "used_memory",
    # "conference_sizes",
    # "graceful_shutdown",
    # "total_bytes_received",
    # "total_bytes_received_octo",
    # "total_bytes_sent",
    # "total_bytes_sent_octo",
    # "total_channels",
    # "total_colibri_web_socket_messages_received",
    # "total_colibri_web_socket_messages_sent",
    # "total_conference_seconds",
    # "total_data_channel_messages_received",
    # "total_data_channel_messages_sent",
    # "total_memory",
    # "total_no_payload_channels",
    # "total_no_transport_channels",
    # "total_packets_received",
    # "total_packets_received_octo",
    # "total_packets_sent",
    # "total_packets_sent_octo",

]

# chart options: type.id name title units [family [context [charttype [priority [update_every [options [plugin [module]]]]]]]]
# data point options: id name algo (absolute, incremental, pct-of-abs, pct-of-incr) multi, divisor
CHARTS = {

    'overview': {
        'options': [ None,
                     'Current conferences, participants and streams on the video bridge',
                     'count', 'jvb_overview', 'jvb.overview',
                     'lines'
        ],
        'lines': [
            ["audiochannels"],
            ["videochannels"],
            ["videostreams"],
            ["conferences"],
            ["participants"],
            ["largest_conference"]
        ],
    },
    'bitrate': {
        'options': [ None,
                     'Total incoming and outgoing bitrate for the video bridge',
                     'kbit/s', 'bitrate', 'bitrate', 'lines'
        ],
        'lines': [
            [ 'bit_rate_download', 'received' ],
            [ 'bit_rate_upload', 'sent' ],
        ]
    },
    'packetrate': {
        'options': [ None,
                     'incoming and outgoing packet rate and lost packets for the video bridge',
                     'pps', 'packetrate', 'packetrate', 'lines'
        ],
        'lines': [
            ['packet_rate_download', 'received'],
            ['packet_rate_upload', 'sent'],
            ['loss_rate_download', 'lost_received'],
            ['loss_rate_upload', 'lost_sent']
        ]
    },

    'rtt': {
        'options': [ None,
                     'An average value of the RTT across all streams.',
                     'ms', 'rtt', 'rtt', 'lines'
        ],
        'lines': [
            ['rtt_aggregate', 'rtt']
        ]
    },

    'participant_problems': {
        'options': [ None, 'Changes in loss-controlled, loss-limited and loss-degraded participant-seconds',
                     'seconds', 'participant_problems','participant_problems', 'lines'
        ],
        'lines': [
            ['total_loss_controlled_participant_seconds', 'loss_controlled', 'incremental'],
            ['total_loss_limited_participant_seconds', 'loss_limited', 'incremental'],
            ['total_loss_degraded_participant_seconds', 'loss_degraded', 'incremental'],
        ]
    },

    'conference_events': {
        'options': [ None,
                     'Creation and completion of conferences',
                     'count', 'conference_events', 'conference_events', 'lines'
        ],
        'lines': [
            ['total_conferences_completed', 'completed', 'incremental'],
            ['total_conferences_created', 'created', 'incremental'],
            ['total_failed_conferences', 'failed', 'incremental'],
            ['total_partially_failed_conferences', 'partially_failed', 'incremental']
        ]
    },

    'connections_created': {
        'options': [ None,
                     'Creation of tcp and udp connections',
                     'count', 'connections_created', 'connections_created', 'lines'
        ],
        'lines': [
            ["total_tcp_connections", 'tcp', 'incremental'],
            ["total_udp_connections", 'udp', 'incremental']
        ]
    },

    'threads': {
        'options': ['threads',
                    'Number of Java threads that the video bridge is using',
                    'count', 'threads', 'threads', 'lines'
        ],
        'lines': [
            ['threads']
        ]
    }
}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.url = self.configuration.get('url', 'http://localhost/colibri/stats')
        self.keys = [l[0] for i in CHARTS.values() for l in i['lines']]


    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        try:
            data = loads(self._get_raw_data())
            ret = dict([ (k, data[k]) for k in self.keys])
            # post processing of loss rate
            ret['loss_rate_download'] = ret['packet_rate_download']*ret['loss_rate_download']
            ret['loss_rate_upload'] = ret['packet_rate_upload']*ret['loss_rate_upload']
            # turn upload rates negative
            for k in self.keys:
                if k.find('upload')>-1:
                    ret[k] = -1*ret[k]
            return ret
        except (ValueError, AttributeError):
            return None
