from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
from datetime import datetime as dt

alldata = []  # all users' input in cache

'''Count class to put into buckets according to key'''
class Count():

  def __init__(self, key):
    self.key = key

  '''Count the occurence of same key'''
  def count(self):

    self.buckets = {}
    
    name = Counter(k[self.key] for k in alldata)
    for name, count in name.most_common():
        self.buckets[name] = count

  def get_buckets(self):
    self.count()
    return self.buckets

''' Process and sort all_data by session'''
@api_view(['GET'])
def session_count(request, format=None):
    
    report = "This are counts by session"
    buckets = Count('session_id').get_buckets()

    return Response({report : buckets})

''' Process and sort all_data by category'''
@api_view(['GET'])
def category_count(request, format=None):
    
    report = "This are counts by category"
    buckets = Count('category').get_buckets()

    return Response({report : buckets})

''' Process and sort all_data by name'''
@api_view(['GET'])
def name_count(request, format=None):
    
    report = "This are counts by name"
    buckets = Count('name').get_buckets()

    return Response({report : buckets})    

'''Get report for specific type and value'''
class Report():
    def __init__(self, input):
        self.input = input
        #self.validate()

    def get_report(self):

        input = self.input
        response = []
        text = "Nothing found"

        if (len(input) > 0):
            key, value = list(input.items())[0]
    
        '''session_id, category or name'''
        if (len(input) > 0 and type(value) is str):

            response = [x for x in alldata if x[key] == value]

        '''time range'''
        if (len(input) > 0 and type(value) is list):

            start_time = dt.strptime(value[0], "%Y-%m-%d %H:%M:%S.%f")
            end_time = dt.strptime(value[1], "%Y-%m-%d %H:%M:%S.%f")
            #TODO validate time

            response = [x for x in alldata if 
                dt.strptime(x['timestamp'],"%Y-%m-%d %H:%M:%S.%f")  >= start_time
                and dt.strptime(x['timestamp'],"%Y-%m-%d %H:%M:%S.%f") <= end_time]

        if (len(response) > 0) :
            text = f'The report you requested - {key} of value {value} : '

        return {text : response}

@api_view(['GET', 'POST'])
def report(request, format=None):

    response = Report(request.data).get_report()
    return Response(response)

@api_view(['GET'])
def report_all_activities(request, format=None):

    return Response({"This are all the activities : " : alldata})

def validation(input):
    pass

'''Collect user's data and save it in cache '''
def collect_data(data):

    if len(data) :
        alldata.append(data)

@api_view(['GET', 'POST'])
def main(request, format=None):

    try:
        validation(request.data)
        collect_data(request.data) 
        response = "We got your data, thank you"
    except:
        response = "Something wrong..."

    return Response(response)