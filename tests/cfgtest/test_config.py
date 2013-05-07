#! python



import unittest
import sys
import logging
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','src')))
sys.path.append((os.path.dirname(os.path.abspath(__file__))))
import xunit.config

class UtTest(unittest.TestCase):
	def test_LoadBasic(self):
		# now for 
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('base.cfg')
		self.assertEqual(utcfg.GetValue('new','base2'),'hello world')
		return
	def test_IncludeFiles(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		includes = utcfg.GetIncludeFiles()
		self.assertTrue( 'inc.cfg' in includes )
		self.assertTrue( 'base.cfg' in includes )
		#self.assertTrue(len(includes) == 2)
		return

	def test_Unittests(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		units = utcfg.GetUnitTests()
		self.assertTrue('base.unit.test' in units)
		self.assertTrue('inc.unit.test' in units)
		self.assertTrue(len(units) == 2)
		return

	def test_SearchPaths(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		paths = utcfg.GetSearchPaths()
		self.assertTrue( 'inc' in paths)
		return

	def test_OverflowError(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		ok = 1
		try:
			v = utcfg.GetValue('value1','base1')
		except xunit.config.XUnitConfigOverflowError as e:
			ok = 0
		self.assertTrue( ok == 0)

		ok = 1
		try:
			v = utcfg.GetValue('value2','base2')
		except xunit.config.XUnitConfigOverflowError as e:
			ok = 0
		self.assertTrue( ok == 0)
		return

	def test_SectionInnerOverflowError(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		ok = 1
		try:
			v = utcfg.GetValue('valuebase','base1')
		except xunit.config.XUnitConfigOverflowError as e:
			ok = 0
		self.assertTrue( ok == 0)
		return

	def test_NonValue(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		v = utcfg.GetValue('no_section','no_opt')
		self.assertTrue( v == '')
		return
		
	def test_3LevelRef(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		v = utcfg.GetValue('base2.value','base2')
		self.assertEqual(v,'hello param1')
		return

	def test_noref(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		v = utcfg.GetValue('base2.value','base3')
		self.assertEqual(v,' param1')
		return

	def test_setgetvalue(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('inc.cfg')
		utcfg.SetValue('base2.value','base4','%(base2.value.base2)s value')
		v = utcfg.GetValue('base2.value','base4')
		self.assertEqual(v,'hello param1 value')
		return

	def test_LoadError(self):
		ok = 1
		try:
			utcfg = xunit.config.XUnitConfigBase()
			utcfg.LoadFile('nocfg.cfg')
		except xunit.config.XUnitConfigLoadFileError as e:
			ok = 0
		self.assertTrue(ok == 0)
		return

	def test_SearchPathExp(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('exp.cfg')
		paths = utcfg.GetSearchPaths()
		self.assertTrue( '/usr/inc' in paths )
		return

	def test_SearchPathNoRef(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('exp.cfg')
		paths = utcfg.GetSearchPaths()
		self.assertTrue( '/nopath' in paths )
		return

	def test_Singleton(self):
		utcfg = xunit.config.XUnitConfig()
		ut2 = xunit.config.XUnitConfig()
		self.assertTrue( utcfg == ut2)
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__))+os.sep+'inc')
		utcfg.LoadFile('exp.cfg')
		paths = utcfg.GetSearchPaths()
		self.assertTrue( '/nopath' in paths )
		ut2.LoadFile('inc.cfg')
		paths = ut2.GetSearchPaths()
		self.assertTrue( '/nopath' in paths )
		ut2.SetValue('no_section','no_opt','no_value')
		v = utcfg.GetValue('no_section','no_opt')
		self.assertEqual(v,'no_value')
		return

	def test_unittest(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('tst.cfg')
		units = utcfg.GetUnitTests()
		self.assertEqual(units[0] , 'base20.test')
		self.assertEqual(units[1] , 'base30.test')
		self.assertEqual(units[2] , 'base100.test')
		return

	def test_unittestbad(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('tstbad.cfg')
		ok = 1
		try:
			units = utcfg.GetUnitTests()
		except  xunit.config.XUnitConfigKeyError as e:
			ok = 0
		self.assertEqual(ok,0)
		return

	def test_splitunittest(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('tstparam.cfg')
		units = utcfg.GetUnitTests()
		self.assertTrue( units[0] == 'test.base1')
		self.assertTrue( units[1] == 'test.base2')
		self.assertTrue( units[2] == 'test.base3')
		return

	def test_GetSectionsPattern(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('ks.cfg')
		sections = utcfg.GetSectionsPattern()
		self.assertTrue('expsection' in sections)
		self.assertTrue('newsection' in sections)

		sections = utcfg.GetSectionsPattern('^\.\w+')
		self.assertTrue('expsection' not in sections)
		self.assertTrue('newsection' not in sections)
		self.assertTrue('.path' in sections)
		self.assertTrue('test.case' not in sections)
		return

	def test_GetOptionsPattern(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.AddSearchPath(os.path.dirname(os.path.abspath(__file__)))
		utcfg.LoadFile('ks.cfg')
		options = utcfg.GetOptionsPattern('.path')
		self.assertTrue('/usr/inc/lib' in options)
		self.assertTrue('/usr/inc/share' in options)
		options = utcfg.GetOptionsPattern('.path','share$')
		self.assertTrue('/usr/inc/share' in options)
		self.assertTrue('/usr/inc/lib' not in options)
		self.assertTrue('/usr/share/lib' not in options)
		options = utcfg.GetOptionsPattern('expsection')
		self.assertTrue('value_exp_2'  in options)
		return

	def test_getdefaultvalue(self):
		utcfg = xunit.config.XUnitConfigBase()
		v = utcfg.GetValue('no_section','no_option','no_value')
		self.assertTrue(v == 'no_value')
		utcfg.LoadFile('ks.cfg')
		v = utcfg.GetValue('no_section','no_option','no_value')
		self.assertTrue(v == 'no_value')
		return

	def test_casesensitive(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.SetValue('Section','Option','Value')
		utcfg.SetValue('section','option','value')

		v = utcfg.GetValue('section','option','')
		self.assertEqual(v,'value')
		v = utcfg.GetValue('Section','Option','')
		self.assertEqual(v,'Value')
		return

	def test_spaceword(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.SetValue('spaces','spcopt','o ',1)
		v = utcfg.GetValue('spaces','spcopt','')
		self.assertEqual(v,'o ')

		return

	def test_spacefile(self):
		utcfg = xunit.config.XUnitConfigBase()
		utcfg.LoadFile('spc.cfg')
		v = utcfg.GetValue('space section','space option','')
		self.assertEqual(v,'o ')
		v = utcfg.GetValue('expand section','expand option','')
		self.assertEqual(v,'o ')
		v = utcfg.GetValue('expand section','expand 2option','')
		self.assertEqual(v,' cc ')
		return

	
		
if __name__ == '__main__':
	if '-v' in sys.argv[1:] or '--verbose' in sys.argv[1:]:
		logging.basicConfig(level=logging.INFO,format="%(levelname)-8s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	unittest.main()

