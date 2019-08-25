# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:53:01 2019

@author: hj823
"""
from requests import get

class Firebase():
    def __init__(self):
        self.firebase_url="https://smartmanu-af015.firebaseio.com/.json"
    def read(self):
        data = get(self.firebase_url).json()['AgvStation']
        return data
    def write(self,site,data):
        self.firebase_url.ref(site).update(data)