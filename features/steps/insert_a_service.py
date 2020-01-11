from behave import given, when, then
from ServiceData import ServiceData
from Compose import Compose
from ServiceImage import ServiceImage
from util import to_dict
from copy import deepcopy

@given(u'a docker-compose with the following content')
def step_impl(context):
    context.raw_compose_model = context.text

@given(u'"{service_image}" as the new image of an existing service')
@given(u'"{service_image}" as the image of the new service')
def step_impl(context, service_image):
    context.service_image = service_image

@given(u'I have specified "{ip_address}" as IP address')
def step_impl(context, ip_address):
    if ip_address != '-':
        context.ip_address = ip_address

@given(u'I have specified "{external_port}" as external port')
def step_impl(context, external_port):
    if external_port != '-':
        context.external_port = external_port

@given(u'I have specified "{internal_port}" as internal port')
def step_impl(context, internal_port):
    if internal_port != '-':
        context.internal_port = internal_port

@when(u'I try to generate a new docker-compose')
def step_impl(context):
    compose_model = to_dict(context.raw_compose_model)

    if 'volumes' in compose_model:
        context.previous_volumes = deepcopy(compose_model['volumes'])

    service_image = ServiceImage(getattr(context, 'service_image', 'x-us-field:34'))
    proposed_address = { 
        'ip': getattr(context, 'ip_address', None),
        'external_port': getattr(context, 'external_port', None),
        'internal_port': getattr(context, 'internal_port', None)
    }
    service_data = ServiceData(volume_enabled=getattr(context, 'volume_enabled', False))
    context.compose, context.service_name = Compose(compose_model, service_data).generate(service_image, proposed_address)

@then(u'I should receive a docker-compose that includes "{service_name}" as a service')
def step_impl(context, service_name):
    assert service_name in context.compose['services']

@then(u'I should receive a docker-compose that includes a service with "{socket_address}" as socket address')
def step_impl(context, socket_address):
    expected_socket_address = { 'ports': [ socket_address ] }
    assert expected_socket_address.items() <= context.compose['services'][context.service_name].items()

@then(u'I should receive a docker-compose that includes "{volume}" as a volume')
def step_impl(context, volume):
    service_volumes = context.compose['services'][context.service_name]['volumes']
    assert len([v for v in service_volumes if v.split(':')[0] == volume]) == 1
    assert volume in context.compose['volumes']

@then(u'the volumes that were already there')
def step_impl(context):
    assert context.previous_volumes.items() <= context.compose['volumes'].items()

@then(u'I should receive a docker-compose with no volumes')
def step_impl(context):
    assert 'volumes' not in context.compose

@then(u'I should receive a docker-compose with same volumes')
def step_impl(context):
    assert context.previous_volumes.items() == context.compose['volumes'].items()

@then(u'"{eureka_ip_address}" as EUREKA_INSTANCE_IP-ADDRESS')
def step_impl(context, eureka_ip_address):
    assert context.compose['services'][context.service_name]['environment']['EUREKA_INSTANCE_IP-ADDRESS'] == eureka_ip_address

@then(u'"{server_port}" as SERVER_PORT')
def step_impl(context, server_port):
    assert context.compose['services'][context.service_name]['environment']['SERVER_PORT'] == server_port