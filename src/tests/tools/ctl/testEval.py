import unittest

from pynusmv.fsm.bddFsm import BddFsm
from pynusmv.dd.bdd import BDD
from pynusmv.init.init import init_nusmv, deinit_nusmv
from pynusmv.parser.parser import parse_simple_expression as parseSexp
from pynusmv.spec.spec import Spec

from tools.ctl.eval import eval_ctl


class TestEval(unittest.TestCase):
    
    def setUp(self):
        init_nusmv()
    
    def tearDown(self):
        deinit_nusmv()
    
    
    def init_model(self):
        fsm = BddFsm.from_filename("tests/tools/ctl/admin.smv")
        self.assertIsNotNone(fsm)
        return fsm
        

    def test_atom(self):
        fsm = self.init_model()
        
        anspec = Spec(parseSexp("admin = none"))
        an = eval_ctl(fsm, anspec)
        self.assertIsNotNone(an)
        self.assertTrue(fsm.init <= an)
        
        aaspec = Spec(parseSexp("admin = alice"))
        aa = eval_ctl(fsm, aaspec)
        self.assertIsNotNone(aa)
        self.assertTrue((fsm.init & aa).is_false())
        self.assertTrue((aa & an).is_false())