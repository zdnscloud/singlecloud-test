from base import system

test_path = system.TEST_PATH

resource_path = '/Users/tanxu/tmp/singlecloud/docs/resources'
base_url = 'http://10.0.0.33:30000/apis/zcloud.cn/v1'
agent_base_url = 'http://10.0.0.33:30001/apis/agent.zcloud.cn/v1'

delimiter = '/'
base_resource = 'cluster'
cluster = 'chengdu'
extra_cluster = 'vagrant'
test_namespace = 'namespace-test'
node_master = 'master'
resource_name_suffix = '-test'

token_path = test_path + 'var/token'

admin_user = 'admin'
admin_password = 'zdns'

status_ok = 200
status_created = 201
status_no_content = 204
status_general_error = 422
status_forbidden = 403
