'''Business logics go here'''

from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
from datetime import datetime as dt
from eye import validator

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
    
    report = "This are counts by session id"
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
        
    def get_report(self):

        input = self.input
        response = []
        text = ""
        errmsg = ""

        if (len(input) == 0):
            text = "Tell us what info you need, {Info Needed : Value}, examples : "
            response = [{"category" : "form interaction",
                        "timestamp" : ["2021-01-01 06:15:27.2","2021-01-01 08:15:27.2"]}]
            return {text : response}

        try:

            text = "Nothing found"
            key, value = list(input.items())[0]
    
            if (type(value) is str):    # session_id, category or name
                text = "Nothing found"
                response = [x for x in alldata if x[key] == value]

            elif (type(value) is list): # time range

                for timestamp_to_validate in value:
                    v = validator.Validator('timestamp', timestamp_to_validate)
                    if (v.is_it_valid() == False): 
                        errmsg = v.get_error_message()
                        raise Exception()

                start_time = dt.strptime(value[0], "%Y-%m-%d %H:%M:%S.%f")
                end_time = dt.strptime(value[1], "%Y-%m-%d %H:%M:%S.%f")
                ''' No need to validate these time because already done when users sent them'''

                response = [x for x in alldata if 
                    dt.strptime(x['timestamp'],"%Y-%m-%d %H:%M:%S.%f")  >= start_time
                    and dt.strptime(x['timestamp'],"%Y-%m-%d %H:%M:%S.%f") <= end_time]
            else:
                errmsg = f"**INVALID INPUT : {input}"
                raise Exception()

            if (len(response) > 0) :
                text = f'The report you requested - {key} of value {value} : '                       

        except:
            return(errmsg)

        return {text : response}

@api_view(['GET', 'POST'])
def report(request, format=None):

    response = Report(request.data).get_report()
    return Response(response)

@api_view(['GET'])
def report_all_activities(request, format=None):

    return Response({"This are all the activities : " : alldata})

def validate(input):
    errmsg = ''
    required_fields = ['session_id', 'category', 'name', 'data', 'timestamp']
    input = list(input.keys())
    v = validator.Validator('keys_no_more_no_less',[input, required_fields])
    missing_keys, extraneous_keys = v.get_missing_and_extraneous_keys()
    if (len(missing_keys) > 0 ):
        errmsg = f'**Missing required info : {missing_keys}**'
    elif (len(extraneous_keys) > 0 ):
        errmsg = f'**Unrecongized message type : {extraneous_keys}**'  

    return errmsg

'''Collect user's data and save it in cache '''
def collect_data(data):

    if len(data) :
        alldata.append(data)

@api_view(['GET', 'POST'])
def main(request, format=None):

    err = ''

    try:
        err = validate(request.data)
        if (len(err) == 0):
            collect_data(request.data) 
            response = "We got your data, thank you"
        else:
            raise Exception(err)
    except:
        if (len(err) > 0):
            response = err
        else:
            response = 'Something Wrong'

    return Response(response)