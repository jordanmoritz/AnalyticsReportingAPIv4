#main.py

#ENHANCEMENTS
# Add dimension filter option to request builder functions
# Create functions for outputting data to sources

#MODULES
import configparser
import pandas as pd
from analyticsreportingapi import gen_util_funcs as util
from analyticsreportingapi import mgmt_api as mgmt
from analyticsreportingapi import reporting_api as report

#CONFIG
config_parser = configparser.ConfigParser(delimiters=('='))
config_parser.read('config.ini')

#Service account details
scopes = config_parser.get('Service Account', 'scopes').split(',')
service_credentials_file = config_parser.get('Service Account', 'service_credentials_file')

#Account details from management API
management_client = util.get_service_client(scopes, 'analytics', 'v3', service_credentials_file)
account_summary = mgmt.get_account_summary(management_client, print_accounts=False)
view_ids = mgmt.get_view_ids(account_summary)
segments = mgmt.get_segments(management_client, print_segments=False)

#Report parameters
start_date = config_parser.get('Report Parameters', 'start_date')
end_date = config_parser.get('Report Parameters', 'end_date')

direct_segment_id = mgmt.get_segment_ids('Direct Traffic', segments)
view_id = view_ids[3].get('view_id')
segment = direct_segment_id[0]

data_requests = [
    {'metrics': ['sessions', 'pageviews'],
     'dimensions': ['country', 'browser']},
    {'metrics': ['sessions', 'pageviews', 'bounces'],
     'dimensions': ['fullReferrer', 'country', 'browser']}]

#SCRIPT
reporting_client = util.get_service_client(scopes, 'analyticsreporting', 'v4', service_credentials_file)
request_body = report.build_request_body(data_requests)
request_parameters = report.build_request_parameters(view_id, start_date, end_date, segment=segment)
response_data = report.get_analytics_data(reporting_client, request_parameters, request_body)
analytics_df = report.response_to_dataframe(response_data)

for df in analytics_df:
    df.columns = util.clean_strings(df.columns, util.clean_operations)

print(analytics_df[1])