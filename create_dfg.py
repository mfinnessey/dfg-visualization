#!/bin/python3

def generate_node_string(node):
    node_name = node['name']

    # set appropriate number of lanes (1 if not otherwise specified)
    lanes = 1
    if 'lanes' in node.keys():
        lanes = int(node['lanes'])

    # build node string
    node_string = '<f0>'
    if lanes == 1:
        node_string += node_name
    else:
        # determine rough middle location to place node name after
        middle = lanes / 2 - 1

        # add lanes
        for i in range(1, lanes):
            node_string += ' | <f'+ str(i) + '> '
            # add in blank port with node name on it
            if i == middle:
                node_string += ' | ' + node_name + ' '

    return node_string


def create_graph_images(json_filepath):
    # parse JSON
    with open(json_filepath, 'r') as f:
        raw = ''.join(f.readlines())
    parsed = eval(raw.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    group = 0 # FIXME currently hardcoded to only generate an image for the first subgraph
    roots = []
    subgraph = [node for node in parsed if node['group'] == group]

    # draw subgraph using graphviz
    import graphviz
    from graphviz import nohtml
    g = graphviz.Digraph('g', filename="dfg.gv", node_attr={'shape': 'record', 'height': '.1'})


    # add nodes (including ports)
    for node in subgraph:
        g.node(str(node['id']), nohtml(generate_node_string(node)))

    # go back and add edges now that nodes and ports are defined
    for node in subgraph:
        if node['inputs'] != None:
            for input in node['inputs']:
                tail_identifier = str(input['edges'][0]['src_id']) + ':f' + str(input['edges'][0]['src_val'])
                head_identifier = str(node['id']) + ':f' + str(input['edges'][0]['oid'])
                g.edge(tail_identifier, head_identifier)

    # render graph
    g.view()


if __name__ == "__main__":
    import sys
    for i in range(1, len(sys.argv)):
        create_graph_images(sys.argv[i])
