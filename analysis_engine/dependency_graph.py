from __future__ import print_function

import os
import logging
import networkx as nx # pip install networkx or /opt/epd/bin/easy_install networkx
import six
import copy

from collections import deque, Counter
from itertools import chain

from analysis_engine.node import (
    ApproachNode,
    DerivedParameterNode,
    MultistateDerivedParameterNode,
    FlightAttributeNode,
    FlightPhaseNode,
    KeyPointValueNode,
    KeyTimeInstanceNode,
)

logger = logging.getLogger(__name__)

CALCULATE_NODE_LAST = [
    '2 Deg Pitch To 35 Ft Duration',
]

"""
TODO:
=====

* Getting important: Circular dependencies need to have a priority to determine which order to evaluate a node's successors.

node_succ_dict is a dictionary which is iterated over when using
node.successors() in dependencies3(). If somewhere in each of a node's
successor's tree there is a circular dependency to another one of the node's
successor's tree (i.e. we're at the node which can make the choice which
circular dependant to process first) we can evaluate a priority. Is it more
important to process Groundspeed using just Gspd (1) first so that Latitude
can use Groundspeed for smoothing??



before Latitude Lat/Long or is it more important to
calculate the Lat/Long from the Groundspeed? The priority should include the
fact that if a parameter is recorded, it is already available.

Q:

* Nice to have: reverse digraph to get arrows poitning towards the root - use
  pre's rather than successors in tree traversal
"""


class InoperableDependencies(KeyError):
    ##def __init__(self, inoperable):
        ##self.inoperable = inoperable
    pass


class RequiredNodesMissing(KeyError):
    pass


def print_ordered_tree(tree_path):
    '''
    This is tool that prints the order and the intended tree in which nodes are traversed.
    It shows:
    -	The path depth that the node appears
    -	Where the node will be included into the process_order. It will show the number in the processing order that the node will be created, indicated by Node Name (order)
    -	If node's dependencies not satisfied the can_operate, indicated by [Node Name] (INOP)
    -	If node reappears into the tree path (a circular dependency), indicated by <<< Node Name CIRCULAR >>>

    example:
    6:							- <<< 'Gear Up In Transit CIRCULAR' >>> (438) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear Up' > 'Gear Up In Transit'><<< 'Gear Up In Transit' CIRCULAR >>>
    5:						- ['Gear Position'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear Up' > 'Gear Position'
    4:					- ['Gear Up'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear Up'
    6:							- <<< 'Gear Up In Transit' CIRCULAR >>> (439) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear In Transit' > 'Gear Up In Transit'><<< Gear Up In Transit CIRCULAR >>>
    4:					- ['Gear In Transit'] (INOP) 	 'root'>'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear In Transit'
    5:						- ['Gear (L) Red Warning'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear (*) Red Warning' > 'Gear (L) Red Warning'
    5:						- ['Gear (N) Red Warning'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear (*) Red Warning' > 'Gear (N) Red Warning'
    5:						- ['Gear (R) Red Warning'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear (*) Red Warning' > 'Gear (R) Red Warning'
    4:					- ['Gear (*) Red Warning'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear (*) Red Warning'
    4:					- ['Gear Position'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit' > 'Gear Position'
    3:				- ['Gear Up In Transit'] (INOP) 	 'root' > 'Mach While Gear Retracting Max' > 'Gear Retracting' > 'Gear Up In Transit'
    2:			- ['Gear Retracting'] (INOP) 	 'root' > 'Mach While Gear Retracting Max > Gear Retracting'
    1:		- ['Mach While Gear Retracting Max'] (INOP) 	 'root' > 'Mach While Gear Retracting Max'
    1:		- 'Turbulence During Cruise Max' (440) 	 'root' > 'Turbulence During Cruise Max'
    0:	- 'root' (713) 	 'root'
    '''
    for line in format_ordered_tree(tree_path):
        print(line[:-1])

def format_ordered_tree(tree_path):
    order = 0
    lines = []
    tree = copy.deepcopy(tree_path)
    for path in tree[:]:
        if path[-1] == 'NOT OPERATIONAL':
            path.pop()
            lines.append("%d:%s- ['%s'] (INOP) \t '%s'\n" % (len(path)-1, '\t'*len(path), path[-1], "' > '".join(path)))
        elif path[-1] == 'CIRCULAR':
            path.pop()
            lines.append("%d:%s- <<< '%s' CIRCULAR >>> \t '%s' ><<< '%s' CIRCULAR >>>\n" % (len(path)-1, '\t'*len(path), path[-1], "' > '".join(path), path[-1]))
        else:
            lines.append("%d:%s- '%s' (%d) \t '%s'\n" % (len(path)-1, '\t'*len(path), path[-1], order, "' > '".join(path)))
            order += 1
    return lines

