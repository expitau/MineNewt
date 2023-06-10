# WIP README UNDER CONSTRUCTION
---
# MineNewt: Neural Networks in Minecraft

MineNewt is a unique fusion of machine learning and sandbox gaming, allowing users to build, train, and run neural networks right within the world of Minecraft. It leverages a powerful neural network library written in Rust, along with a Python-based world generation library to create a full-featured, stochastic neural network simulation within the game.

## Features
MineNewt is composed of three main components:

1. **Training**: A neural network library built in Rust. Users can train networks on arbitrary Rust functions, with the trained networks exported as `.newt` files, which represent the network's weights and biases.

2. **Simulation**: This stochastic neural network simulator takes in a `.newt` file and simulates the accuracy of the Minecraft-based neural network. By running thousands of simulations, it provides insight into the network's robustness and accuracy in the Minecraft environment.

3. **Generation**: A Python library that modifies Minecraft world data, building the neural network from scratch given a `.newt` file. This library allows users to easily import trained networks into their Minecraft worlds.

## Getting Started

### Prerequisites
- [Rust](https://www.rust-lang.org/) (latest version)
- [Python](https://www.python.org/downloads/) (3.6 or later)
- [Minecraft](https://www.minecraft.net/en-us/get-minecraft) (Java Edition 1.16+)

### Installation

1. Clone this repository:
```
git clone https://github.com/expitau-dev/MineNewt.git
```

2. Install the Rust library:
```
cd MineNewt/training
cargo build --release
```

3. Install the Python library:
```
cd ../generation
pip install .
```

## Usage

1. **Training Neural Networks**: Use the training library to train a network on a Rust function. Save your network with the `.newt` extension.

```rust
use minenewt::train::Network;
let mut network = Network::new(/* Parameters */);
network.train(/* Training parameters */);
network.save("network.newt");
```

2. **Simulating Networks**: Use the simulation library to run simulations on your trained network.

```rust
use minenewt::simulate::Simulator;
let mut simulator = Simulator::new("network.newt");
simulator.run(/* Simulation parameters */);
```

3. **Generating Minecraft Worlds**: Use the generation library to create a Minecraft world from your trained network.

```python
from minenewt import generate
generate.world_from_newt("network.newt", "world_directory")
```

This will modify the world data in the specified directory to include the neural network.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more information.
