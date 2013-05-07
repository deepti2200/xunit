#! python

import logging
import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
from xunit import logger
from xunit import case
from xunit.utils import cls
from xunit.utils import randgen
import re


class TestXmlLogger(case.XUnitCase):
	def XUnitsetUp(self):
		return

	def XUnittearDown(self):
		return

	def test_xmldebug(self):
		cn = cls.GetClassName(self)
		xl = logger.XmlLogger(cn)
		xl.SetLevel(logger.DEBUG_LEVEL)
		xl.Debug()