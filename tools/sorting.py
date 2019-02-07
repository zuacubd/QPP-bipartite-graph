import os
import sys
import operator


def get_descending(dc):
        '''
        get sorted the dictonary based on values in descending order
        '''
        dc_sort = sorted(dc.items(), key = operator.itemgetter(1), reverse = True)
        items = [item for item, score in dc_sort]
        return items, dc_sort


def get_ascending(dc):
        '''
        get sorted the dictonary based on values in ascending order
        '''
        dc_sort = sorted(dc.items(), key = operator.itemgetter(1), reverse = False)
        items = [item for item, score in dc_sort]
        return items, dc_sort