def ordered_tree_to_file(tree_path, name='ordered_tree_path.txt'):
    '''
    Same as print_ordered_tree but to file.
    '''
    with open(name, 'w') as f:
        f.writelines(format_ordered_tree(tree_path))


def indent_tree(graph, node, level=0, space='  ', delim='- ', label=True,
                recurse_active=True):
    '''
    Small tool to assist representing a tree on the console.

      print('\n'.join(indent_tree(gr_all, 'root')))

      - root
        - sub1
          - sub2
        - sub3

    :param graph: Entire graph
    :type graph: nx.DiGraph
    :param node: Node to start recursing successors from
    :type node: String/object
    :param level: Current indent level down the tree
    :type level: Int
    :param space: Multiplied by indent level
    :type space: String
    :param delim: Delimiter between space and name
    :type delim: String
    :param label: Whether to add labels about the node type
    :type label: Boolean
    :param recurse_active: Whether to show the tree for active params
    :type recurse_active: Boolean
    '''

    def recurse_tree(node, level):
        if node in path:
            # circular dependency started!
            path.append(node)
            return ['<<Circular Depenency to: %s>>' % node]
        path.append(node)
        if graph.node[node].get('active', True):
            if recurse_active:
                node_repr = node
            else:
                return []
        else:
            node_repr = '[%s]' % node
        node_type = graph.node[node].get('node_type')
        if node_type and label:
            node_repr = '%s (%s)' % (node_repr, node_type)
        row = '%s%s%s' % (space*level, delim, node_repr)
        level_rows = [row]
        for succ in sorted(graph.successors(node)):
            sub_level = recurse_tree(succ, level=level+1)
            path.pop()
            level_rows.extend(sub_level)
        return level_rows

    path = deque()  # current branch path
    return recurse_tree(node, level)


def print_tree(graph, node='root', **kwargs):
    '''
    Helper to shortcut printing of indent_tree.

    See indent_tree for help with args/kwargs.
    '''
    print('\n'.join(indent_tree(graph, node, **kwargs)))


def dependencies3(di_graph, root, node_mgr, dependency_tree_log=False):
    '''
    Performs a Depth First Search down each dependency node in the tree
    (di_graph) until each branch's dependencies are best satisfied.

    Avoids circular dependencies within the DiGraph by building up a path of
    the nodes visited down the current depth search. If encountering a
    node already visited (in the path) two things can happen. Either the node could
    still be derived from other dependencies not already in the path. In that case,
    we try to derive it with the remaining dependencies. Or we have used all possible
    combinations and none worked. This node is declared unavailable at this level of
    the search path. Cycles encountered are recorded. If encountered more than once,
    it means that the nodes within the cycles are permanently inoperative. This
    speeds up the graph traversal by avoiding cycles we have already seen before.

    e.g.
    Heading -> Heading True + Magnetic Variation
    Heading True -> Heading - Magnetic Variation

    :param di_graph: Directed graph of all nodes and their dependencies.
    :type di_graph: nx.DiGraph
    :param root: Root node to start traversing from, usually named 'root'
    :type root: String
    :param node_mgr: Node manager which can assess whether nodes are
                     operational with the available dependencies at each
                     layer of the tree.
    :type node_mgr: analysis_engine.node.NodeManager
    :dependency_tree_log: If True, will populate `tree_path` for visualization of the
                          graph traversal.
    '''
    def traverse_tree(node):
        """
        Begin the recursion at this node's position in the dependency tree

        Returns True if this node dependencies are satisfied. False otherwise.
        """
        path.append(node)

        if node in active_nodes:
            # node already discovered operational
            return True

        # order the successors based on the order in the derive method.
        ordered_successors = [
            name
            for (name, d) in sorted(
                di_graph[node].items(), key=lambda a: (a[1].get("order", False), a[0])
            )
            if name not in inop_nodes
        ]

        # Optimization: check if node can be derived with potential dependencies.
        # Because of this, we must have all required nodes connected to the root,
        # as we might not visit all dependencies.
        if not node_mgr.operational(node, ordered_successors):
            inop_nodes.add(node)
            return False

        if node in path[:-1]:
            # Start of circular dependency.
            # There might still be a chance to derive this node based on its remaining
            # successors. Try again with subset of successors (ignore those in path)
            ordered_successors = [
                name for name in ordered_successors
                if name not in path
            ]

            if not node_mgr.operational(node, ordered_successors):
                # Unfortunately the remaining successors do not allow this node to
                # be derived. Back track.
                # Optimization
                # Find the cycle within the current path
                last_path = list(path)
                start = last_path.index(node)
                stop = len(last_path) - 1  # Because we appear also at the end
                cycle = tuple(last_path[start:stop])
                if cycle in cycles:
                    # If we've seen this cycle before, its parameters will never work
                    inop_nodes.update(cycle)
                else:
                    cycles.add(cycle)

                if dependency_tree_log:
                    tree_path.append(list(path) + ['CIRCULAR',])
                logger.debug("Circular dependency avoided at node '%s'. Branch path: %s", node, path)
                return False

        operating_dependencies = set()  # operating nodes of current node's available dependencies
        for dependency in ordered_successors:
            # recurse to find out if the dependency is available
            if traverse_tree(dependency):
                operating_dependencies.add(dependency)
            # each time traverse_tree returns, remove node from visited path
            path.pop()

        if node_mgr.operational(node, operating_dependencies):
            # node will work at this level with the operating dependencies
            if node not in active_nodes:
                active_nodes.add(node)
                ordering.append(node)  # What about skipping nodes in node_mgr.hdf_keys (they don't derive)

            if node not in node_mgr.hdf_keys and dependency_tree_log:
                tree_path.append(list(path))

            return True
        else:
            if dependency_tree_log:
                tree_path.append(list(path) + ['NOT OPERATIONAL',])
            return False

    ordering = []
    path = []  # current branch path
    active_nodes = set(              # operational nodes visited for fast lookup
        chain.from_iterable((
            node_mgr.aircraft_info,
            node_mgr.achieved_flight_record,
            node_mgr.segment_info
        ))
    )
    inop_nodes = set()  # non operational nodes due to insatisfied dependencies
    tree_path = []  # For viewing the tree in which nodes are added to path
    cycles = set()  # set of cycles already seen
    traverse_tree(root)  # start recursion
    logger.debug(f"Inop nodes: {inop_nodes}")
    return ordering, tree_path


