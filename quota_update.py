import qumulo
import datetime
import json
import os
import logging
import pathlib
import json
from qumulo.rest_client import RestClient

# Logging Details
logging.basicConfig(filename='quota_update.log', level=logging.INFO,
    format='%(asctime)s,%(levelname)s,%(message)s')

# Read credentials
json_file = open('credentials.json','r')
json_data = json_file.read()
json_object = json.loads(json_data)

# Parse cluster credentials
cluster_address = json_object['cluster_address']
port_number = json_object['port_number']
username = json_object['username']
password = json_object['password']

# Connect to the cluster
rc = RestClient(cluster_address, port_number)
rc.login(username, password)
logging.info('Connection established with {}'.format(cluster_address))

quota=list(rc.quota.get_all_quotas_with_status(page_size=1000))[0]['quotas']
print(range(len(quota)))
 
for x in range(len(quota)):
    file_id = quota[x]['id']
    capacity_usage = quota[x]['capacity_usage']
    new_quota=int(float(capacity_usage)*1.5)
    rc.quota.update_quota(file_id, new_quota)
#    file_path = rc.fs.resolve_paths([file_id])[0]['path']
#    logging.info('Quota values were updated from {} to {} for {}'.format(capacity_usage,new_quota,file_path))
