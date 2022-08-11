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
        node_string += ' 0'
        for i in range(1, lanes):
            node_string += ' | <f'+ str(i) + '> ' + str(i)
            # add in blank port with node name on it
            if i == middle:
                node_string += ' | ' + node_name + ' '

    return node_string


def create_graph_images(json_filepath):
    # parse JSON
    with open(json_filepath, 'r') as f:
        raw = ''.join(f.readlines())
    parsed = eval(raw.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    groups = set()
    for element in parsed:
        groups.add(element['group'])
    for group in groups:
        subgraph = [node for node in parsed if node['group'] == group]

        # draw subgraph using graphviz
        import graphviz
        from graphviz import nohtml
        graph_name = "dfg-" + str(group)
        g = graphviz.Digraph('g', filename=graph_name, node_attr={'shape': 'record', 'height': '.1'})


        # add nodes (including ports)
        for node in subgraph:
            g.node(str(node['id']), nohtml(generate_node_string(node)))

        # go back and add edges now that nodes and ports are defined
        for node in subgraph:
            if node['inputs'] != None:
                for input in node['inputs']:

                    src_id = str(input['edges'][0]['src_id'])
                    src_port = str(input['edges'][0]['src_val'])
                    dest_id = str(node['id'])
                    dest_port = str(input['edges'][0]['oid'])

                    # prevent assignment to a port that graphically doesn't exist on the destination node
                    if 'lanes' not in node.keys():
                        dest_port = '0'

                    src_identifier = src_id + ':f' + src_port
                    dest_identifier =  dest_id + ':f' + dest_port
                    g.edge(src_identifier, dest_identifier)

        # render graph
        g.view()


if __name__ == "__main__":
    import sys
    for i in range(1, len(sys.argv)):
        create_graph_images(sys.argv[i])
