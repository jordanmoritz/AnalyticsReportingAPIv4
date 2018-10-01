#reporting_api.py
import pandas as pd

def build_request_parameters(view_id, start_date, end_date, sampling_level=None, segment=None, cohorts=None):
    # Will need to update this once we get around to adding cohorts, and advanced segments etc.
    request_parameters = {'dateRanges': [{'startDate': start_date,
                                          'endDate': end_date}],
                          'viewId': view_id}
    
    if sampling_level:
        request_parameters.update({'samplingLevel': sampling_level})
    
    # This works for one segment, but will require its own function for multiple
    elif segment:
        request_parameters.update({'segments': [
            {'segmentId': segment}
        ]})
        
    return request_parameters

def build_request_body(data_requests):
    
    request_body = {'reportRequests': []}
    for request in data_requests:
        
        formatted_request = {'metrics': [],
                            'dimensions': []}
        
        for metric in request.get('metrics'):
            formatted_request['metrics'].append({'expression': 'ga:'+ metric})
        
        for dimension in request.get('dimensions'):
            formatted_request['dimensions'].append({'name': 'ga:'+ dimension})
            
        request_body['reportRequests'].append(formatted_request)
    
    return request_body

def get_analytics_data(reporting_client, request_parameters, request_body):
    """
    Has bandaid built in to handle request_body formatting when segments are defined in request_parameters
    """
    for request in request_body['reportRequests']:
        request.update(request_parameters)
        
        if request_parameters.get('segments'):
            request.get('dimensions').append({'name': 'ga:segment'})

    response_data = reporting_client.reports().batchGet(
        body=request_body
        ).execute()

    return response_data

def response_to_dataframe(response_data):
    
    data_frames = []
    
    # Yank out the meta data for each report
    for report in response_data.get('reports', []):
        headers = report.get('columnHeader', {})
        dimension_headers = headers.get('dimensions', [])
        metric_details = headers.get('metricHeader', {}).get('metricHeaderEntries', [])
        
        # Run through to grab metric headers
        metric_headers = []
        for metric in metric_details:
            metric_headers.append(metric.get('name'))
        
        # Pull dimension headers and metric headers together
        column_headers = tuple(dimension_headers + metric_headers)
        
        # For each report, yank out the actual data values
        rows_list = []
        for row in report.get('data').get('rows'):
            
            # Creates a tuple for each row of raw data
            row_data = []
            for dim_value in row.get('dimensions'):
                row_data.append(dim_value)

            for metric_value in row.get('metrics')[0].get('values'):
                row_data.append(metric_value)

            rows_list.append(tuple(row_data))

        # Build a data frame out of the data and append to list for multiple reports
        df = pd.DataFrame(rows_list, columns=column_headers)
        data_frames.append(df)
    
    return data_frames