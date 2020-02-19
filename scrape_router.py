from __future__ import print_function
import time, os
from kubernetes import client as k_client, config
from kubernetes.client.rest import ApiException
import pandas as pd

def get_router_logs(resource_type, resource_output_file):
    kube_client = None
    kube_v1_batch_client = None
    
    

    kubecfg_path = os.environ.get('/home/parulsingh/.kube/config')
    
    config.load_kube_config(config_file=kubecfg_path)
    kube_client = k_client.CoreV1Api()
    kube_v1_batch_client = k_client.BatchV1Api()
    print('-----------------------------',kube_client)

    # create an instance of the API class
    name = 'router-default-67c98fd99c-2bk57' # str | name of the Pod
    container = 'syslog' # str | The container for which to stream logs. Defaults to only container if there is one container in the pod. (optional)
    project = 'openshift-ingress'
    timestamps = True # bool | If true, add an RFC3339 or RFC3339Nano timestamp at the beginning of every line of log output. Defaults to false. (optional)
    log = kube_client.read_namespaced_pod_log(namespace=project, name=name, container=container, timestamps=timestamps)
    timestamp = []
    log_list = log.split('\n')
    print(len(log_list))
    for item in log_list:
        if resource_type in item:
            timestamp.append(item.split(' ')[0])
    print(len(timestamp))
    with open(resource_output_file, 'w+') as file:
        for item in timestamp:
            ts= pd.Timestamp(item)
            ts_string = str(ts)
            ts_string = ts_string.split('+')[0]
            file.write(ts_string+"\n")
            

if __name__ == "__main__":
    # resource_type = "GET /cpu"
    # resource_output_file = "cpu_timestamp"
    # get_router_logs(resource_type, resource_output_file)
    resource_type = "GET /memory"
    resource_output_file = "memory_timestamp"
    get_router_logs(resource_type, resource_output_file)