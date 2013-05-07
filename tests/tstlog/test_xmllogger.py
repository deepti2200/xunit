#! python

import logging
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
from xunit import logger
from xunit import case
from xunit.utils import cls
from xunit.utils.randgen import InitRandom,GenRandomChars,GenRandomNum
import re


class TestXmlLogger(case.XUnitCase):
	@classmethod
	def XUnitsetUpClass(cls):
		InitRandom()
		return
	def XUnitsetUp(self):
		return

	def XUnittearDown(self):
		return

	def test_xmldebug(self):
		cn = cls.GetClassName(self)
		xl = logger.XmlLogger(cn)
		xl.SetLevel(logger.DEBUG_LEVEL)
		n = GenRandomNum(100,1)
		s = GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		v = xl.Flush()
		self.assertTrue(vpat.search(v))

		xl.SetLevel(logger.WARNING_LEVEL)
		n = GenRandomNum(100,1)
		s = GenRandomChars(n)
		xl.Debug(s)
		vpat = re.compile(s)
		v = xl.Flush()
		self.assertTrue(v == '')
		return

	


