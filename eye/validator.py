'''Validator Class for all sorts of validation'''
from datetime import datetime as dt

class Validator():

    def __init__(self, what_to_validate, data):
        self.errmsg = ''
        self.data = data
        self.valid_or_not = False
        self.dt_obj = 0
        if (what_to_validate == 'timestamp'):
            self._time_validator()
        if (what_to_validate == 'future'):
            self._future_time_validator()
        if (what_to_validate == 'keys_no_more_no_less'):
            self.input = data[0]
            self.required_keys = data[1]
            self._keys_no_more_no_less()  

    def _time_validator(self):
        data = self.data
        
        valid_time_format = \
            ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"]
        ''' If users send invalid format, send them the text below as examples '''
        valid_time_format_text = \
            ["YYYY-MM-DD", "YYYY-MM-DD HH:MM:SS", "YYYY-MM-DD HH:MM:SS.xxx"]

        for x in valid_time_format:
            try:
                self.dt_obj = dt.strptime(data, x)    # if invalid exception will be raised and caught below
                self.valid_or_not = True
            except:
                self.errmsg = f'**INVALID DATETIME FORMAT - {data}*** '
                self.errmsg += f'Acceptable format : {valid_time_format_text}'

    def _keys_no_more_no_less(self):
        input = self.input
        required_keys = self.required_keys
        self.missing_keys = [x for x in required_keys if x not in input]
        self.extraneous_keys = [x for x in input if x not in required_keys]

    def get_missing_and_extraneous_keys(self):
        return self.missing_keys, self.extraneous_keys

    def _future_time_validator(self):
        self.future_or_not = self.data > dt.now()  

    def get_timestamp_obj(self):
        return self.dt_obj

    def is_it_future(self):
        return self.future_or_not

    def is_it_valid(self):
        return self.valid_or_not

    def get_error_message(self):
        return self.errmsg
