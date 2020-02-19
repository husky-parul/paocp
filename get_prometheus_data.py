from prometheus_api_client import Metric, MetricsList, PrometheusConnect
from prometheus_api_client.utils import parse_datetime, parse_timedelta

import matplotlib.pyplot as plt
import pandas as pd

pc = PrometheusConnect(url="https://prometheus-k8s-openshift-monitoring.apps-crc.testing", 
                    headers={"Authorization":"bearer 7lmyVwWaTrWZYwiM0KRN30fBw5W70OkcqOMnizZ-cr0"},
                    disable_ssl=True)

start_time = parse_datetime("7d")
end_time = parse_datetime("now")
chunk_size = parse_timedelta("now", "1d")



def get_data(metrics,timestamp_filenames,datafile):
    
   
    def _getTimestamps(timestamp_filename):
        print(timestamp_filename)
        file_name = open(timestamp_filename, "r") 
        ts = file_name.readlines()
        return ts
    
    def _getMetricsData(metric):
        metric_data = pc.get_metric_range_data(metric,
                                                start_time=start_time,
                                                end_time=end_time,
                                                chunk_size=chunk_size,)
        
        metrics_object_list = MetricsList(metric_data)
        metric_object = metrics_object_list[0]
        value_list = metric_object.metric_values
        return value_list
           

    # Iterating through timestamps and converting string ts to pandas.Timestamps
    _cpu = []
    _memory = []
    _nio = []
    for metric in metrics:
        cmetric_vlist = _getMetricsData(metric)
        
        # load all the timestamps from router_log_file into list
        for ts in timestamp_filenames:
            timestamp = _getTimestamps(ts)
            for item in timestamp:
                ts= pd.Timestamp(item.split(' /')[0])
                df1 = cmetric_vlist[cmetric_vlist['ds'] >= ts]
                # print("*************** ",df1)
                for index, row in df1.head(1).iterrows():
                    if "cpu" in metric:
                        _cpu.append(str(ts)+"\t"+str(row['y'])+ "\t"+item.split(' /')[1])

                    elif "memory" in metric:
                        _memory.append(str(ts)+"\t"+str(row['y'])+ "\t"+item.split(' /')[1])

                    elif "container_network" in metric:
                        _nio.append(str(ts)+"\t"+str(row['y'])+ "\t"+item.split(' /')[1])
    # print(_cpu[0])
    # print(len(_cpu))
    # print(len(_memory))
    # print(len(_nio))
    # print(_nio[200])
    # print(_memory[200])

    # with open("datasets/cpu_data", "w+") as df:
    #     for index in range(215):
    #         df.write(_cpu[index].split("\t")[1] + _cpu[index].split("\t")[2])
    
    # with open("datasets/memory_data", "w+") as df:
    #     for index in range(215):
    #         df.write(_memory[index].split("\t")[1] + _memory[index].split("\t")[2])

    # with open("datasets/nio_data", "w+") as df:
    #     for index in range(215):
    #         df.write(_nio[index].split("\t")[1] + _nio[index].split("\t")[2])
            

    
    with open(datafile, "w+") as df:
        for index in range(len(_cpu)):
            print(index,_cpu[index])
            df.write(_cpu[index].split("\t")[1] + ","+_memory[index].split("\t")[1] + "," + _nio[index].split("\t")[1] + "," +_cpu[index].split("\t")[2])
            

   

    
    

def general(metric_name):
    metric_data = pc.get_metric_range_data(metric_name,
    start_time=start_time,
    end_time=end_time,
    chunk_size=chunk_size,)

    metrics_object_list = MetricsList(metric_data)
    metric_object = metrics_object_list[0]
    value_list = metric_object.metric_values
    print(value_list)


if __name__ == "__main__":
    # metric_name = 'container_cpu_system_seconds_total{namespace="openshift" ,pod="openshift-python-flask-1-bwdjt",  container="openshift-python-flask"}'
    # resource_type = 'memory_datafile_2'
    # resource_timestamp_filename = 'memory_timestamp'
    # get_data(metric_name,resource_type,resource_timestamp_filename, "/memory    cpu")

    container_metrics = ['container_cpu_system_seconds_total{namespace="openshift" ,pod="openshift-python-flask-1-bwdjt",  container="openshift-python-flask"}',
                    'container_memory_usage_bytes{namespace="openshift" ,pod="openshift-python-flask-1-bwdjt",  container="openshift-python-flask"}',
                    'container_network_transmit_bytes_total{namespace="openshift" ,pod="openshift-python-flask-1-bwdjt",  container="POD"}'
                    ]
    
    node_metrics = ['cluster:capacity_cpu_cores:sum',
                    'cluster:capacity_memory_bytes:sum',
                    'sum(node_network_transmit_bytes_total)']

    timestamp_filenames = ['datasets/cpu_timestamp','datasets/memory_timestamp']
    datafile = 'datasets/data'

    get_data(container_metrics,timestamp_filenames,datafile)


