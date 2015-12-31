# -*- coding: utf-8 -*-


class Kaonashi(object):

    """Kaonashi interface"""

    def __init__(self):
        self.prot = 8080
        self.host = 'localhost'

    def greeting(self, name):
        """just greeting 5 times"""
        for i in range(5):
            print("hello, " + name)

kaonashi = Kaonashi()
