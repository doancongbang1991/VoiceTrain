'''
Created on Dec 14, 2016

@author: BangDoan
'''
from voice import get_voice_application_property
import time

#import LUT ODR

from vocollect_lut_odr.connections import LutConnection, OdrConnection
from vocollect_lut_odr.receivers import Lut, OdrConfirmationByte
from vocollect_lut_odr.transports import TransientSocketTransport

class InventoryOdr(object):
    def __init__(self):
        #create transport
        self._transport = TransientSocketTransport(
                        str(get_voice_application_property('ODRHost')),
                        int(get_voice_application_property('ODRPort')))
        self._formatter = RecordFormatter('')
        self._connection = OdrConnection('Inventory', self._transport,self._formatter, OdrConfirmationByte())
         
    def send(self, command, *fields):
        #save the command
        self._formatter.command_name = command
        #have value for fields
        field_list = [x if x is not None else '' for x in fields]
        #send odr
        self._connection.append(field_list)
        
class RecordFormatter(object):
    
    def __init__(self, command):
        self.command_name = command
        self._record_seperator = '\r\n'
        self._record_set_terminator = '\n'
    
    def format_record(self, fields):
        ''' Format the record's fields, and terminate with a record separator '''
        from voice import getenv
        
        data = [self.command_name, time.strftime("%m-%d-%y %H:%M:%S"), 
                getenv('Device.Id', ''),
                getenv('Operator.Id', '')]
        data.extend([str(field) for field in fields])
        request = ",".join(data)     
        
        return request + self._record_seperator
    
    
    def terminate_recordset(self):
        #return end of record
        return self._record_set_terminator
    
    
    
    
    