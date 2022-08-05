#!/bin/python3

def create_graph_images(json_filepath):
    with open(json_filepath, 'r') as f:
        raw = ''.join(f.readlines())
        parsed = eval(raw.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
        for node in parsed:
            if 'bmss' in node.keys():
                print(node['bmss'])
            else:
                print(None)

if __name__ == "__main__":
    import sys
    for i in range(1, len(sys.argv)):
        create_graph_images(sys.argv[i])