def graph_adjacencies(graph):
    '''
    Create a dictionary of each nodes adjacencies within the graph. Useful for
    JIT javascript presentation of the tree.

    :param graph: Dependency tree graph
    :type graph: nx.Graph
    :returns: Restructured graph
    '''
    data = []
    for n,nbrdict in graph.adjacency():
        # build the dict for this node
        d = dict(id=n, name=graph.node[n].get('label', n), data=graph.node[n])
        adj = []
        for nbr, nbrd in nbrdict.items():
            adj.append(dict(nodeTo=nbr, data=nbrd))
        d['adjacencies'] = adj
        data.append(d)
    return data


def graph_nodes(node_mgr):
    """
    :param node_mgr:
    :type node_mgr: NodeManager
    """
    # gr_all will contain all nodes
    gr_all = nx.DiGraph()
    # create nodes without attributes now as you can only add attributes once
    # (limitation of add_node_attribute())
    gr_all.add_nodes_from(node_mgr.hdf_keys, color='#72f4eb', # turquoise
                          node_type='HDFNode')
    derived_minus_lfl = {k: v for k, v in node_mgr.derived_nodes.items() if k not in node_mgr.hdf_keys}
    # Group into node types to apply colour. TODO: Make colours less garish.
    colors = {
        ApproachNode: '#663399', # purple
        MultistateDerivedParameterNode: '#2aa52a', # dark green
        DerivedParameterNode: '#72cdf4',  # fds-blue
        FlightAttributeNode: '#b88a00',  # brown
        FlightPhaseNode: '#d93737',  # red
        KeyPointValueNode: '#bed630',  # fds-green
        KeyTimeInstanceNode: '#fdbb30',  # fds-orange
    }
    derived_nodes = []
    for name, node in derived_minus_lfl.items():
        # the default is gray, if you see it, something is wrong
        color = '#888888'
        for base in node.__bases__:
            if base in colors:
                color = colors[base]
                break

        node_info = (name, {'color': color,
                            'node_type': node.__base__.__name__})
        derived_nodes.append(node_info)
    gr_all.add_nodes_from(derived_nodes)

    # build list of dependencies
    derived_deps = set()  # list of derived dependencies
    for node_name, node_obj in six.iteritems(derived_minus_lfl):
        derived_deps.update(node_obj.get_dependency_names())
        # Create edges between node and its dependencies
        edges = []
        for (n, dep) in enumerate(node_obj.get_dependency_names()):
            edges.append((node_name, dep, {'order':n}))
        gr_all.add_edges_from(edges)

    # add root - the top level application dependency structure based on required nodes
    gr_all.add_node('root', color='#ffffff')
    root_edges = []
    for node_req in node_mgr.requested:
        # Add all requested nodes to the root
        root_edges.append(('root', node_req))

    gr_all.add_edges_from(root_edges) ##, color='red')

    #TODO: Split this up into the following lists of nodes
    # * LFL used
    # * LFL unused
    # * Derived used
    # * Derived not operational
    # * Derived not used -- coz not referenced by a dependency kpv etc therefore not part of the spanning tree

    # Note: It's hard to tell whether a missing dependency is a mistyped
    # reference to another derived parameter or a parameter not available on
    # this LFL
    # Set of all derived and LFL Nodes.
    ##available_nodes = set(node_mgr.derived_nodes.keys()).union(set(node_mgr.hdf_keys))
    available_nodes = set(node_mgr.keys())
    # Missing dependencies.
    missing_derived_dep = list(derived_deps - available_nodes)
    # Missing dependencies which are requested.
    missing_requested = list(set(node_mgr.requested) - available_nodes)

    if missing_derived_dep:
        logger.warning("Found %s dependencies which don't exist in LFL or Node modules.", len(missing_derived_dep))
        logger.debug("The missing dependencies: %s", missing_derived_dep)
    if missing_requested:
        raise ValueError("Missing requested parameters: %s" % missing_requested)

    # Add missing nodes to graph so it shows everything. These should all be
    # RAW parameters missing from the LFL unless something has gone wrong with
    # the derived_nodes dict!
    gr_all.add_nodes_from(missing_derived_dep, color='#6a6e70')  # fds-grey

    return gr_all


