Feature: Insert a service

    Scenario Outline: Inserting a service that does not exist
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
              anotherDummyService:
                assocArr: 24
            """
        And "<service_image>" as the image of the new service
        When I try to generate a new docker-compose
        Then I should receive a docker-compose that includes "<service_name>" as a service
    
    Examples:
        | service_image     | service_name |
        | x-us-field    | xusfield |
        | x-field       | xfield   |
        | x             | x        |
        | x:34          | x        |
        | x-us-field:34 | xusfield |

    Scenario Outline: Inserting a service with different socket addresses
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
                ports:
                  - 9010
                  - 9011:9999
                  - 192.168.10.6:9012:9998
              anotherDummyService:
                assocArr: 24
                ports:
                  - 9009:9997
                  - 192.168.10.6:9012:9996
                  - 9008
            """
        And I have specified "<ip_address>" as IP address
        And I have specified "<external_port>" as external port
        And I have specified "<internal_port>" as internal port
        When I try to generate a new docker-compose
        Then I should receive a docker-compose that includes a service with "<socket_address>" as socket address
        And "<eureka_ip_address>" as EUREKA_INSTANCE_IP-ADDRESS
        And "<server_port>" as SERVER_PORT
    
    Examples:
        | ip_address   | external_port | internal_port | socket_address         | eureka_ip_address | server_port |
        | -            | -             | -             | 192.168.10.7:9022:9022 | 192.168.10.7      | 9022        |
        | 192.168.10.5 | -             | -             | 192.168.10.5:9022:9022 | 192.168.10.5      | 9022        |
        | -            | 8010          | -             | 192.168.10.7:8010:8010 | 192.168.10.7      | 8010        |
        | -            | -             | 8020          | 192.168.10.7:8020:8020 | 192.168.10.7      | 8020        |
        | 192.168.10.5 | 8010          | -             | 192.168.10.5:8010:8010 | 192.168.10.5      | 8010        |
        | -            | 8010          | 8020          | 192.168.10.7:8010:8020 | 192.168.10.7      | 8020        |
        | 192.168.10.5 | -             | 8020          | 192.168.10.5:8020:8020 | 192.168.10.5      | 8020        |
        | 192.168.10.5 | 8010          | 8020          | 192.168.10.5:8010:8020 | 192.168.10.5      | 8020        |

    Scenario Outline: Inserting a service with its volume enabled in a compose with no global volumes
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
              anotherDummyService:
                assocArr: 24
            """
        And "<service_image>" as the image of the new service
        And I have enabled volumes for new services
        When I try to generate a new docker-compose
        Then I should receive a docker-compose that includes "<volume>" as a volume

        Examples:
            | service_image     | volume              |
            | x             | x-config        |
            | x-us-field    | xusfield-config |
            | x-us-field:34 | xusfield-config |

    Scenario: Inserting a service with its volume disabled in a compose with no global volumes
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
              anotherDummyService:
                assocArr: 24
            """
        When I try to generate a new docker-compose
        Then I should receive a docker-compose with no volumes

    Scenario Outline: Inserting a service with its volume enabled in a compose with global volumes
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
              anotherDummyService:
                assocArr: 24
            volumes:
                dummyVolumeA:
                dummyVolB:
            """
        And "<service_image>" as the image of the new service
        And I have enabled volumes for new services
        When I try to generate a new docker-compose
        Then I should receive a docker-compose that includes "<volume>" as a volume
        And the volumes that were already there

        Examples:
            | service_image     | volume              |
            | x             | x-config        |
            | x-us-field    | xusfield-config |
            | x-us-field:34 | xusfield-config |

    Scenario: Inserting a service with its volume disabled in a compose with global volumes
        Given a docker-compose with the following content
            """
            version: '2'
            services:
              service1:
                assocArr: 'randomValue'
              anotherDummyService:
                assocArr: 24
            volumes:
                dummyVolumeA:
                dummyVolB:
            """
        When I try to generate a new docker-compose
        Then I should receive a docker-compose with same volumes
