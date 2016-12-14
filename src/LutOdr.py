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

class InventoryLut(object):
    def __init__(self, command, *field):
        #create transport
        self._transport = TransientSocketTransport(
                        str(get_voice_application_property('LUTHost')),
                        int(get_voice_application_property('LUTPort')))
        #define LUT
        self._connection = LutConnection(self._transport,
                                         RecordFormatter(command),
                                         Lut(*field))
        
    def send(self, *fields):
        field_list = [x if x is not None else '' for x in fields]
        error = -1
        try:
            self._connection.append(field_list)
            #check every 20ms, beep every 2s
            start = time.clock()
            while not self._connection.data_ready():
                time.sleep(0.02)
                now = time.clock()
                if now - start > 2:
                    start = now
                    import voice
                    voice.audio.beep(400, 0.2)
            error = 0
        except Exception:
            pass
        return error
    def get_data(self):
        return self._connection.lut_data 
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
    
    
    
    
    