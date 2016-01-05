import os
import sys
import json
import os.path
import logging

def get_vcap_args():
    build_dir = sys.argv[1]
    vcap_services_filename = "_vcap_services.txt"
    vcap_application_filename = "_vcap_application.txt"
    vcap_services_filename = os.path.join(build_dir, vcap_services_filename)
    vcap_application_filename = os.path.join(build_dir, vcap_application_filename)
    
    with open(vcap_services_filename) as data_file:
        VCAP_SERVICES = json.load(data_file)

    with open(vcap_application_filename) as data_file:
        VCAP_APPLICATION = json.load(data_file)
    return VCAP_SERVICES, VCAP_APPLICATION


def generate_appdy_statement():
    VCAP_SERVICES, VCAP_APPLICATION = get_vcap_args()

    extension_name = "appdynamics"
    controllerHostName = VCAP_SERVICES["appdynamics"][0]["credentials"]["host-name"]
    controllerPort = VCAP_SERVICES["appdynamics"][0]["credentials"]["port"]
    accountName = VCAP_SERVICES["appdynamics"][0]["credentials"]["account-name"]
    accountAccessKey = VCAP_SERVICES["appdynamics"][0]["credentials"]["account-access-key"]
    applicationName = VCAP_APPLICATION["name"]
    tierName = "test"
    nodeName = "process"
    
    require_statement = """require('%s').profile({ controllerHostName: 
        '%s',controllerPort: %s, accountName: '%s', accountAccessKey: '%s', 
        applicationName: '%s',tierName: '%s',nodeName: '%s'});""" % (extension_name, controllerHostName, controllerPort, accountName, accountAccessKey, applicationName, tierName, nodeName)

    print require_statement
    
generate_appdy_statement()
