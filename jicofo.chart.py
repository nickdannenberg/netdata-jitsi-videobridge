#!/usr/bin/env python3


from bases.FrameworkServices.UrlService import UrlService
from json import loads

ORDER = [
    'overview',
    #"conferences",
    #"participants",
    #"largest_conference",
    #"recording_active",

    'bridges',
    #"operational_bridge_count",
    #"bridge_count",

    'conference_sizes',
    #empty, 1, 2, 3,...21+

]

# chart options: type.id name title units [family [context [charttype [priority [update_every [options [plugin [module]]]]]]]]
# data point options: id name algo (absolute, incremental, pct-of-abs, pct-of-incr) multi, divisor
CHARTS = {

    'overview': {
        'options': [ None,
                     'Current conferences, participants and streams on all video bridges',
                     'count', 'jicofo_overview', 'jicofo.overview',
                     'lines'
        ],
        'lines': [
            ["conferences"],
            ["participants"],
            ["largest_conference"],
            # ['recording_active'],
        ],
    },
    'bridges': {
        'options': [ None,
                     'Number of video bridges',
                     'count', 'brigdes', 'bridges', 'lines'
        ],
        'lines': [
            [ 'operational_bridge_count', 'available' ],
            [ 'bridge_count', 'total' ],
        ]
    },
    'conference_sizes': {
        'options': [ None,
                     'Conference size distribution',
                     'size', 'conference_sizes', 'conference_sizes', 'lines'
        ],
        'lines': [
             ['0_to_1', '0 to 1'],
             ['1_to_2', '1 to 2'],
             ['2_to_3', '2 to 3'],
             ['3_to_5', '3 to 5'],
             ['5_to_10', '5 to 10'],
             ['10_to_20', '10 to 20'],
             ['20_to_50', '20 to 50'],
             ['50_to_100', '50 to 100'],
             ['100_to_200', '100 to 200'],
             ['200_to_300', '200 to 300'],
             ['300_to_400', '300 to 400'],
             ['400_to_500', '400 to 500'],
             ['500_to_max', '500 to max'],
        ]
    },

}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.url = self.configuration.get('url', 'http://localhost:8888/stats')
        self.keys = [l[0] for i in CHARTS.values() if 'lines' in i for l in i['lines']]


    def _get_data(self):
        """
        Format data received from http request
        :return: dict
        """
        try:
            data = loads(self._get_raw_data())
            ret = dict([(k, data[k]) for k in self.keys if k in data])
            # conference_sizes
            c = data['conference_sizes']['buckets']
            for i in c:
              ret[i]=c[i]
            # bridges
            ret['operational_bridge_count'] = data['bridge_selector']['operational_bridge_count']
            ret['bridge_count'] = data['bridge_selector']['bridge_count']
            return ret
        except (ValueError, AttributeError):
            return None
