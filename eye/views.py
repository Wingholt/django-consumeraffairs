from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter

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