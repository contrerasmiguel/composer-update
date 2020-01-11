from behave import given, when, then
from ServiceData import ServiceData
from ServiceImage import ServiceImage
from ruamel.yaml import YAML
from util import to_dict, rec_merge
from copy import deepcopy

@given(u'I have specified "{image}" as an image')
def step_impl(context, image):
    context.image = image

@given(u'I have specified the following service model')
def step_impl(context):
    context.raw_service_model = context.text

@when(u'I try to create a service')
def step_impl(context):
    service_model = to_dict(getattr(context, 'raw_service_model', None))
    service_image = ServiceImage(getattr(context, 'image', 'dummy-service'))
    socket_address = {
        'ip': '192.168.10.7',
        'external_port': '9000',
        'internal_port': '9000'
    }
    volume_name = getattr(context, 'image', 'x-us-field:34').split(':')[0] + '-config'
    context.service_data = ServiceData(service_model, getattr(context, 'volume_enabled', 'False')).generate(service_image, socket_address, volume_name=volume_name)

def model_in_service_data(context, raw_service_model):
    service_model = to_dict(raw_service_model)
    service_data = deepcopy(context.service_data)
    rec_merge(service_data, service_model)
    return service_model.items() <= service_data.items()

@then(u'I should receive a service that includes the values shown below')
def step_impl(context):
    assert model_in_service_data(context, context.text)

@then(u'I should receive a service that includes the values specified in the model')
def step_impl(context):
    assert model_in_service_data(context, context.raw_service_model)

@then(u'I should receive a service with "{image}" as image')
def step_impl(context, image):
    assert { 'image': context.image }.items() <= context.service_data.items()

@then(u'I should receive a service with no volumes')
def step_impl(context):
    assert 'volumes' not in context.service_data

@then(u'I should receive a service with "{volume}" as volume')
def step_impl(context, volume):
    assert False if ('volumes' not in context.service_data) else volume in context.service_data['volumes']