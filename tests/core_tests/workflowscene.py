'''
Created on Mar 14, 2013

@author: hsorby
'''
import unittest

from PyQt4 import QtCore

from core.workflowscene import WorkflowScene, MetaStep

class DumbManager(object):
    pass

class DumbStep(object):
    pass

class WorkflowSceneTestCase(unittest.TestCase):


    def testCreate(self):
        
        s = WorkflowScene(DumbManager())
        self.assertIsNotNone(s)

    def testItemAPI(self):
        
        item = MetaStep(DumbStep())
        s = WorkflowScene(DumbManager())
        s.addItem(item)
        self.assertEqual(len(s._items), 1)
        s.setItemPos(item, QtCore.QPoint(344, 404))
        self.assertEqual(s._items[item]._pos.x(), 344)
        self.assertEqual(s._items[item]._pos.y(), 404)
        s.setItemSelected(item, False)
        self.assertFalse(s._items[item]._selected)
        s.removeItem(item)
        self.assertEqual(len(s._items), 0)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()