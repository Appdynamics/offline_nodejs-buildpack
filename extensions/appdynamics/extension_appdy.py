import os
import sys
import json
import os.path
import logging

class Appdynamics_ext:
    def get_vcap_args(self):
        build_dir = sys.argv[1]
        vcap_services_filename = "_vcap_services.txt"
        vcap_application_filename = "_vcap_application.txt"
        vcap_services_filename = os.path.join(build_dir, vcap_services_filename)
        vcap_application_filename = os.path.join(build_dir, vcap_application_filename)
        
        with open(vcap_services_filename) as data_file:
            self.VCAP_SERVICES = json.load(data_file)
    
        with open(vcap_application_filename) as data_file:
            self.VCAP_APPLICATION = json.load(data_file)
    
    def generate_appdy_statement(self):
        self.get_vcap_args()
    
        extension_name = "appdynamics"
        controllerHostName = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["host-name"]
        controllerPort = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["port"]
        accountName = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["account-name"]
        accountAccessKey = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["account-access-key"]
        applicationName = self.VCAP_APPLICATION["name"]
        tierName = "test"
        nodeName = "process"
        
        require_statement = """require('%s').profile({ controllerHostName: 
            '%s',controllerPort: %s, accountName: '%s', accountAccessKey: '%s', 
            applicationName: '%s',tierName: '%s',nodeName: '%s'});""" % (extension_name, controllerHostName, controllerPort, accountName, accountAccessKey, applicationName, tierName, nodeName)
    
        print require_statement
        
Appdynamics_ext_obj = Appdynamics_ext()
Appdynamics_ext_obj.generate_appdy_statement()
