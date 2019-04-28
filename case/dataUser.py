from base import helper
from base import baseData

token_prefix = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'

user = 'user-test'
password = 'zdns'
new_password = 'zdns1'

extra_namespace = 'namespace-extra'

user_collection_url = baseData.base_url + '/users'
user_url = user_collection_url + '/' + user
project = [{"cluster": baseData.cluster, "namespace": baseData.test_namespace}]

create_user = {
    "name": user,
    "password": helper.encrypt_password(password),
    "projects": project
}

login_url = user_url + '?action=login'
reset_password_url = user_url + '?action=resetPassword'

update_user = {
    "projects": [{"cluster": baseData.cluster, "namespace": extra_namespace}]
}

namespace_collection_url = helper.get_collection_url('namespace')

deployment_url_test = namespace_collection_url + '/' + baseData.test_namespace + '/deployments'
deployment_url_extra = namespace_collection_url + '/' + extra_namespace + '/deployments'

reset_password = {
    "oldPassword": helper.encrypt_password(password),
    "newPassword": helper.encrypt_password(new_password)
}

multi_namespace = [
    {"cluster": baseData.cluster, "namespace": baseData.test_namespace},
    {"cluster": baseData.cluster, "namespace": extra_namespace}
]
create_user_with_multi_namespace = {
    "name": user,
    "password": helper.encrypt_password(password),
    "projects": multi_namespace
}

create_user_with_all_namespace = {
    "name": user,
    "password": helper.encrypt_password(password),
    "projects": [{"cluster": baseData.cluster, "namespace": '_all'}]
}

cluster_collection_url = helper.get_collection_url('cluster')

admin_and_normal_user = [baseData.admin_user, user]
normal_user = [user]

all_cluster = [baseData.cluster, baseData.extra_cluster]
extra_cluster = [baseData.extra_cluster]

namespace_least_count = 2
