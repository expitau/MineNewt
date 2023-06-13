def read_neural_net_file(filename):
    with open(filename, 'r') as f:
        layers_nodes = list(map(int, f.readline().strip().split())) # read first line for number of nodes in each layer

        layers = []
        for num_nodes in layers_nodes:  # for each layer
            layer = []
            for _ in range(num_nodes):  # for each node
                node = list(map(float, f.readline().strip().split()))  # read a line and convert to float
                layer.append(node)
            layers.append(layer)
        return [len(layers[0][0]) - 1] + layers_nodes, layers
