import requests


class HTTP:
    """Reformat HTTP response
    """

    @staticmethod
    def get(url, return_json=True):
        """Reformat HTTP `get` response into text or json

        :param url: URL link to get HTTP response
        :type url: string
        :param return_json: if the returned results \
        json format or not, defaults to Ture
        :type return_json: boolean
        :return: return formatted HTTP response
        :rtype: json format or string

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
