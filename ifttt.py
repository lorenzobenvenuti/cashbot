import requests

class IftttClient(object):

    _url_template = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

    def __init__(self, key):
        self._key = key

    def trigger(self, event, *args):
        if len(args) > 3:
            raise ValueError('Cannot send more than three values')
        body = { 'value{}'.format(i + 1): args[i] for i in range(len(args)) }
        r = requests.post(
            IftttClient._url_template.format(event, self._key),
            json=body,
            verify=False
        )
        return r.status_code
