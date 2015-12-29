#!/usr/bin/python

import sys
import json
import os
import os.path
import tempfile
import shutil
from build_pack_utils.cloudfoundry import CloudFoundryUtil

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

base_path = sys.argv[1] 
json_object = sys.argv[2]
print json.loads(json_object)

CloudFoundryUtil.initialize()
appdynamics = utils.load_extension(os.path.join(base_path,'extensions'))
ad = appdynamics.AppDynamicsInstaller(json.loads(json_object))
eq_(True, ad.should_install())
eq_('x64', ad._php_arch)
eq_('@{HOME}/php/lib/php/extensions/no-debug-non-zts-20121212',
    ad._php_extn_dir)
eq_(False, ad._php_zts)
eq_('20121212', ad._php_api)
eq_('@{HOME}/appdynamics/agent/x64/appdynamics-20121212.so', ad.appdynamics_so)
eq_('app-name-2', ad.app_name)
eq_('LICENSE2', ad.license_key)
eq_('@{HOME}/logs/appdynamics-daemon.log', ad.log_path)
eq_('@{HOME}/appdynamics/daemon/appdynamics-daemon.x64', ad.daemon_path)
eq_('@{HOME}/appdynamics/daemon.sock', ad.socket_path)
eq_('@{HOME}/appdynamics/daemon.pid', ad.pid_path)




