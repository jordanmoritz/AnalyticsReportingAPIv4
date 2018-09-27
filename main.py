#main.py

#ENHANCEMENTS
# Add dimension filter option to request builder functions
# Create functions for outputting data to sources

#MODULES
import configparser
from analytics_reporting_api import gen_util_funcs
from analytics_reporting_api import mgmt_api
from analytics_reporting_api import reporting_api

#CONFIG
config_parser.read('config.ini')

#Service account details
scopes = config_parser.get('Service Account', 'scopes').split(',')
service_credentials_file = config_parser.get('Service Account', 'service_credentials_file')

#Account details from management API
management_client = get_service_client(scopes, 'analytics', 'v3', service_credentials_file)
account_summary = get_account_summary(management_client, print_accounts=False)
view_ids = get_view_ids(account_summary)
segments = get_segments(management_client, print_segments=False)

#Report parameters
start_date = config_parser.get('Report Parameters', 'start_date')
end_date = config_parser.get('Report Parameters', 'end_date')

direct_segment_id = get_segment_ids('Direct Traffic', segments)
view_id = view_ids[3].get('view_id')
segment = direct_segment_id[0]

data_requests = [
    {'metrics': ['sessions', 'pageviews'],
     'dimensions': ['country', 'browser']},
    {'metrics': ['sessions', 'pageviews', 'bounces'],
     'dimensions': ['fullReferrer', 'country', 'browser']}]

#SCRIPT
reporting_client = get_service_client(scopes, 'analyticsreporting', 'v4', service_credentials_file)
request_body = build_request_body(data_requests)
request_parameters = build_request_parameters(view_id, start_date, end_date, segment=segment)
response_data = get_analytics_data(reporting_client, request_parameters, request_body)
analytics_df = response_to_dataframe(response_data)

for df in analytics_df:
    df.columns = clean_strings(df.columns, clean_operations)

analytics_df[1]