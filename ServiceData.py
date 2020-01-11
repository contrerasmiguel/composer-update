class ServiceData:
    default_model = {
        'restart': 'always',
        'environment': {
            'ENCRYPT_KEY': '-',
            'SPRING_PROFILES_ACTIVE': 'dev,testdb',
            'SPRING_CLOUD_CONFIG_ENABLED': 'true',
            'SPRING_CLOUD_CONFIG_FAILFAST': 'false',
            'SPRING_CLOUD_CONFIG_URI': 'http://192.168.10.7:8888',
            'SPRING_CLOUD_CONFIG_USERNAME': '-',
            'SPRING_CLOUD_CONFIG_PASSWORD': '{cipher}xxx',
            'JAVA_OPTS': '-d64 -Xms96M -Xmx96M -XX:+CMSClassUnloadingEnabled -XX:+UseParallelGC -XX:+UseNUMA -XX:ParallelGCThreads=2 -XX:MaxNewSize=16m -XX:NewSize=16m -XX:SurvivorRatio=2 -XX:TargetSurvivorRatio=45 -Xloggc:diagnostico.gc'
        },
        'mem_limit': '196M',
        'networks': ['us1']
    }

    def __init__(self, model=None, volume_enabled=False):
        self.model = self.default_model if not model else model
        self.volume_enabled = volume_enabled

    def generate(self, image, socket_address, volume_name=''):
        environment_content = { 
            **{ 'EUREKA_INSTANCE_IP-ADDRESS': socket_address['ip'] },
            **{ 'SERVER_PORT': socket_address['internal_port'] },
            **self.model['environment']
        }
        return {
            **{ 
                'image': str(image),
                'ports': [ socket_address['ip'] + ':' + socket_address['external_port'] + ':'
                    + socket_address['internal_port'] ]
            },
            **({ 'volumes': [ volume_name + ':/opt/' + image.name + '/kus-api/main/resources' ] }
                if self.volume_enabled == True else {}),
            **{
                **self.model,
                **{ 'environment': environment_content } 
            }
        }