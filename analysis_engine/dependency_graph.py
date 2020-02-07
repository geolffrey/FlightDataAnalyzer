import copy
import logging
import types

import networkx as nx

logger = logging.getLogger(__name__)


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


def indent_tree(graph, node, level=0, space='  ', delim='- ', label=True, recurse_active=True):
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

    path = []  # current branch path
    return recurse_tree(node, level)


def print_tree(graph, node='root', **kwargs):
    '''
    Helper to shortcut printing of indent_tree.

    See indent_tree for help with args/kwargs.
    '''
    print('\n'.join(indent_tree(graph, node, **kwargs)))


def traverse_tree(state, node_mgr, graph, node, dependency_tree_log=False):
    """
    Begin the recursion at this node's position in the dependency tree

    Returns True if this node dependencies are satisfied. False otherwise.
    """
    if node in state.active_nodes:
        return True  # Node already found to be operational.

    successors = [name for name in graph[node] if name not in state.inop_nodes]

    # Optimization: check if node can be derived with potential dependencies.
    # Because of this, we must have all required nodes connected to the root,
    # as we might not visit all dependencies.
    if not successors or not node_mgr.operational(node, successors):
        state.inop_nodes.add(node)
        return False

    if node in state.path:
        # Start of circular dependency.
        # There might still be a chance to derive this node based on its remaining
        # successors. Try again with subset of successors (ignore those in path)
        successors = [name for name in successors if name not in state.path]

        if not successors or not node_mgr.operational(node, successors):
            # Unfortunately the remaining successors do not allow this node to
            # be derived. Back track.
            # Optimization
            # Find the cycle within the current path
            start = state.path.index(node)
            cycle = tuple(state.path[start:])
            if cycle in state.cycles:
                # If we've seen this cycle before, its parameters will never work
                state.inop_nodes.update(cycle)
            else:
                state.cycles.add(cycle)

            if dependency_tree_log:
                state.tree_path.append(state.path + [node, 'CIRCULAR'])
            logger.debug("Circular dependency avoided at node '%s'. Branch path: %s", node, state.path)
            return False

    state.path.append(node)

    operating_dependencies = set()  # operating nodes of current node's available dependencies
    for dependency in successors:
        # recurse to find out if the dependency is available
        if traverse_tree(state, node_mgr, graph, dependency, dependency_tree_log=dependency_tree_log):
            operating_dependencies.add(dependency)

    state.path.pop()

    if node_mgr.operational(node, operating_dependencies):
        # node will work at this level with the operating dependencies
        if node not in state.active_nodes:
            state.active_nodes.add(node)
            state.order.append(node)
        if dependency_tree_log:
            state.tree_path.append(state.path + [node])
        return True
    else:
        if dependency_tree_log:
            state.tree_path.append(state.path + [node, 'NOT OPERATIONAL'])
        return False


def dependencies3(graph, root, node_mgr, dependency_tree_log=False):
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

    :param graph: Directed graph of all nodes and their dependencies.
    :type graph: nx.DiGraph
    :param root: Root node to start traversing from, usually named 'root'
    :type root: String
    :param node_mgr: Node manager which can assess whether nodes are
                     operational with the available dependencies at each
                     layer of the tree.
    :type node_mgr: analysis_engine.node.NodeManager
    :dependency_tree_log: If True, will populate `tree_path` for visualization of the
                          graph traversal.
    '''
    state = types.SimpleNamespace(
        active_nodes={  # operational nodes visited for fast lookup
            'HDF Duration',
            *node_mgr.aircraft_info,
            *node_mgr.achieved_flight_record,
            *node_mgr.hdf_keys,
            *node_mgr.segment_info,
        },
        inop_nodes=set(),  # non operational nodes due to insatisfied dependencies
        cycles=set(),  # set of cycles already seen
        order=[],
        path=[],  # current branch path
        tree_path=[],  # For viewing the tree in which nodes are added to path
    )

    for node in graph[root]:
        traverse_tree(state, node_mgr, graph, node, dependency_tree_log=dependency_tree_log)

    assert not state.path, 'Branch tracking path state not empty!'

    return state.order, state.tree_path


def graph_nodes(node_mgr):
    derived_only = {k: v for k, v in node_mgr.derived_nodes.items() if k not in node_mgr.hdf_keys}

    graph = nx.DiGraph()
    graph.add_node('root')  # Add a top-level root node to attach required nodes to.
    graph.add_nodes_from(node_mgr.hdf_keys, node_type='HDFNode')  # Add available raw parameter nodes.
    graph.add_nodes_from((name, {'node_type': node.__base__.__name__}) for name, node in derived_only.items())

    graph.add_edges_from(('root', node) for node in sorted(node_mgr.requested))  # Attach requested nodes to the root.

    derived_deps = set()
    for name, node in derived_only.items():
        dependencies = node.get_dependency_names()
        derived_deps.update(dependencies)
        graph.add_edges_from((name, dependency) for dependency in dependencies)  # Attach node to dependencies.

    available_nodes = set(node_mgr.keys())
    missing_derived_deps = derived_deps - available_nodes
    missing_requested = set(node_mgr.requested) - available_nodes

    if missing_derived_deps:
        logger.warning("Found %s dependencies which don't exist in LFL or Node modules.", len(missing_derived_deps))
        logger.debug('The missing dependencies: %s', sorted(missing_derived_deps))

    if missing_requested:
        raise ValueError('Missing requested parameters: %s' % sorted(missing_requested))

    return graph


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
    gr_all = graph_nodes(node_mgr)

    order, tree_path = dependencies3(gr_all, 'root', node_mgr, dependency_tree_log=dependency_tree_log)
    logger.debug("Processing order of %d nodes is: %s", len(order), order)
    if dependency_tree_log:
        ordered_tree_to_file(tree_path, name=dependency_tree_log)

    inactive_nodes = set(gr_all.nodes()) - set(order) - set(node_mgr.hdf_keys) - {'root'}
    logger.debug("Inactive nodes: %s", sorted(inactive_nodes))
    gr_st = gr_all.copy()
    gr_st.remove_nodes_from(inactive_nodes)

    inoperable_requested = set(node_mgr.requested) - set(order)
    if inoperable_requested:
        logger.warning("Found %s inoperable requested parameters.", len(inoperable_requested))
        if logging.NOTSET < logger.getEffectiveLevel() <= logging.DEBUG:
            # only build this massive tree if in debug!
            items = []
            for node in inactive_nodes:
                # add attributes to the node to reflect it's inactivity
                gr_all.node[node]['active'] = False
                gr_all.add_edges_from(gr_all.in_edges(node))
            for n in sorted(inoperable_requested):
                tree = indent_tree(gr_all, n, recurse_active=False)
                if tree:
                    items.append('------- INOPERABLE -------')
                    items.extend(tree)
            logger.debug('\n' + '\n'.join(items))
        if raise_inoperable_requested:
            raise InoperableDependencies(inoperable_requested)

    required_missing = set(node_mgr.required) - set(order)
    if required_missing:
        raise RequiredNodesMissing("Required nodes missing: %s" % ', '.join(required_missing))

    return order, gr_st
