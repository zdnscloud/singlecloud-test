import json
import random
import requests
from base import baseData
from base import toolkit
import time
import os
import hashlib

int_type = ['int', 'int32', 'uint32', 'int64']
http_code = {'get': baseData.status_ok, 'post': baseData.status_created, 'put': baseData.status_ok, 'delete': baseData.status_no_content}
method_exec_order = ['post_resource', 'get_resource', 'get_collection', 'delete_resource']
namespace_check_interval = 1
not_regular_doc = ['errorcode.json', 'user.json']


def get_all_resource():
    file_list = os.listdir(baseData.resource_path)
    resource_list = []
    for file in file_list:
        if file in not_regular_doc:
            continue
        resource_list.append(file.split('.')[0])
    return resource_list


def get_resource_path(resource_type):
    return baseData.resource_path + baseData.delimiter + resource_type + '.json'


def get_resource_element(resource_type, element, resource_self=False):
    with open(get_resource_path(resource_type)) as resource_json:
        resource_dict = json.load(resource_json)
    if resource_self:
        return resource_dict
    return resource_dict[element]


def get_resource_parent(resource_type):
    return get_resource_element(resource_type, 'parentResource')


def get_collection_name(resource_type):
    return get_resource_element(resource_type, 'collectionName')


def get_resource_relation(resource_type):
    resource_relation = [resource_type]
    if resource_type == baseData.base_resource:
        return resource_relation
    while True:
        parent = get_resource_parent(resource_type)
        resource_relation.insert(0, parent)
        resource_type = parent
        if resource_type == baseData.base_resource:
            break
    return resource_relation


def resource_name(resource_type):
    if resource_type == baseData.base_resource:
        return baseData.cluster
    if resource_type == 'node':
        return baseData.node_master
    return resource_type + baseData.resource_name_suffix


def get_resource_url(resource_type):
    resource_relation = get_resource_relation(resource_type)
    resource_url = baseData.base_url
    for rr in resource_relation:
        resource_url = resource_url + baseData.delimiter + get_collection_name(rr) + baseData.delimiter + resource_name(rr)
    return resource_url


def get_collection_url(resource_type):
    resource_url = get_resource_url(resource_type)
    collection_url = resource_url.replace(baseData.delimiter + resource_name(resource_type), '')
    return collection_url


def has_resource_method(resource_type, method):
    methods = get_resource_element(resource_type, 'resourceMethods')
    return method.upper() in methods


def has_collection_method(resource_type, method):
    methods = get_resource_element(resource_type, 'collectionMethods')
    return method.upper() in methods


def generate_resource_field(resource_type, resource_field, sub_resource, field_key):
    if resource_field['type'] == 'bool':
        return True
    if resource_field['type'] == 'string':
        field_value = resource_name(resource_type) + toolkit.gen_random_str().lower()
        if field_key == 'name':
            field_value = resource_name(resource_type)
        if 'path' in field_key.lower():
            field_value = baseData.delimiter + field_value + toolkit.gen_random_str()
        if field_key == 'schedule':
            field_value = '0 0 * * *'
        return field_value
    if resource_field['type'] in int_type:
        return random.randint(1, 2)
    if resource_field['type'] == 'enum':
        return random.choice(resource_field['validValues'])
    if resource_field['type'] == 'array':
        if resource_field['elemType'] == 'string':
            return [toolkit.gen_random_str()]
        sub_fields = sub_resource[resource_field['elemType']]
        sub_payload = {}
        for field in sub_fields:
            sub_payload[field] = generate_resource_field(resource_type, sub_fields[field], sub_resource, field)
        return [sub_payload]
    if resource_field['type'] == 'map':
        if resource_field['keyType'] == 'resourceName':
            return {generate_resource_field(resource_type, sub_resource['resourceName'], sub_resource, 'resourceName'): str(random.randint(1, 2))}
        return {toolkit.gen_random_str(): toolkit.gen_random_str()}
    if resource_field['type'] == 'advancedOptions':
        sub_fields = sub_resource[resource_field['type']]
        sub_payload = {}
        for field in sub_fields:
            sub_payload[field] = generate_resource_field(resource_type, sub_fields[field], sub_resource, field)
        return sub_payload


def check_field_basic_type(field_value, field_type, field_key):
    print('[' + field_key + ']', field_type, field_value)
    if field_type == 'bool':
        field_type = bool
    if field_type in int_type:
        field_type = int
    if field_type == 'string':
        field_type = str
    if field_type == 'array':
        field_type = list
    if field_type == 'map':
        field_type = dict
    if field_type == 'enum' or field_type == 'advancedOptions':
        return
    if not isinstance(field_value, field_type):
        # raise Exception(TypeError)
        print(field_key + "'s type is not " + field_type.__name__)


