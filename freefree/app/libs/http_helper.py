# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
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
