'''
Created on Mar 14, 2013

@author: hsorby
'''
import unittest

from PyQt4 import QtCore

from core.workflowscene import WorkflowScene, WorkflowDependencyGraph, MetaStep, Connection, _findAllPaths, _findPath, _findHead, _findTail

class DumbManager(object):
    pass


class DumbStep(object):
    
    def isConfigured(self):
        return True


class WorkflowSceneTestCase(unittest.TestCase):


    def testCreate(self):
        
        s = WorkflowScene(DumbManager())
        self.assertTrue(s != None)

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
       

class WorkflowDependencyGraphTestCase(unittest.TestCase):
    

    def setUp(self):
        self._s =  WorkflowScene(DumbManager())
        self._nodes = []
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        self._nodes.append(MetaStep(DumbStep()))
        
    def tearDown(self):
        self._s.clear()
        self._nodes = []
           
    def testCreate(self):
        g = WorkflowDependencyGraph(self._s)
        self.assertTrue(g != None)
        
    def testGraph1(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], self._nodes[1])
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(c1)
        
        self.assertTrue(g.canExecute())
        g._calculateGraph()
        self.assertEqual(len(g._graph), 2)
        self.assertEqual(g._graph[0], self._nodes[0])
        self.assertEqual(g._graph[1], self._nodes[1])

    def testGraph2(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], self._nodes[1])
        c2 = Connection(self._nodes[1], self._nodes[2])
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(c1)
        self._s.addItem(c2)
        
        self.assertTrue(g.canExecute())
        g._calculateGraph()
        self.assertEqual(len(g._graph), 3)
        self.assertEqual(g._graph[0], self._nodes[0])
        self.assertEqual(g._graph[1], self._nodes[1])
        self.assertEqual(g._graph[2], self._nodes[2])

    def testGraph3(self):
        g = WorkflowDependencyGraph(self._s)
        c1 = Connection(self._nodes[0], self._nodes[1])
        c2 = Connection(self._nodes[1], self._nodes[2])
        c3 = Connection(self._nodes[2], self._nodes[3])
        self._s.addItem(self._nodes[0])
        self._s.addItem(self._nodes[1])
        self._s.addItem(self._nodes[2])
        self._s.addItem(self._nodes[3])
        self._s.addItem(c3)
        self._s.addItem(c1)
        self._s.addItem(c2)
        
        self.assertTrue(g.canExecute())
        g._calculateGraph()
        self.assertEqual(len(g._graph), 4)
        self.assertEqual(g._graph[0], self._nodes[0])
        self.assertEqual(g._graph[1], self._nodes[1])
        self.assertEqual(g._graph[2], self._nodes[2])
        self.assertEqual(g._graph[3], self._nodes[3])
        
class GraphUtilitiesTestCase(unittest.TestCase):
    
    
    _graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

    def testFindPath(self):
        path = _findPath(self._graph, 'A', 'D')
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        
    def testFindPath1(self):
        path = _findPath(self._graph, 'A', 'G')
        self.assertEqual(path, [])
        
    def testFindAllPath(self):
        path = _findAllPaths(self._graph, 'A', 'D')
        self.assertEqual(path, [['A', 'B', 'C', 'D'], ['A', 'B', 'D'], ['A', 'C', 'D']])
        
    def testFindHead1(self):
        head = _findHead(self._graph, 'C')
        self.assertTrue(head in ['A', 'E'])
        
    def testFindTail1(self):
        tail = _findTail(self._graph, 'C')
        self.assertEqual(tail, 'D')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()