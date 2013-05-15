#! python

import unittest
import sys
import logging
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))
from xunit.utils import Xml2Html
from xunit.case import XUnitCase
import StringIO


class XmlUtTest(XUnitCase):
	def test_loadok(self): 
		abspath =os.path.dirname(os.path.abspath(__file__))
		fname = os.path.join(abspath,'o.xml')
		x2h = Xml2Html.Xml2Html()
		sio = StringIO.StringIO()
		x2h.Dump(fname,sio)
		del sio
		del x2h
		return

	def test_notloadok(self):
		abspath =os.path.dirname(os.path.abspath(__file__))
		fname = os.path.join(abspath,'noexist.xml')
		ok = 1
		try:
			sio = StringIO.StringIO()
			x2h = Xml2Html.Xml2Html()
			x2h.Dump(fname,sio)
		except Xml2Html.X2HFileError:
			ok = 0
		self.assertEqual(ok,0)
		return

	def test_dumpfileok(self):
		abspath =os.path.dirname(os.path.abspath(__file__))
		fname = os.path.join(abspath,'o.xml')
		ofname =os.path.join(abspath,'o.html')
		with open(ofname,'w+b') as f:
			x2h = Xml2Html.Xml2Html()
			x2h.Dump(fname,f)
		return

if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(lineno)-5s] %(message)s")	
		pass
	unittest.main()


