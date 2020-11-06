import requests


class HTTP:
    """ Reformat HTTP response """
    @staticmethod
    def get(url, return_json=True):
        """Reformat `get` response.

        :param url: URl parameter passing to `get` method
        :type url: string
        :param return_json: if returned format is json, defaults to `True`
        :type return_json: boolean
        :return: HTTP response result in json or text
        :type: string or json format
        """
        r = requests.get(url)
        if r.status_code != 200:
            if return_json:
                return r.json()
            else:
                return ''
        else:
            if return_json:
                return r.json()
            else:
                return r.text
