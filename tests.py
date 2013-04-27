#! python

import os
import sys
import logging

targs = ''
if len(sys.argv[1:]) > 0:
	targs = ' '.join(sys.argv[1:])

absdir = os.path.dirname(os.path.abspath(__file__))

testcases_files = [
	os.path.join(absdir,'tests','cfgtest','test_config.py'),
	os.path.join(absdir,'tests','ldrtest','test_suite.py'),
	os.path.join(absdir,'tests','tstcase','test_case.py'),
	os.path.join(absdir,'tests','tstcls','test_cls.py'),
	os.path.join(absdir,'tests','tstlog','test_logger.py')
]

for f in testcases_files:
	cmd = 'python %s %s'%(f,targs)
	ret = os.system(cmd)
	if ret != 0:
		logging.error('can not run (%s) proper'%(cmd))
		sys.exit(3)