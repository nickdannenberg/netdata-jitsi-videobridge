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
                     'size', 'conference_sizes', 'conference_sizes', 'stacked'
        ],
        'lines': [
            ['1participant', '1'],
            ['2participant', '2'],
            ['3participant', '3'],
            ['4participant', '4'],
            ['5participant', '5'],
            ['6participant', '6'],
            ['7participant', '7'],
            ['8participant', '8'],
            ['9participant', '9'],
            ['10participant', '10'],
            ['11participant', '11'],
            ['12participant', '12'],
            ['13participant', '13'],
            ['14participant', '14'],
            ['15participant', '15'],
            ['16participant', '16'],
            ['17participant', '17'],
            ['18participant', '18'],
            ['19participant', '19'],
            ['20participant', '20'],
            ['21participant', '21+'],
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
            c = data['conference_sizes']
            some = False
            for i in range( 1, min( len(c), 22)):
                if c[i]>0:
                    some = True
                    ret[str(i)+'participant'] = c[i]
            if not(some): # return empty record for this graph
                ret['1participant'] = 0
            # bridges
            ret['operational_bridge_count'] = data['bridge_selector']['operational_bridge_count']
            ret['bridge_count'] = data['bridge_selector']['bridge_count']
            return ret
        except (ValueError, AttributeError):
            return None
