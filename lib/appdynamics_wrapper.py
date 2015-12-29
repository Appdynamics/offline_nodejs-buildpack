#!/usr/bin/python

import sys
import json
import os
import os.path
import tempfile
import shutil
from nose.tools import eq_
from nose.tools import with_setup
from build_pack_utils import utils

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

base_path = sys.argv[1] 
json_object = sys.argv[2]
print json.load(json_object)


appdynamics = utils.load_extension('extensions')





