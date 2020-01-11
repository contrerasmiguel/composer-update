Feature: Create a service

    Scenario: No service model specified
        When I try to create a service
        Then I should receive a service that includes the values shown below
            """
            restart: always
            environment:
              ENCRYPT_KEY: -
              SPRING_PROFILES_ACTIVE: dev,testdb
              SPRING_CLOUD_CONFIG_ENABLED: 'true'
              SPRING_CLOUD_CONFIG_FAILFAST: 'false'
              SPRING_CLOUD_CONFIG_URI: 'http://192.168.10.7:8888'
              SPRING_CLOUD_CONFIG_USERNAME: '-'
              SPRING_CLOUD_CONFIG_PASSWORD: '{cipher}xxx'
              JAVA_OPTS: "-d64 -Xms96M -Xmx96M -XX:+CMSClassUnloadingEnabled -XX:+UseParallelGC -XX:+UseNUMA -XX:ParallelGCThreads=2 -XX:MaxNewSize=16m -XX:NewSize=16m -XX:SurvivorRatio=2 -XX:TargetSurvivorRatio=45 -Xloggc:diagnostico.gc"
            mem_limit: 196M
            networks:
              - us1
            """

    Scenario: A service model specified
        Given I have specified the following service model
            """
            restart: never
            environment:
              ENCRYPT_KEY: -
              SPRING_PROFILES_ACTIVE: dev,testdb
              SPRING_CLOUD_CONFIG_ENABLED: 'true'
              SPRING_CLOUD_CONFIG_FAILFAST: 'false'
              SPRING_CLOUD_CONFIG_URI: 'http://192.168.10.7:8888'
              SPRING_CLOUD_CONFIG_USERNAME: '-'
              SPRING_CLOUD_CONFIG_PASSWORD: '{cipher}xxx'
            mem_limit: 1024M
            networks:
              - us1
              - us2
            """
        When I try to create a service
        Then I should receive a service that includes the values specified in the model

    Scenario: An image is specified
        Given I have specified "<image>" as an image
        When I try to create a service
        Then I should receive a service with "<image>" as image

    Scenario: Service volume was not requested
        When I try to create a service
        Then I should receive a service with no volumes

    Scenario Outline: Service volume was requested
        Given I have enabled volumes for new services
        And I have specified "<image>" as an image
        When I try to create a service
        Then I should receive a service with "<volume>" as volume

    Examples:
        | image             | volume                                                           |
        | x             | x-config:/opt/x/kus-api/main/resources                   |
        | x-us-field    | x-us-field-config:/opt/x-us-field/kus-api/main/resources |
        | x-us-field:34 | x-us-field-config:/opt/x-us-field/kus-api/main/resources |