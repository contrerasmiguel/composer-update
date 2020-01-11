Feature: Config safety

    Scenario Outline: Open good files
        Given I have specified "input/<input_file>" as input file
        And I have specified "output/<output_file>" as output file
        When I try to read the config
        Then I should not receive an exception

    Examples:
        | input_file    | output_file     |
        | good_file     | output_file     |
        | x/good_file   | x/output_file   |
        | x/y/good_file | x/y/output_file |

    Scenario Outline: Open bad files
        Given I have specified "<input_file>" as input file
        And I have specified "<output_file>" as output file
        When I try to read the config
        Then I should receive an exception with "<exception_message>" as message

    Examples:
        | input_file      | output_file      | exception_message                                   |
        | input/good_file | bad/output_file  | the output file must be inside the output directory |
        | input/good_file | output_file      | the output file must be inside the output directory |
        | bad/input_file  | output/good_file | the input file must be inside the input directory   |
        | bad/input_file  | bad/output_file  | the input file must be inside the input directory   |
        | input_file      | bad/output_file  | the input file must be inside the input directory   |
    
    Scenario Outline: Open good backup file
        Given I have specified "backup/<backup_file>" as backup file
        When I try to read the config
        Then I should not receive an exception

    Examples:
        | backup_file   |
        | good_file     |
        | x/good_file   |
        | x/y/good_file |

    Scenario Outline: Open bad backup files
        Given I have specified "<backup_file>" as backup file
        When I try to read the config
        Then I should receive an exception with "the backup file must be inside the backup folder" as message

    Examples:
        | backup_file     |
        | bad/backup_file |
        | bad/backup_file |
        | backup_file     |