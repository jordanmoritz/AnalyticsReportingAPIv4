#mgmt_api.py

# Management API functions
def print_accounts(account_summary):
    for account in account_summary.get('items'):
        print(f"\nAccount: {account.get('name')}")
        for prop in account.get('webProperties'):
            print(f"\tProperty: {prop.get('name')}")
            for view in prop.get('profiles'):
                print(f"\t\tView: {view.get('name')} - {view.get('id')}")

def get_account_summary(management_client, print_accounts=None):
    """
    Requires that you pass a service client built on management API
    If you specify print_accounts=True, will log out account structure from account_summary object
    """
    account_summary = management_client.management().accountSummaries().list().execute()
    
    if print_accounts:
        print_accounts(account_summary)
    
    return account_summary

def get_view_ids(account_summary, account_name=None, prop_name=None):
# At some point make this searchable if user already knows account/prop name/id 
    view_ids = []    
    for account in account_summary.get('items'):
        for prop in account.get('webProperties'):
            for view in prop.get('profiles'):
                view_ids.append({"view_name": f"{account.get('name')} > {prop.get('name')} > {view.get('name')}",
                                 "view_id": view.get('id')})

    return view_ids

def get_segments(management_client, print_segments=None):
    segments = management_client.management().segments().list().execute()
    
    if print_segments:
        print_segment_names(segments)
    
    return segments

def print_segment_names(segments):
    for segment in segments.get('items'):
        print(f"{segment.get('name')} = {segment.get('segmentId')}")

def get_segment_ids(segment_name, segments):
    segment_ids = []
    for segment in segments.get('items'):
        if segment.get('name') == segment_name:
            segment_ids.append(segment.get('segmentId'))

    return segment_ids
        
def print_segment_def(segments, segment_id=None, segment_name=None):
    
    if segment_id:
        for segment in segments.get('items'):
            if segment.get('segmentId') == segment_id:
                print(f"{segment.get('name')}, {segment.get('segmentId')} = {segment.get('definition')}")
    
    elif segment_name:
        for segment in segments.get('items'):
            if segment.get('name') == segment_name:
                print(f"{segment.get('name')}, {segment.get('segmentId')} = {segment.get('definition')}")