def process_order(gr_all, node_mgr, raise_inoperable_requested=False,
                  dependency_tree_log=False):
    """
    :param gr_all:
    :type gr_all: nx.DiGraph
    :param node_mgr:
    :type node_mgr: NodeManager
    :returns:
    :rtype:
    """
    process_order, tree_path = dependencies3(
        gr_all, 'root', node_mgr, dependency_tree_log=dependency_tree_log)
    logger.debug("Processing order of %d nodes is: %s", len(process_order), process_order)
    if dependency_tree_log:
        ordered_tree_to_file(tree_path, name=dependency_tree_log)
    for n, node in enumerate(process_order):
        gr_all.node[node]['label'] = '%d: %s' % (n, node)
        gr_all.node[node]['active'] = True

    inactive_nodes = set(gr_all.nodes()) - set(process_order)
    logger.debug("Inactive nodes: %s", list(sorted(inactive_nodes)))
    gr_st = gr_all.copy()
    gr_st.remove_nodes_from(inactive_nodes)

    for node in inactive_nodes:
        # add attributes to the node to reflect it's inactivity
        gr_all.node[node]['color'] = '#c0c0c0'  # silver
        gr_all.node[node]['active'] = False
        inactive_edges = gr_all.in_edges(node)
        gr_all.add_edges_from(inactive_edges, color='#c0c0c0')  # silver

    inoperable_requested = list(set(node_mgr.requested) - set(process_order))
    if inoperable_requested:
        logger.warning("Found %s inoperable requested parameters.", len(inoperable_requested))
        if logging.NOTSET < logger.getEffectiveLevel() <= logging.DEBUG:
            # only build this massive tree if in debug!
            items = []
            for n in sorted(inoperable_requested):
                tree = indent_tree(gr_all, n, recurse_active=False)
                if tree:
                    items.append('------- INOPERABLE -------')
                    items.extend(tree)
            logger.debug('\n'+'\n'.join(items))
        if raise_inoperable_requested:
            raise InoperableDependencies(inoperable_requested)

    required_missing = set(node_mgr.required) - set(process_order)
    if required_missing:
        raise RequiredNodesMissing(
            "Required nodes missing: %s" % ', '.join(required_missing))

    return gr_all, gr_st, process_order[:-1] # exclude 'root'


def dependency_order(node_mgr, raise_inoperable_requested=False, dependency_tree_log=False):
    """
    Main method for retrieving processing order of nodes.

    :param node_mgr:
    :type node_mgr: NodeManager
    :param draw: Will draw the graph. Green nodes are available LFL params, Blue are operational derived, Black are not requested derived, Red are active top level requested params, Grey are inactive params. Edges are labelled with processing order.
    :type draw: boolean
    :returns: List of Nodes determining the order for processing and the spanning tree graph.
    :rtype: (list of strings, dict)
    """
    _graph = graph_nodes(node_mgr)
    gr_all, gr_st, order = process_order(_graph, node_mgr,
                                         raise_inoperable_requested=raise_inoperable_requested,
                                         dependency_tree_log=dependency_tree_log)

    return order, gr_st
