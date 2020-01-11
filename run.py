from Config import Config, ConfigError
from argparse import ArgumentParser, FileType
from ruamel.yaml import YAML
from ServiceImage import ServiceImage
from ServiceData import ServiceData
from Compose import Compose
from sys import stderr
from os import SEEK_SET

def backup_file(file, backup_file):
    if backup_file:
        file.seek(0, SEEK_SET)
        backup_file.writelines(file.readlines())

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
try:
    config = Config(ArgumentParser(), FileType, yaml).read()
    backup_file(config['input_file'], config['backup_file'])
    service_data = ServiceData(config['service_model'], config['volume_enabled'])
    service_image = ServiceImage(config['image'])
    proposed_address = {
        'ip': config['ip'],
        'external_port': config['external_port'],
        'internal_port': config['internal_port']
    }
    generated_compose = Compose(config['compose_model'], service_data).generate(service_image, proposed_address)[0]
    config['output_file'].truncate(0)
    yaml.dump(generated_compose, config['output_file'])
except ConfigError as e:
    stderr.write('ConfigError: ' + e.args[0] + '\n')