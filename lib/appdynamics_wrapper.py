#!/usr/bin/python

import sys
import json
import os
import os.path
import tempfile
import shutil
from build_pack_utils import utils

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

base_path = sys.argv[1]
json_object = sys.argv[2]
print json.loads(json_object)

build_dir = tempfile.mkdtemp('build-')
node_dir = os.path.join(build_dir, 'node', 'etc')
os.makedirs(node_dir)



appdynamics = utils.load_extension(os.path.join(base_path,'extensions'))

ctx = utils.FormattedDict({
    'BUILD_DIR': build_dir,
    'APPDYNAMICS_LICENSE': 'JUNK_LICENSE',
    'VCAP_APPLICATION': {
        'name': 'app-name-1'
    },
    'NODE_VM': 'node'
})
ad = appdynamics.preprocess_commands(utils.FormattedDict(json.loads(json_object)))
#ad = appdynamics.AppDynamicsInstaller(ctx)
eq_(True, ad.should_install())

eq_('@{HOME}/appdynamics/agent/x64/appdynamics-20121212.so', ad.appdynamics_so)
eq_('app-name-1', ad.app_name)
eq_('JUNK_LICENSE', ad.license_key)
eq_('@{HOME}/logs/appdynamics-daemon.log', ad.log_path)
eq_('@{HOME}/appdynamics/daemon/appdynamics-daemon.x64', ad.daemon_path)
eq_('@{HOME}/appdynamics/daemon.sock', ad.socket_path)
eq_('@{HOME}/appdynamics/daemon.pid', ad.pid_path)


#ad = appdynamics.AppDynamicsInstaller(utils.FormattedDict(json.loads(json_object)))
#ad = appdynamics.AppDynamicsInstaller(json.loads(json_object))
