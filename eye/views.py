from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

alldata = []

'''Collect user's data and save it '''
def collect_data(data):

    if len(data) :
        alldata.append(data)

''' Process and sort all_data by session'''
@api_view(['GET'])
def report_session(request, format=None):

    report = "This is your report by session"

    return Response(report)

''' Process and sort all_data by category'''
@api_view(['GET'])
def report_category(request, format=None):

    report = "This is your report by category"

    return Response(report)


''' Process and sort all_data by time range'''
@api_view(['GET'])
def report_time(request, format=None):

    report = "This is your report by time reange"

    return Response(report)    


@api_view(['GET'])
def report(request, format=None):

    return Response({"This is your report : " : alldata})

def validation(input):
    pass

@api_view(['GET', 'POST'])
def main(request, format=None):

    try:
        validation(request.data)
        collect_data(request.data) 
        response = "We got your data"
    except:
        response = "Something wrong..."

    return Response(response)