from behave import given, when, then
from Config import Config, ConfigError
from unittest import mock

@given(u'I have specified "{input_file}" as input file')
def step_impl(context, input_file):
    context.input_file = input_file

@given(u'I have specified "{output_file}" as output file')
def step_impl(context, output_file):
    context.output_file = output_file

@given(u'I have specified "{backup_file}" as backup file')
def step_impl(context, backup_file):
    context.backup_file = backup_file

def create_file_mock(context, attr_name, default_value):
    file_mock = mock.Mock()
    file_mock.name = getattr(context, attr_name, default_value)
    return file_mock

def create_backup_file_mock(context):
    try:
        file_mock = mock.Mock()
        file_mock.name = getattr(context, 'backup_file')
    except AttributeError:
        file_mock = None
    return file_mock

@when(u'I try to read the config')
def step_impl(context):
    args_mock = mock.Mock()
    args_mock.input_file = create_file_mock(context, 'input_file', 'input/good_file')
    args_mock.output_file = create_file_mock(context, 'output_file', 'output/good_file')
    args_mock.backup_file = create_backup_file_mock(context)
    arg_parser = mock.Mock()
    arg_parser.parse_args = mock.Mock(return_value=args_mock)
    yaml_mock = mock.Mock()
    yaml_mock.load = mock.Mock()
    config = Config(arg_parser, mock.Mock, yaml_mock)
    try:
        config.read()
    except ConfigError as e:
        context.exception_message = e.args[0]

@then(u'I should not receive an exception')
def step_impl(context):
    assert not hasattr(context, 'exception_message')

@then(u'I should receive an exception with "{exception_message}" as message')
def step_impl(context, exception_message):
    assert context.exception_message == exception_message