'''
Created on Dec 13, 2016

@author: BangDoan
'''
from vocollect_core.task.task import TaskBase
from vocollect_core.dialog.functions import prompt_only

REQUEST_STOCK = 'requestBacekStock'
QUANTITY_PROMPT = 'quantityPrompt'

class BackStockTask(TaskBase):
    def __init__(self, location, taskRunner = None, callingTask = None):
        super(BackStockTask, self).__init__(taskRunner, callingTask)
        
        self.name = 'taskQuery'
        self._location = location
        
    def initializeStates(self):
        self.addState(REQUEST_STOCK, self.request_stock)
        self.addState(QUANTITY_PROMPT, self.quantity_prompt)
        
    def request_stock(self):
        self._quantity = '456'
    
    def quantity_prompt(self):
        prompt_only('there are ' + str(self._quantity) + ' items in back stock')