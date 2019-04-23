from base import helper
from base import baseData

not_namespaced = [baseData.base_resource, 'namespace', 'node']
resource_list = helper.get_all_resource()

helper.delete_namespace_without_warning()
for resource in resource_list:
    helper.post_parent(resource)
    helper.check_all_method(resource)
    if resource not in not_namespaced:
        helper.delete_namespace()