def check_resource_field(resource_type, resource_field, response_field, sub_resource, field_key):
    if field_key == 'status':
        return
    check_field_basic_type(response_field, resource_field['type'], field_key)
    if resource_field['type'] == 'enum':
        if response_field not in resource_field['validValues']:
            raise Exception(TypeError)
    if resource_field['type'] == 'array':
        if resource_field['elemType'] == 'string':
            for field in response_field:
                check_field_basic_type(field, resource_field['elemType'], field)
            return
        sub_fields = sub_resource[resource_field['elemType']]
        for field in sub_fields:
            check_resource_field(resource_type, sub_fields[field], response_field[0][field], sub_resource, field)
    if resource_field['type'] == 'map':
        for field in response_field:
            check_field_basic_type(field, 'string', field)
    if resource_field['type'] == 'advancedOptions':
        sub_fields = sub_resource[resource_field['type']]
        for field in sub_fields:
            check_resource_field(resource_type, sub_fields[field], response_field[field], sub_resource, field)


def post_payload(resource_type):
    post_parameter = get_resource_element(resource_type, 'postParameters')
    post_field = post_parameter['fields']
    sub_resource = {}
    if 'subResources' in post_parameter.keys():
        sub_resource = post_parameter['subResources']
    payload = {}
    for field in post_field:
        payload[field] = generate_resource_field(resource_type, post_field[field], sub_resource, field)
    return payload


def check_resource_response(resource_type, response):
    resource_field = get_resource_element(resource_type, 'resourceFields')
    sub_resource = {}
    resource_self = get_resource_element(resource_type, 'subResources', resource_self=True)
    if 'subResources' in resource_self.keys():
        sub_resource = resource_self['subResources']
    for field in resource_field:
        try:
            check_resource_field(resource_type, resource_field[field], response[field], sub_resource, field)
        except KeyError:
            print('missing ' + field + ' in response.')


class HttpResponse(object):
    def __init__(self, status, response):
        self.status = status
        self.response = response


def get_response(method, url, payload=None, token=None):
    if not token:
        token = get_token_by_login()
    rq = requests.request(method, url, json=payload, headers={'Authorization': 'Bearer ' + token})
    response = None
    if not method.lower() == 'delete':
        response = rq.json()
    http_status = rq.status_code
    http_response = HttpResponse(http_status, response)
    return http_response


def check_resource(resource_type, method, url, is_collection=False):
    payload = None
    if method.lower() == 'post':
        payload = post_payload(resource_type)
    response = get_response(method, url, payload)
    print(method + ' ' + url + '\n' + 'STATUS: ' + str(response.status) + '\n' + str(json.dumps(payload)) + '\n' + str(
        json.dumps(response.response)) + '\n\n')
    if is_collection:
        response.response = response.response['data'][0]
    if not response.status == http_code[method]:
        raise Exception(method + ' status ' + str(response.status) + ' not ok.')
    if not method.lower() == 'delete':
        check_resource_response(resource_type, response.response)


def check_all_method(resource_type):
    resource_url = get_resource_url(resource_type)
    collection_url = get_collection_url(resource_type)
    for method_exec in method_exec_order:
        if method_exec == 'post_resource' and has_collection_method(resource_type, 'post'):
            check_resource(resource_type, 'post', collection_url)
        method_and_resource = method_exec.split('_')
        method = method_and_resource[0]
        resource = method_and_resource[1]
        if resource == 'resource' and has_resource_method(resource_type, method):
            if resource_type == 'namespace' and method.upper() == 'DELETE':
                delete_namespace()
                return
            if resource_type == 'pod' and method.upper() == 'GET':
                return
            check_resource(resource_type, method, resource_url)
        if resource == 'collection' and has_collection_method(resource_type, method):
            check_resource(resource_type, method, collection_url, is_collection=True)


def post_parent(resource_type):
    relations = get_resource_relation(resource_type)
    relations.pop(-1)
    for relation in relations:
        if has_collection_method(relation, 'post'):
            check_resource(relation, 'post', get_collection_url(relation))


def delete_namespace():
    resource_url = get_resource_url('namespace')
    check_resource('namespace', 'delete', resource_url)
    while True:
        response = get_response('delete', resource_url)
        time.sleep(namespace_check_interval)
        if str(response.status) == '404':
            break


def delete_namespace_without_warning():
    try:
        delete_namespace()
    except Exception as error:
        print(error)


def create_namespace():
    collection_url = get_collection_url('namespace')
    check_resource('namespace', 'post', collection_url)


def encrypt_password(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode())
    password = sha1.hexdigest()
    return password


def user_login_status(user=baseData.admin_user, password=baseData.admin_password):
    password = encrypt_password(password)
    login_payload = {'user': user, 'password': password}
    login_url = baseData.base_url + baseData.delimiter + 'users/' + user + '?action=login'
    rq = requests.request('post', login_url, json=login_payload)
    return rq.status_code


def get_token_by_login(user=baseData.admin_user, password=baseData.admin_password):
    password = encrypt_password(password)
    login_payload = {'user': user, 'password': password}
    login_url = baseData.base_url + baseData.delimiter + 'users/' + user + '?action=login'
    rq = requests.request('post', login_url, json=login_payload)
    return rq.json()['token']


def check_dir(the_dir):
    if not os.path.exists(the_dir):
        os.makedirs(the_dir)


def save_token(user=baseData.admin_user, password=baseData.admin_password):
    token = get_token_by_login(user, password)
    check_dir(baseData.token_path)
    with open(baseData.token_path + '/' + user, 'w') as token_file:
        token_file.write(token)


def get_token_by_file(user=baseData.admin_user):
    with open(baseData.token_path + '/' + user) as token_file:
        token = token_file.read()
    return token
