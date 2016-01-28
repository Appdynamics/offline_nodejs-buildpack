import os
import sys
import json
import os.path
import logging
import subprocess

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
            
    def set_environ_variables(self):
        setEnv = "cf set-env %s http_proxy %s"%(self.applicationName, self.httpProxy)
        subprocess.call(setEnv)
    
    def generate_appdy_statement(self):
        self.get_vcap_args()
    
        self.extension_name = "appdynamics"
        self.controllerHostName = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["host-name"]
        self.controllerPort = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["port"]
        self.accountName = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["account-name"]
        self.accountAccessKey = self.VCAP_SERVICES["appdynamics"][0]["credentials"]["account-access-key"]
        self.applicationName = os.getenv('APPDYNAMICS_APP_NAME') or self.VCAP_APPLICATION["name"]
        self.tierName = self.VCAP_APPLICATION["name"]
        self.nodeName = self.tierName
        self.httpProxy= os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
        if self.httpProxy:
            self.set_environ_variables()
        require_statement = """require('%s').profile({ controllerHostName: 
            '%s',controllerPort: %s, accountName: '%s', accountAccessKey: '%s', 
            applicationName: '%s',tierName: '%s',nodeName: '%s'});""" % (self.extension_name, self.controllerHostName, self.controllerPort, self.accountName, self.accountAccessKey, self.applicationName, self.tierName, self.nodeName)
    
        print require_statement
        
Appdynamics_ext_obj = Appdynamics_ext()
Appdynamics_ext_obj.generate_appdy_statement()
