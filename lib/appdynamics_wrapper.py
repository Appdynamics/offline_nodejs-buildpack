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


appdynamics = utils.load_extension('extensions')
ad = appdynamics.AppDynamicsInstaller(json.loads(json_object))




