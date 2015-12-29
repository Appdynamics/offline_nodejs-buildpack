#!/usr/bin/python

import sys
import json

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

base_path = sys.argv[1] 
json_object = sys.argv[2]
print json.load(json_object)




