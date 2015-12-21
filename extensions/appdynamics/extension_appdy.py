import os
import sys
import json
import os.path
import logging
import subprocess
import commands

class Appdynamics_ext:
    def set_environ_variables(self):
        setEnv = "cf set-env %s http_proxy %s"%(self.applicationName, self.httpProxy)
        subprocess.call(setEnv)
    
    def generate_appdy_statement(self):
        self.VCAP_SERVICES=json.loads(os.environ['VCAP_SERVICES'])
        self.VCAP_APPLICATION=json.loads(os.environ['VCAP_APPLICATION'])
        
        print self.VCAP_SERVICES
        print self.VCAP_APPLICATION
        
        if "appdynamics" in self.VCAP_SERVICES:
            self.extension_name = "appdynamics"
        else:
            self.extension_name = "user-provided"
            
        self.tierName = self.VCAP_APPLICATION["name"]
        self.nodeName = "%s:%s"%(self.tierName, str(os.system("echo $VCAP_APPLICATION | sed -e \'s/.*instance_index.://g;s/\".*host.*//g\' | sed \'s/,//\'")))
        self.httpProxy= os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
        
        if self.httpProxy:
            self.set_environ_variables()

        require_statement = """require('appdynamics').profile({ controllerHostName:JSON.parse(process.env.VCAP_SERVICES)["%s"][0].credentials["host-name"],
            controllerPort: JSON.parse(process.env.VCAP_SERVICES)["%s"][0].credentials["port"],
            accountName: JSON.parse(process.env.VCAP_SERVICES)["%s"][0].credentials["account-name"],
            accountAccessKey: JSON.parse(process.env.VCAP_SERVICES)["%s"][0].credentials["account-access-key"],
            applicationName: JSON.parse(process.env.VCAP_APPLICATION).application_name, tierName: JSON.parse(process.env.VCAP_APPLICATION).application_name,
            nodeName: '%s','noNodeNameSuffix': 'true'});""" % (self.extension_name, self.extension_name, self.extension_name, 
            self.extension_name, self.nodeName)
        print require_statement
        vcap_application_filename = os.path.join("/tmp", '_appd_module.txt')
        f = open(vcap_application_filename, 'w')
        f.write(require_statement)
        f.close()

Appdynamics_ext_obj = Appdynamics_ext()
Appdynamics_ext_obj.generate_appdy_statement()
