'''
Created on Dec 13, 2016

@author: BangDoan
'''
from vocollect_core.task.task import TaskBase
from vocollect_core.dialog.functions import prompt_ready, prompt_digits, prompt_only, prompt_yes_no
from vocollect_core.utilities import obj_factory
from BackStockTask import BackStockTask
from voice import globalwords
from vocollect_core.utilities.localization import itext
WELCOME_PROMPT = 'welcomePrompt'
REQUEST_LOCATION = 'requestLocation'
LOCATION_PROMPT = 'locationPrompt'
QUANTITY_PROMPT = 'quantityPrompt'
SEND_INVENTORY = 'sendInventory'


class MainTask(TaskBase):
    
    '''Main Task'''
    
    def __init__(self, taskRunner = None, callingTask = None):
        super(MainTask,self).__init__(taskRunner, callingTask)
        self.name = 'taskMain'
        
    def initializeStates(self):
        self.addState(WELCOME_PROMPT, self.welcome_prompt)
        self.addState(REQUEST_LOCATION, self.request_location)
        self.addState(LOCATION_PROMPT, self.location_prompt)
        self.addState(QUANTITY_PROMPT, self.quantity_prompt)
        self.addState(SEND_INVENTORY, self.send_inventory)
        
    def welcome_prompt(self):
        globalwords.words['sign off'].enabled = False
        prompt_ready(itext('main.welcome.prompt'), True)
        
    def request_location(self):
        self._location = 'location ABC'
        self._chk_digit = '123'
    
    def location_prompt(self):
        globalwords.words['sign off'].enabled = True
        op_entry = prompt_digits(itext('main.location.prompt',self._location), itext('main.location.help'),
                                3, 3, confirm=False)
        if int(self._chk_digit) != int(op_entry) :
            prompt_only(itext('main.wrong.check.digit', str(op_entry)), True)
            self.next_state = LOCATION_PROMPT
    
    def quantity_prompt(self):
        BACK_STOCK_CMD = 'back stock'
        self._bin_qty = prompt_digits('quantity?', 'speak the bin quantity or say back stock', 
                                1, 5, True, additional_vocab = {BACK_STOCK_CMD : False})
        if self._bin_qty == BACK_STOCK_CMD:
            self._bin_qty = 0
            self.launch(obj_factory.get(BackStockTask,self._location, self.taskRunner), self.current_state)
    def send_inventory(self):
        self.next_state = REQUEST_LOCATION
    
    def sign_off(self):
        if prompt_yes_no('sign off, correct?'):
            prompt_only('signing off')
            self.return_to(self.name, WELCOME_PROMPT)
        else: 
            globalwords.words['sign off'].enabled = True
            
        