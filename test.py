import mock_catalyst
from mock_catalyst import EndOfApplication
from main import main
#mock_catalyst.environment_properties['SwVersion.Locale'] = 'vi_VN'
mock_catalyst.environment_properties['SwVersion.Locale'] = 'en_US'
try:
    main()

except EndOfApplication:
    print('Application ended')