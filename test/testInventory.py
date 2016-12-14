import unittest
from vocollect_core_test.base_test_case import BaseTestCaseCore
from MainTask import MainTask, QUANTITY_PROMPT
from vocollect_core.task.task_runner import Launch
from main import Inventory
class Test(BaseTestCaseCore):
    def setUp(self):
        self._obj = MainTask(Inventory())
    def tearDown(self):
        pass
    def testRecordFormatter(self):
        from LutOdr import RecordFormatter
        f = RecordFormatter('test_command')
        r = f.format_record([1,2,3])
        rec = r.split('\r')
        self.assertEqual(rec[1], '\n')
        fields = rec[0].split(',')
        self.assertEqual(len(fields), 7)
        self.assertEqual(fields[0], 'test_command')
        self.assertEqual(fields[2], 'Device.Id')
        self.assertEqual(fields[3], 'Operator.Id')
        self.assertEqual(fields[4], '1')
        self.assertEqual(fields[5], '2')
        self.assertEqual(fields[6], '3')

    def test_qty_prompt(self):
        #post response
        self.post_dialog_responses('3!', 'no', '5!', 'yes')
        self._obj.next_state = None
        
        # run a state
        self._obj.runState(QUANTITY_PROMPT)
        
        #validate state
        self.assertEqual(self._obj.next_state, None)
        
        #validate the prompt
        self.validate_prompts('quantity?', '3, correct?','quantity?', '5, correct?' )
        
        #validate class properties
        self.assertEqual(self._obj._bin_qty, '5')
        
        
    def test_qty_backstock(self):
        #test other task
        self.post_dialog_responses('back stock')
        self._obj.next_state = None
        
        #create location
        self._obj._location = 'Location'
        
        self.assertRaises(Launch, self._obj.runState, QUANTITY_PROMPT)
        
        self.assertEqual(self._obj.next_state, None)
        self.validate_prompts('quantity?')
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()