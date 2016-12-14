from vocollect_core.task.task_runner import TaskRunnerBase
from MainTask import MainTask
from vocollect_core.utilities import obj_factory, pickler



class Inventory(TaskRunnerBase):
	def __init__(self):
		super(Inventory, self).__init__()
		import InvGlobals
		InvGlobals.runner = self
	
	def startUp(self):
		self.launch(obj_factory.get(MainTask,self),	None)
	
	def initialize(self):
		self.app_name = 'Inventory'
		
# This is the driver function for the voice application.
def main():
	# Add additional application start-up logic here
	start = Inventory()
	start = pickler.register_pickle_obj('Inventory', start)
	start.execute()
	