'''
Created on Dec 13, 2016

@author: BangDoan
'''
from vocollect_core.task.task import TaskBase
from vocollect_core.dialog.functions import prompt_only
from vocollect_core.utilities.localization import itext
from LutOdr import InventoryLut
from vocollect_lut_odr.receivers import StringField,NumericField


REQUEST_STOCK = 'requestBackStock'
QUANTITY_PROMPT = 'quantityPrompt'

class BackStockTask(TaskBase):
    def __init__(self, location, taskRunner = None, callingTask = None):
        super(BackStockTask, self).__init__(taskRunner, callingTask)
        
        self.name = 'taskQuery'
        self._location = location
        self._queryLut = InventoryLut('LUTBackStock',StringField('Location'),NumericField('Quantity'))
        
        
    def initializeStates(self):
        self.addState(REQUEST_STOCK, self.request_stock)
        self.addState(QUANTITY_PROMPT, self.quantity_prompt)
        
    def request_stock(self):
        if self._queryLut.send(self._location)==0:
            self._quantity = self._queryLut.get_data()[0]['Quantity']
        else:
            self.next_state = REQUEST_STOCK
    
    def quantity_prompt(self):
        prompt_only(itext('backstock.quantity', str(self._quantity)))