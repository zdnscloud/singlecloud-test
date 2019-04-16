import os
import time

while True:
    os.system('kubectl --kubeconfig=/Users/tanxu/kube_config_cluster.yml apply -f /Users/tanxu/logtest.yaml')
    time.sleep(5)
    os.system('kubectl --kubeconfig=/Users/tanxu/kube_config_cluster.yml delete -f /Users/tanxu/logtest.yaml')
    time.sleep(5)
