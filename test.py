import mock_catalyst
from mock_catalyst import EndOfApplication
from main import main
try:
    main()

except EndOfApplication:
    print('Application ended')