import os
import sys
import json
import os.path
import logging
#from build_pack_utils import utils, runner

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)


build_dir = sys.argv[1]

def get_vcap_args():
    vcap_services_filename = "_vcap_services.txt"
    vcap_application_filename = "_vcap_application.txt"
    vcap_services_filename = os.path.join(build_dir, vcap_services_filename)
    vcap_services_filename = os.path.join(build_dir, vcap_application_filename)
    
    with open(vcap_services_filename) as data_file:
        VCAP_SERVICES = json.load(data_file)

    with open(vcap_application_filename) as data_file:
        VCAP_APPLICATION = json.load(data_file)
    
    return VCAP_SERVICES, VCAP_APPLICATION


def generate_appdy_statement():
    print VCAP_SERVICES
    print VCAP_APPLICATION
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


VCAP_SERVICES, VCAP_APPLICATION = get_vcap_args()
generate_appdy_statement()


'''
VCAP_SERVICES = json.loads(sys.argv[1])
VCAP_APPLICATION = json.loads(sys.argv[2])

print VCAP_SERVICES
print VCAP_APPLICATION

preprocess_commands()

# Extension Methods
def preprocess_commands():
    print "test preprocess"
    #service = ctx.get('VCAP_SERVICES', {})
    service_defs = VCAP_SERVICES.get('appdynamics', [])
    application_defs = VCAP_APPLICATION.get('limits', [])
    detected = False
    print service_defs
    print len(service_defs)
    print len(application_defs)
    print application_defs
    
    
    if len(service_defs) == 0:
       _log.info("AppDynamics services with tag appdynamics not detected.")
       _log.info("Looking for tag app-dynamics service.")
       service_defs = ctx.get('app-dynamics', [])
       if len(service_defs) == 0:
          _log.info("AppDynamics services with tag app-dynamics not detected.")
          _log.info("Looking for Appdynamics user-provided service.")
          cups_service_defs = ctx.get('user-provided', [])

          if len(cups_service_defs) == 0:
             _log.info("AppDynamics services not detected.")
          else:
             cups_svc = cups_service_defs.get('name', [])
             if (cups_svc == "appdynamics") or (cups_svc == "app-dynamics"):
                _log.info("AppDynamics cups services detected.")
                detected = True

    if len(service_defs) > 0:
        _log.debug("AppDynamics service detected.")
        detected = True

    if detected == True: 
        #mylist = ["require('appdynamics').profile({","controllerHostName: '52.33.129.11',","controllerPort: 8090,","accountName: 'customer1',","accountAccessKey: 'e47c0e60-6e7d-41ad-8c64-0ae0d2f6708b',","applicationName: 'nodejs_test2',","tierName: 'test',","nodeName: 'process'","});"]
        #mylist = ["require("appdynamics").profile({", "controllerHostName: '<controller host name>',","controllerPort: <controller port number>, ","controllerSslEnabled: false,  // Set to true if controllerPort is SSL","accountName: '<AppDynamics_account_name>',","accountAccessKey: '<AppDynamics_account_key>', //required","applicationName: 'your_app_name',","tierName: 'choose_a_tier_name', ","nodeName: 'choose_a_node_name', ","});"]
        #f = open("init_server.js", "w")
        #os.system("pwd")
        #f.write("\n".join(map(lambda x: str(x), mylist)))
        #f.close()
        #os.system("node init_server.js --use_strict")
        #print os.system("echo $VCAP_APPLICATION")
        exit_code = os.system("echo preprocess_commands: AppDynamics agent configuration")
        
        return [[ 'echo', '" in preprocess;"'],
                ['env'],
                [ 'chmod', ' -R 755 /home/vcap/app'],
                [ 'chmod', ' 777 ./app/appdynamics/appdynamics-nodejs-agent/logs'],
                [ 'export', ' APP_TIERNAME=`echo $VCAP_APPLICATION | sed -e \'s/.*application_name.:.//g;s/\".*application_uri.*//g\' `'],
                [ 'if [ -z $application_name ]; then export APP_NAME=$APP_TIERNAME && APP_TIERNAME=$APP_TIERNAME; else export APP_NAME=$application_name; fi'],
                [ 'export', ' APP_HOSTNAME=$APP_TIERNAME:`echo $VCAP_APPLICATION | sed -e \'s/.*instance_index.://g;s/\".*host.*//g\' | sed \'s/,//\' `'],
                [ 'export', ' AD_ACCOUNT_NAME=`echo $VCAP_SERVICES | sed -e \'s/.*account-name.:.//g;s/\".*port.*//g\' `'],
                [ 'export', ' AD_ACCOUNT_ACCESS_KEY=`echo $VCAP_SERVICES | sed -e \'s/.*account-access-key.:.//g;s/\".*host-name.*//g\' `'],
                [ 'export', ' AD_CONTROLLER=`echo $VCAP_SERVICES | sed -e \'s/.*host-name.:.//g;s/\".*ssl-enabled.*//g\' `'],
                [ 'export', ' AD_PORT=`echo $VCAP_SERVICES | sed -e \'s/.*port.:.//g;s/\".*account-access-key.*//g\' `'],
                [ 'export', ' sslenabled=`echo $VCAP_SERVICES | sed -e \'s/.*ssl-enabled.:.//g;s/\".*.*//g\'`'],
                [ 'if [ $sslenabled == \"true\" ] ; then export sslflag=-s ; fi; '],
                [ 'echo sslflag set to $sslflag' ],
                [ 'PATH=$PATH:./app/php/bin/ ./app/appdynamics/appdynamics-php-agent/install.sh $sslflag -i ./app/appdynamics/phpini -a=$AD_ACCOUNT_NAME@$AD_ACCOUNT_ACCESS_KEY $AD_CONTROLLER $AD_PORT $APP_NAME $APP_TIERNAME $APP_HOSTNAME' ],
                [ 'cat', ' /home/vcap/app/appdynamics/phpini/appdynamics_agent.ini >> /home/vcap/app/php/etc/php.ini'],
                [ 'cat', ' /home/vcap/app/appdynamics/phpini/appdynamics_agent.ini'],
                [ 'echo', '"done preprocess"'],
                ['env']]
    else:
        return ()
    '''
