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

def read_neural_net_from_keras(model):
    """
    Extracts the network architecture and weights from a Keras model.
    
    Returns:
        A tuple containing:
          - A list of architecture parameters: [input_size, nodes_in_layer1, nodes_in_layer2, ...]
          - A list of layers, where each layer is a list of neurons,
            and each neuron is represented as a list of weights ending with the bias.
    """
    layers_nodes = []
    layers = []
    
    # Iterate over each layer in the Keras model
    for layer in model.layers:
        # Get the weights of the layer (for Dense layers, usually two arrays)
        weights = layer.get_weights()
        # Skip layers with no weights (like Dropout, Activation, etc.)
        if not weights:
            continue

        # Assume Dense layer: first array is the weight matrix, second is the bias vector.
        W, b = weights
        # Append number of nodes/neurons in this layer.
        layers_nodes.append(W.shape[1])
        
        # Build the list of neurons for this layer.
        layer_data = []
        # For each neuron, collect its incoming weights and its bias.
        for neuron_idx in range(W.shape[1]):
            # Get weights for neuron i (all inputs for the neuron)
            # Append the corresponding bias for this neuron.
            neuron_weights = list(W[:, neuron_idx]) + [b[neuron_idx]]
            layer_data.append(neuron_weights)
        layers.append(layer_data)
    
    # Attempt to determine the input size.
    # If we have at least one layer, the first neuron's weight vector length includes the bias term,
    # so the number of inputs is len(neuron_weights) - 1.
    if layers:
        input_size = len(layers[0][0]) - 1
    else:
        # Fallback: use the model's input shape (ignoring the batch dimension).
        input_size = model.input_shape[1] if model.input_shape[1] is not None else 0

    # Return the architecture: [input_size, nodes_layer1, nodes_layer2, ...] and the layers' weights.
    return [input_size] + layers_nodes, layers