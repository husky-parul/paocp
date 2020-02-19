# importing the requests library 
import requests 
import time
from prometheus_api_client import Metric, MetricsList, PrometheusConnect
from prometheus_api_client.utils import parse_datetime, parse_timedelta
import matplotlib.pyplot as plt
  
baseurl = 'http://openshift-python-flask-openshift.apps-crc.testing'
def hello():
    # api-endpoint 
    URL = "http://openshift-python-flask-prophet.apps-crc.testing/"
    for i in range(10):
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 
        # extracting data in json format 
        data = r.json() 
        print(r.status_code)

def pinglotsofcpu():
    URL = baseurl+"/cpu"
    for i in range(100):
        t1 = time.time()
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 
        # extracting data in json format 
        data = r.json() 
        t2 = time.time()
        print(r.status_code)
        print(data)
        print("Time taken: ", t2-t1)
        time.sleep(10)


def pinglotsofmemory():
    URL = baseurl+"/memory"
    for i in range(100):
        t1 = time.time()
        # sending get request and saving the response as response object 
        r = requests.get(url = URL) 
        # extracting data in json format 
        data = r.json() 
        t2 = time.time()
        print(r.status_code)
        print(data)
        print("Time taken: ", t2-t1)
        time.sleep(10)

def pro():
    pc = PrometheusConnect(url="https://prometheus-k8s-openshift-monitoring.apps-crc.testing", 
                    headers={"Authorization":"bearer BSI2W0euoJWYRAvT0ZnSJVmgNQ87pl3o3yXuyy38qAg"},
                    disable_ssl=True)
    up_metric = MetricsList(pc.get_current_metric_value(metric_name="haproxy_backend_up{exported_namespace='prophet'}"))
    print(up_metric[0])

    
        
if __name__ == "__main__":
    pinglotsofcpu()
    pinglotsofmemory()
    # pro()

    