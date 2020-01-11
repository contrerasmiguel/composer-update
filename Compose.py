class Compose:
    def __init__(self, model, service_data):
        self.model = model
        self.service_data = service_data

    def to_service_name(self, service_image):
        return ''.join(service_image.name.split('-'))

    def find_external_port(self, socket_address):
        split_address = socket_address.split(':')
        address_item_count = len(split_address)
        if address_item_count == 1:
            last_port = socket_address
        elif address_item_count == 2:
            last_port = split_address[0]
        elif address_item_count == 3:
            last_port = split_address[1]
        else:
            last_port = None
        return int(last_port)

    def calculate_external_port(self, default=9000):
        used_ports = set()
        for service in self.model['services'].values():
            if 'ports' in service:
                for socket_address in [str(p) for p in service['ports']]:
                    ext_port = self.find_external_port(socket_address)
                    if ext_port:
                        used_ports.add(ext_port)
        sorted_ports = sorted(used_ports, reverse=True)
        return str(default if len(sorted_ports) == 0 else (sorted_ports[0] + 10))

    def validate_address(self, address):
        if not address['external_port'] and not address['internal_port']:
            external_port = str(self.calculate_external_port())
            internal_port = external_port
        elif not address['external_port'] and address['internal_port']:
            internal_port = address['internal_port']
            external_port = internal_port
        elif address['external_port'] and not address['internal_port']:
            external_port = address['external_port']
            internal_port = external_port
        else:
            external_port = address['external_port']
            internal_port = address['internal_port']

        return {
            'ip': '192.168.10.7' if not address['ip'] else address['ip'],
            'external_port': external_port,
            'internal_port': external_port if not address['internal_port'] else address['internal_port']
        }

    def generate(self, service_image, proposed_address):
        service_name = self.to_service_name(service_image)
        model_without_services = { k: v for (k, v) in self.model.items() if k != 'services' }
        validated_address = self.validate_address(proposed_address)
        vol_name = service_name + '-config'
        service_data = self.service_data.generate(service_image, {
            'ip': validated_address['ip'],
            'external_port': validated_address['external_port'],
            'internal_port': validated_address['internal_port']
        }, volume_name=vol_name)
        services = { 
            'services': { 
                **self.model['services'],
                **{ service_name: service_data } 
            }
        }

        if self.service_data.volume_enabled == True:
            try:
                model_without_services['volumes'].update({ vol_name: None })
            except KeyError:
                model_without_services['volumes'] = { vol_name: None }

        return { **model_without_services, **services }, service_name