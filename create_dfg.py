with open('./mm_0_4_4.dfg.json', 'r') as f:
    raw = ''.join(f.readlines())
    parsed = eval(raw.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    for node in parsed:
        if 'bmss' in node.keys():
            print(node['bmss'])
        else:
            print(None)
