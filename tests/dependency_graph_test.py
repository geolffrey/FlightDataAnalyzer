from __future__ import print_function

import importlib.util
from pathlib import Path
import unittest
import types

from datetime import datetime

from analysis_engine.node import (DerivedParameterNode, Node, NodeManager, P)
from analysis_engine.dependency_graph import (
    dependency_order,
    graph_nodes,
    indent_tree,
)
from analysis_engine.utils import get_derived_nodes
from analysis_engine import settings

test_data_path = Path(__file__).parent / 'test_data'

def import_module(module_name):
    module_name = Path(module_name)
    path = Path(__file__).resolve().parent / ('%s.py' % module_name)
    spec = importlib.util.spec_from_file_location(f"{module_name.name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod


class MockParam(Node):
    def __init__(self, dependencies=['a'], operational=True):
        self.dependencies = dependencies
        self.operational = operational
        # Hack to allow objects rather than classes to be added
        # to the tree.
        self.__base__ = DerivedParameterNode
        self.__bases__ = [self.__base__]

    def can_operate(self, avail):
        return self.operational

    def derive(self, a=P('a')):
        pass

    def get_derived(self, args):
        pass

    def get_dependency_names(self):
        return self.dependencies


class TestDependencyGraph(unittest.TestCase):

    def assert_order_maintained(self, first, second, msg=None):
        '''
        Test that all elements from second appear in first in the same order.

        first can contain additional items in any places, provided that all the elements
        from second appear in first in the same order.
        '''
        second_set = set(second)
        filtered_first = [item for item in first if item in second_set]
        self.assertEqual(filtered_first, second, msg=msg)

    def setUp(self):
        # nodes found on this aircraft's LFL
        self.lfl_params = [
            'Raw1',
            'Raw2',
            'Raw3',
            'Raw4',
            'Raw5',
        ]

        # nodes found from all the derived params code (top level, not their dependencies)
        #NOTE: For picturing it, it should show ALL raw params required.
        self.derived_nodes = {
            'P4' : MockParam(dependencies=['Raw1', 'Raw2']),
            'P5' : MockParam(dependencies=['Raw3', 'Raw4']),
            'P6' : MockParam(dependencies=['Raw3']),
            'P7' : MockParam(dependencies=['P4', 'P5', 'P6']),
            'P8' : MockParam(dependencies=['Raw5']),
        }
        ##########################################################

    def tearDown(self):
        pass

    def test_indent_tree(self):
        requested = ['P7', 'P8']
        mgr2 = NodeManager({'Start Datetime': datetime.now()}, 10, self.lfl_params,
                           requested, [], self.derived_nodes, {}, {})
        gr = graph_nodes(mgr2)
        gr.node['Raw1']['active'] = True
        gr.node['Raw2']['active'] = False
        gr.node['P4']['active'] = False
        self.assertEqual(
            indent_tree(gr, 'P7', space='__', delim=' ', label=False),
            [' P7',
             '__ [P4]',
             '____ Raw1',
             '____ [Raw2]',
             '__ P5',
             '____ Raw3',
             '____ Raw4',
             '__ P6',
             '____ Raw3',
            ])
        # don't recurse valid parameters...
        self.assertEqual(
            indent_tree(gr, 'P5', label=False, recurse_active=False),
            [])
        self.assertEqual(
            indent_tree(gr, 'P4', label=False, recurse_active=False),
            ['- [P4]',
             '  - [Raw2]',
             ])

        self.assertEqual(
            indent_tree(gr, 'root'),
            ['- root',
             '  - P7 (DerivedParameterNode)',
             '    - [P4] (DerivedParameterNode)',
             '      - Raw1 (HDFNode)',
             '      - [Raw2] (HDFNode)',
             '    - P5 (DerivedParameterNode)',
             '      - Raw3 (HDFNode)',
             '      - Raw4 (HDFNode)',
             '    - P6 (DerivedParameterNode)',
             '      - Raw3 (HDFNode)',
             '  - P8 (DerivedParameterNode)',
             '    - Raw5 (HDFNode)',
            ])

    def test_graph_nodes_using_sample_tree(self):
        requested = ['P7', 'P8']
        mgr2 = NodeManager({'Start Datetime': datetime.now()}, 10, self.lfl_params, requested, [],
                           self.derived_nodes, {}, {})
        gr = graph_nodes(mgr2)
        self.assertEqual(len(gr), 11)
        self.assertEqual(sorted(gr.neighbors('root')), sorted(['P8', 'P7']))

    def test_graph_requesting_all_dependencies_links_root_to_all_requests(self):
        # build list of all nodes as required
        requested = self.lfl_params + list(self.derived_nodes.keys())
        mgr = NodeManager({'Start Datetime': datetime.now()}, 1, self.lfl_params, requested, [],
                          self.derived_nodes, {}, {})
        gr = graph_nodes(mgr)
        # should be linked to all requested nodes
        self.assertEqual(sorted(gr.neighbors('root')), sorted(requested))

    def test_graph_middle_level_depenency_builds_partial_tree(self):
        requested = ['P5']
        mgr = NodeManager({'Start Datetime': datetime.now()}, 1, self.lfl_params, requested, [],
                          self.derived_nodes, {}, {})
        gr = graph_nodes(mgr)
        # should only be linked to P5
        self.assertEqual(list(gr.neighbors('root')), ['P5'])

    def test_graph_nodes_with_duplicate_key_in_lfl_and_derived(self):
        # Test that LFL nodes are used in place of Derived where available.
        # Tests a few of the colours
        class One(DerivedParameterNode):
            # Hack to allow objects rather than classes to be added to the tree.
            __base__ = DerivedParameterNode
            __bases__ = [__base__]
            def derive(self, dep=P('DepOne')):
                pass
        class Four(DerivedParameterNode):
            # Hack to allow objects rather than classes to be added to the tree.
            __base__ = DerivedParameterNode
            __bases__ = [__base__]
            def derive(self, dep=P('DepFour')):
                pass
        one = One('overridden')
        four = Four('used')
        mgr1 = NodeManager({'Start Datetime': datetime.now()}, 10, ['1', '2'], ['2', '4'], [],
                           {'1':one, '4':four},{}, {})
        gr = graph_nodes(mgr1)
        self.assertEqual(len(gr), 5)
        # LFL
        self.assertEqual(list(gr.edges('1')), []) # as it's in LFL, it shouldn't have any edges
        self.assertEqual(gr.node['1'], {'node_type': 'HDFNode'})
        # Derived
        self.assertEqual(list(gr.edges('4')), [('4','DepFour')])
        self.assertEqual(gr.node['4'], {'node_type': 'DerivedParameterNode'})
        # Root
        self.assertEqual(list(gr.successors('root')), ['2','4']) # only the two requested are linked
        self.assertEqual(gr.node['root'], {})

    def test_dependency(self):
        requested = ['P7', 'P8']
        mgr = NodeManager({'Start Datetime': datetime.now()}, 10, self.lfl_params, requested, [],
                          self.derived_nodes, {}, {})
        order, _ = dependency_order(mgr)
        self.assertEqual(order, ['P4', 'P5', 'P6', 'P7', 'P8'])

        """
# Sample demonstrating which nodes have predecessors, successors and so on:
for node in node_mgr.keys():
    print('Node: %s \tPre: %s \tSucc: %s \tNeighbors: %s \tEdges: %s' % (node, gr_all.predecessors(node), gr_all.successors(node), gr_all.neighbors(node), gr_all.edges(node)))

Node: P4 	Pre: ['P7'] 	Succ: ['Raw2', 'Raw1'] 	Neighbors: ['Raw2', 'Raw1'] 	Edges: [('P4', 'Raw2'), ('P4', 'Raw1')]
Node: P5 	Pre: ['P7'] 	Succ: ['Raw3', 'Raw4'] 	Neighbors: ['Raw3', 'Raw4'] 	Edges: [('P5', 'Raw3'), ('P5', 'Raw4')]
Node: P6 	Pre: ['P7'] 	Succ: ['Raw3'] 	Neighbors: ['Raw3'] 	Edges: [('P6', 'Raw3')]
Node: P7 	Pre: [] 	Succ: ['P6', 'P4', 'P5'] 	Neighbors: ['P6', 'P4', 'P5'] 	Edges: [('P7', 'P6'), ('P7', 'P4'), ('P7', 'P5')]
Node: P8 	Pre: [] 	Succ: ['Raw5'] 	Neighbors: ['Raw5'] 	Edges: [('P8', 'Raw5')]
Node: Raw1 	Pre: ['P4'] 	Succ: [] 	Neighbors: [] 	Edges: []
Node: Raw2 	Pre: ['P4'] 	Succ: [] 	Neighbors: [] 	Edges: []
Node: Raw3 	Pre: ['P6', 'P5'] 	Succ: [] 	Neighbors: [] 	Edges: []
Node: Raw4 	Pre: ['P5'] 	Succ: [] 	Neighbors: [] 	Edges: []
Node: Raw5 	Pre: ['P8'] 	Succ: [] 	Neighbors: [] 	Edges: []
Node: Start Datetime 	Pre: [] 	Succ: [] 	Neighbors: [] 	Edges: []
"""

    def test_dependency_with_lowlevel_dependencies_requested(self):
        """ Simulate requesting a Raw Parameter as a dependency. This requires
        the requested node to be removed when it is not at the top of the
        dependency tree.
        """
        requested = ['P7', 'P8', # top level nodes
                     'P4', 'P5', 'P6', # middle level node
                     'Raw3', # bottom level node
                     ]
        mgr = NodeManager({'Start Datetime': datetime.now()}, 10, self.lfl_params + ['Floating'],
                          requested, [], self.derived_nodes, {}, {})
        order, _ = dependency_order(mgr)
        self.assertEqual(order, ['P4', 'P5', 'P6', 'P7', 'P8'])

    def test_dependency_one_path_circular(self):
        '''Test that if one Node can be created using its 2 dependencies, but one of
        them is optional and creates a circular dependency.

          ,-> P1 ~~~~~~~~~> P2 ~~~~~~~~> P3--、
         |      `---> Raw1   `---> Raw2      |
         |                                   |
          `----------------------------------’

        P1 requires Raw1 but tries also P2. P2 requires Raw 2 but also tries P3.
        P3 requires P1. This makes a circular dependency. But we don't want to give up
        here as we could still make P1 from Raw1 only, avoiding the circular path.
        '''
        class P1(DerivedParameterNode):
            @classmethod
            def can_operate(self, avail):
                return 'Raw1' in avail

            def derive(self, P2=P('P2'), raw=P('Raw1')):
                pass

        class P2(DerivedParameterNode):
            @classmethod
            def can_operate(self, avail):
                return 'Raw2' in avail

            def derive(self, P3=P('P3'), raw=P('Raw2')):
                pass

        class P3(DerivedParameterNode):
            @classmethod
            def can_operate(self, avail):
                return 'P1' in avail

            def derive(self, P1=P('P1')):
                pass

        derived_nodes = {
            'P0' : MockParam(dependencies=['P1']),
            'P1' : P1,
            'P2' : P2,
            'P3' : P3,
        }
        requested = ['P0']
        lfl_params = ['Raw1', 'Raw2']

        segment_info = {'Start Datetime': datetime.now(), 'Segment Type': 'START_AND_STOP'}
        mgr = NodeManager(segment_info, 10, lfl_params, requested, [], derived_nodes, {}, {})
        order, _ = dependency_order(mgr)
        self.assertEqual(order, ['P1', 'P3', 'P2', 'P0'])

    def test_invalid_requirement_raises(self):
        lfl_params = []
        requested = ['Moment of Takeoff']
        node_modules = [import_module(Path('dummy_nodes') / 'derived_parameters')]
        # go through modules to get derived nodes
        derived_nodes = get_derived_nodes(node_modules)
        mgr = NodeManager({'Start Datetime': datetime.now()}, 10, lfl_params, requested, [],
                          derived_nodes, {}, {})
        self.assertRaises(ValueError, dependency_order, mgr)

    def test_avoiding_possible_circular_dependency(self):
        # Possible circular dependency which can be avoided:
        # Gear Selected Down depends on Gear Down which depends on Gear Selected Down...!
        lfl_params = ['Airspeed', 'Gear (L) Down', 'Gear (L) Red Warning', 'Altitude STD']
        requested = ['Airspeed At Gear Down Selection']
        aircraft_info = {
            'Aircraft Type': 'aeroplane',
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected_order = [
            'Gear Down Selected', 'Airspeed At Gear Down Selection'
        ]
        self.assert_order_maintained(order, expected_order)

        # try a bigger cyclic dependency on top of the above one

    def _get_dependency_order(self, requested, aircraft_info, lfl_params, segment_info={}):
        if not segment_info:
            segment_info = {
                'Start Datetime': datetime.now(),
                'Segment Type': 'START_AND_STOP',
            }

        rel_path = Path('dummy_nodes')
        pre_processing_modules = ['merge_multistate_parameters', 'merge_parameters']
        node_modules = [
            import_module(rel_path / 'pre_processing' / f'{mod}')
            for mod in pre_processing_modules
        ]
        pre_processing_nodes = get_derived_nodes(node_modules)
        pre_processing_requested = list(pre_processing_nodes.keys())

        node_mgr = NodeManager(
            segment_info, 10, lfl_params,
            pre_processing_requested, [], pre_processing_nodes, aircraft_info, {})
        order, _ = dependency_order(node_mgr)

        modules = {
            rel_path: [
                'derived_parameters', 'flight_phase', 'key_point_values',
                'key_time_instances', 'approaches', 'multistate_parameters',
                'flight_attribute'
            ]
        }
        if aircraft_info['Aircraft Type'] == 'helicopter':
            modules[rel_path / 'helicopter'] = [
                'derived_parameters', 'flight_phase', 'key_point_values',
                'key_time_instances', 'multistate_parameters',
            ]
        node_modules = [
            import_module(path / f'{mod}') for path, mods in modules.items()
            for mod in mods

        ]
        # go through modules to get derived nodes
        derived_nodes = get_derived_nodes(node_modules)
        if requested == []:
            # Use all derived nodes if requested is empty
            requested = [p for p in derived_nodes.keys() if p not in lfl_params]
        node_mgr= NodeManager(segment_info, 10, lfl_params + order,
                              requested, [], derived_nodes, aircraft_info, {})
        order, _ = dependency_order(node_mgr)
        return order

    def test_avoiding_circular_dependency_gear_up_selected(self):
        lfl_params = [
            "Gear (L) Down",
            "Gear (L) On Ground",
            "Gear (L) Red Warning",
            "Gear (N) Down",
            "Gear (N) On Ground",
            "Gear (N) Red Warning",
            "Gear (R) Down",
            "Gear (R) On Ground",
            "Gear (R) Red Warning",
            "Gear On Ground",
            "Gear (*) Red Warning"
        ]
        requested = ['Gear Up Selection',]
        aircraft_info = {'Aircraft Type': 'aeroplane',}
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        expected_order = [
            'Gear Down In Transit', 'Gear Up In Transit', 'Gear In Transit',
            'Gear Up Selected', 'Gear Down Selected', 'Gear Up'
        ]

        self.assert_order_maintained(order, expected_order)

    def test_avoiding_circular_dependency_approach_range(self):
        lfl_params = ['Altitude STD', 'Airspeed', 'Heading']
        requested = ['Approach Range',]
        aircraft_info = {
            'Aircraft Type': 'aeroplane',
            'Precise Positioning': False,
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        expected_order = [
            'Heading Continuous', 'Fast',
            'Altitude STD Smoothed', 'Altitude AAL', 'Altitude AAL For Flight Phases',
            'Airborne', 'Takeoff', 'Takeoff Acceleration Start',
            'Takeoff Roll', 'Grounded', 'Takeoff Runway Heading',
            'Takeoff Roll Or Rejected Takeoff', 'Heading During Takeoff', 'Mach',
            'Heading Rate', 'Mobile', 'Landing', 'Airspeed True', 'Landing Roll',
            'Heading During Landing', 'Vertical Speed', 'Liftoff',
            'Vertical Speed For Flight Phases', 'Level Flight', 'Approach',
            'Approach And Landing', 'ILS Localizer', 'Roll', 'Touchdown',
            'Approach Information', 'FDR Landing Runway', 'Approach Range'
        ]
        self.assert_order_maintained(order, expected_order)

    def test_avoiding_circular_dependency_latitude_smoothed(self):
        lfl_params = ['Altitude STD', 'Airspeed', 'Heading', 'Latitude', 'Longitude']
        requested = ['Latitude Smoothed',]
        aircraft_info = {
            'Aircraft Type': 'aeroplane',
            'Precise Positioning': False,
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        expected_order = [
            'Heading Continuous',
            'ILS Localizer', 'Fast',
            'Altitude STD Smoothed', 'Altitude AAL', 'Magnetic Variation',
            'Altitude AAL For Flight Phases', 'Airborne', 'Takeoff',
            'Takeoff Acceleration Start', 'Takeoff Roll', 'Grounded',
            'Takeoff Runway Heading', 'Takeoff Roll Or Rejected Takeoff',
            'Heading During Takeoff', 'Mach', 'Heading Rate', 'Mobile', 'Landing',
            'Airspeed True', 'Landing Roll', 'Heading During Landing', 'Vertical Speed',
            'Liftoff', 'Latitude At Liftoff', 'Longitude At Liftoff', 'Off Blocks',
            'Latitude Off Blocks', 'Longitude Off Blocks', 'FDR Takeoff Airport',
            'Latitude At Takeoff Acceleration Start',
            'Longitude At Takeoff Acceleration Start', 'FDR Takeoff Runway',
            'Vertical Speed For Flight Phases', 'Level Flight', 'Approach',
            'Approach And Landing', 'Touchdown', 'Latitude At Touchdown',
            'Longitude At Touchdown', 'Roll', 'Approach Information',
            'FDR Landing Runway', 'Magnetic Variation From Runway', 'Heading True',
            'Approach Range', 'Heading True Continuous', 'Latitude Smoothed'
        ]
        self.assert_order_maintained(order, expected_order)

    def test_avoiding_circular_dependency_latitude_smoothed_helicopter(self):
        lfl_params = ['Altitude STD', 'Airspeed', 'Heading', 'Latitude', 'Longitude']
        requested = ['Latitude Smoothed',]
        aircraft_info = {
            'Aircraft Type': 'helicopter',
            'Precise Positioning': False,
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected_order = [
            'Heading Continuous',
            'ILS Localizer', 'Altitude STD Smoothed',
            'Vertical Speed', 'Heading Rate', 'Mobile',
            'Off Blocks', 'Latitude Off Blocks', 'Longitude Off Blocks',
            'FDR Takeoff Airport', 'Mach', 'Airspeed True', 'Latitude Smoothed',
            'Longitude Smoothed'
        ]
        self.assert_order_maintained(order, expected_order)

    def test_avoiding_circular_dependency_fdr_landing(self):
        lfl_params = [
            'Altitude STD', 'Altitude Radio', 'Airspeed', 'Heading', 'Latitude',
            'Longitude', 'Gear (L) On Ground', 'Collective',
        ]
        requested = ['FDR Landing Airport',]
        aircraft_info = {
            'Aircraft Type': 'helicopter',
            'Precise Positioning': False,
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected_order = [
            'Altitude STD Smoothed',
            'Vertical Speed', 'Gear On Ground',
            'Altitude AGL', 'Heading Continuous', 'Heading Rate',
            'Airborne', 'Mobile', 'Landing',
            'Approach', 'Approach And Landing', 'ILS Localizer', 'Touchdown',
            'Latitude At Touchdown', 'Longitude At Touchdown', 'Altitude ADH',
            'Liftoff', 'Takeoff', 'Approach Information', 'FDR Landing Airport'
        ]
        self.assert_order_maintained(order, expected_order)

    def test_avoiding_circular_dependency_approach_information_helicopter(self):
        lfl_params = [
            'Altitude STD', 'Altitude AGL', 'Altitude Radio', 'Airspeed', 'Heading',
            'Latitude', 'Longitude', 'Gear (L) On Ground', 'Collective',
        ]
        requested = ['Approach Information',]
        aircraft_info = {'Aircraft Type': 'helicopter', 'Precise Positioning': False}
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected_order = [
            'Gear On Ground', 'Heading Continuous',
            'Heading Rate', 'Airborne', 'Mobile',
            'Landing', 'Approach', 'Approach And Landing', 'ILS Localizer',
            'Touchdown', 'Latitude At Touchdown', 'Longitude At Touchdown',
            'Liftoff', 'Takeoff', 'Approach Information'
        ]
        self.assert_order_maintained(order, expected_order)

    def test_avoiding_all_circular_dependencies_by_having_nothing_recorded(self):
        # not realistic use case; but let's see if we can avoid all circular dependencies in the theoretical deriving tree structure things
        lfl_params = []#['Altitude STD', 'Airspeed', 'Heading'] # Core parameters
        aircraft_info = {'Aircraft Type': 'aeroplane',}
        requested = []
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected = [
            'Grounded', 'Eng Start', 'FDR Analysis Datetime',
            'FDR Takeoff Datetime', 'FDR Flight Type', 'FDR Version'
        ]
        self.assertTrue(set(order) >= set(expected))

    def _example_recorded_parameters(self):
        # A more realistic tree, for finding circular dependencies, using the
        # recorded parameter names and aircraft_info (de-identified) from AE-214.
        # Segment Hash: 141ef6749191d5aecb6b3dc5f6d2c341276aa9bce61ee38b1f5ccf4f825329f4
        aircraft_info = {
            'Aircraft Type': 'aeroplane',
            'Data Type': None,
            'QAR Serial Number': '',
            'Data Source': 'FDR',
            'Ground To Lowest Point Of Tail': 2.57712,
            'Dry Operating Weight': None, 'Data Rate': 256,
            'Fleet Code': None,
            'Engine Count': 2,
            'Engine Manufacturer': 'CFM International',
            'Frame Type': None,
            'Modifications': [],
            'Tail Number': None,
            'Precise Positioning': True,
            'Recorder Name': 'MEDIAPREP',
            'Main Gear To Lowest Point Of Tail': 9.8234,
            'Frame Doubled': False,
            'Engine Series': 'CFM56-7B',
            'Model': 'B737-7CN(BBJ)',
            'Identifier': '',
            'Frame Name': '737-3A',
            'Family': 'B737 NG',
            'Series': 'B737-700',
            'Frame': '737-3A',
            'Engine Propulsion': 'JET',
            'Manufacturer Serial Number': None,
            'Processing Format': 'tdwgl',
            'Stretched': None,
            'Main Gear To Radio Altimeter Antenna': None,
            'Engine Type': 'CFM56-7B26',
            'Manufacturer': 'Boeing',
            'Payload': None,
            'Maximum Landing Weight': None
        }
        path = Path(test_data_path) / 'dependency_graph_example_recorded_lfl_parameters.txt'
        lfl_params = path.read_text().splitlines()
        # Pre-processed order
        lfl_params.extend(['Gear Down', 'Latitude Prepared', 'Longitude Prepared', 'Aircraft Type'])
        return aircraft_info, lfl_params

    def test_avoiding_all_circular_dependencies_with_recorded_lfls(self):
        aircraft_info, lfl_params = self._example_recorded_parameters()
        requested = []
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        path = Path(test_data_path) / 'dependency_graph_example_recorded_expected.txt'
        expected = path.read_text().splitlines()

        self.assert_order_maintained(order, expected)
        self.assertTrue(set(order) >= set(expected))

    def test_acceleration_normal_offset_processing_order(self):
        # In the past, the KPV 'Acceleration Normal Offset' got straved out of
        # the dependency processing order as 'Acceleration Normal Offset Removed'
        # could be derived without it. Test to ensure that the dependency tree
        # order doesn't do that again
        aircraft_info, lfl_params = self._example_recorded_parameters()
        requested = []
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        self.assertIn('Acceleration Normal Offset', order)
        self.assertIn('Acceleration Normal Offset Removed', order)
        self.assertLess(order.index('Acceleration Normal Offset'),
                        order.index('Acceleration Normal Offset Removed'))

    def test_acceleration_lateral_offset_processing_order(self):
        # In the past, the KPV 'Acceleration Lateral Offset' got straved out of
        # the dependency processing order as 'Acceleration Lateral Offset Removed'
        # could be derived without it. Test to ensure that the dependency tree
        # order doesn't do that again
        aircraft_info, lfl_params = self._example_recorded_parameters()
        requested = []
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        self.assertIn('Acceleration Lateral Offset', order)
        self.assertIn('Acceleration Lateral Offset Removed', order)
        self.assertLess(order.index('Acceleration Lateral Offset'),
                        order.index('Acceleration Lateral Offset Removed'))

    def test_processing_order_magnetic_variation_from_runway(self):
        # In the past Magnetic Variation From Runway failed to the derived at
        # the right time (happened latter in the order). As a result Heading
        # True just used Magnetic Variation.
        # Test ensures that:
        # 'Magnetic Variation' created before 'Magnetic Variation From Runway'
        # 'Magnetic Variation From Runway' created before 'Heading True'.
        aircraft_info, lfl_params = self._example_recorded_parameters()
        requested = []
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)
        self.assertIn('Heading True', order)
        self.assertIn('Magnetic Variation From Runway', order)
        self.assertIn('Magnetic Variation', order)
        # Magnetic Variation From Runway must be derived before Heading True
        self.assertLess(order.index('Magnetic Variation From Runway'),
                        order.index('Heading True'))
        # Magnetic Variation must be derived before Magnetic Variation From Runway
        self.assertLess(order.index('Magnetic Variation'),
                        order.index('Magnetic Variation From Runway'))

    def test_processing_order_approach_and_landing(self):
        lfl_params = ['Altitude STD', 'Airspeed','Heading']
        requested = ['Approach And Landing',]
        aircraft_info = {
            'Aircraft Type': 'aeroplane',
            'Precise Positioning': False,
            'Frame': 'dummy_LFL'  # Needed for Altitude STD Smoothed, although not needed in derive method!
        }
        order = self._get_dependency_order(requested, aircraft_info, lfl_params)

        expected_order = [
            'Fast', 'Altitude STD Smoothed', 'Altitude AAL',
            'Altitude AAL For Flight Phases', 'Airborne', 'Vertical Speed For Flight Phases',
            'Level Flight', 'Heading Continuous', 'Heading Rate', 'Takeoff',
            'Takeoff Acceleration Start', 'Takeoff Roll', 'Grounded',
            'Takeoff Runway Heading', 'Takeoff Roll Or Rejected Takeoff',
            'Heading During Takeoff', 'Mach', 'Landing', 'Airspeed True', 'Landing Roll',
            'Heading During Landing', 'Vertical Speed', 'Liftoff', 'Approach And Landing',
            'ILS Localizer', 'Roll', 'Touchdown', 'Approach Information',
            'FDR Landing Runway', 'Mobile', 'Approach'
        ]
        self.assert_order_maintained(order, expected_order)


if __name__ == '__main__':
    unittest.main()

