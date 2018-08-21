from __future__ import print_function

import sys
sys.path.append('C:\Users\Ram Asokan\Desktop\Highgard\Scripts\facebook_business\Lib\site-packages')
sys.path.append('C:\Users\Ram Asokan\Desktop\Highgard\Scripts\facebook_business\Lib\site-packages\facebook_business-3.0.3.dist-info')

from facebook_business.exceptions import FacebookRequestError
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

## authentication and initialization
my_app_id = '1699903186946001'
my_app_secret = '9d5909a2e9c23f3d923dcb2fc37257ff'
my_access_token = 'EAAYKDY2cR9EBAFtxD0q4lJE9emHZAUC0gzFcZCpJqP0ZBm5Cqtm1JGzbZCDIlIMY0ezGc6kdqJKhSlnEOWHHBfYYusFWCZAmdZACYgiKvG1vWdrSS4nS6WukgqxQNWZAHnCoSVWPxS6SRGxOo7A6PcQC1hQCJ4cYadxbRcmCo1gnAZDZD'

FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_654678324709162')
campaigns = my_account.get_campaigns()
print(campaigns)
