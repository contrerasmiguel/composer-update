from ruamel.yaml import StringIO

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, arg_parser, file_type, yaml):
        self.arg_parser = arg_parser
        self.file_type = file_type
        self.yaml = yaml

    def valid_file(self, io_type, file):
        folders = file.name.split('/')
        if len(folders) > 0:
            return folders[0] == io_type
        else:
            return False

    def valid_backup_file(self, file):
        return not file or self.valid_file('backup', file)

    def read(self):
        self.arg_parser.add_argument('input_file', type=self.file_type('r'),
            help='Path of the docker-compose file that will be used as input')
        self.arg_parser.add_argument('image',
            help='The name and tag of the image that will be used on the service')
        self.arg_parser.add_argument('output_file', type=self.file_type('a'),
            help='Path of the file that will be used as output')
        self.arg_parser.add_argument('--backup', metavar='BACKUP', dest='backup_file',
            type=self.file_type('w+'), default=None,
            help='If used, content of the input file will be copied to this file')
        self.arg_parser.add_argument('--model', metavar='SERVICE_MODEL', dest='service_model',
            type=self.file_type('r'), default=None,
            help='Path of the file that contains the default values of a service')
        self.arg_parser.add_argument('--ip', metavar='SERVICE_IP', dest='ip',
            default=None,
            help='IP address of the service. Default: 192.168.10.7')
        self.arg_parser.add_argument('--ext-port', metavar='EXTERNAL_PORT', dest='external_port',
            type=int, default=None,
            help='External port of the service')
        self.arg_parser.add_argument('--int-port', metavar='INTERNAL_PORT', dest='internal_port',
            type=int, default=None,
            help='Internal port of the service')
        self.arg_parser.add_argument('--use-volumes', action='store_true', dest='use_volumes',
            help='Enables the volumes of the service.')
        args = self.arg_parser.parse_args()

        if not self.valid_file('input', args.input_file):
            raise ConfigError('the input file must be inside the input directory')
        elif not self.valid_file('output', args.output_file):
            raise ConfigError('the output file must be inside the output directory')
        elif not self.valid_backup_file(args.backup_file):
            raise ConfigError('the backup file must be inside the backup folder')

        return {
            'input_file': args.input_file,
            'compose_model': self.yaml.load(args.input_file),
            'image': args.image,
            'output_file': args.output_file,
            'backup_file': args.backup_file,
            'service_model': None if not args.service_model else self.yaml.load(args.service_model),
            'ip': args.ip,
            'external_port': args.external_port,
            'internal_port': args.internal_port,
            'volume_enabled': args.use_volumes
        }
