# MineNewt: Neural Networks in Minecraft

MineNewt is a neural network created from scratch in Minecraft using redstone. The network is first compiled using a custom rust library, and is then dynamically generated into a Minecraft world. This allows users to train neural networks on arbitrary functions and import them into Minecraft, effectively acting as a Rust compiler targeting Minecraft.

- [Features](#features)
- [Gallery](#gallery)
- [How it Works](#how-it-works)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)

## Features
MineNewt is composed of three main components:

1. **Training**: A neural network library built in Rust. Users can train networks on arbitrary Rust functions, with the trained networks exported as `.newt` files, which represent the network's weights and biases.

2. **Simulation**: This stochastic neural network simulator takes in a `.newt` file and simulates the accuracy of the Minecraft-based neural network. By running thousands of simulations, it provides insight into the network's robustness and accuracy in the Minecraft environment.

3. **Generation**: A Python library that modifies Minecraft world data, building the neural network from scratch given a `.newt` file. This library allows users to easily import trained networks into their Minecraft worlds.

## Gallery


## How it Works

## Getting Started

### Prerequisites
- [Rust](https://www.rust-lang.org/) (latest version)
- [Python](https://www.python.org/downloads/) (3.6 or later)
- [Minecraft](https://www.minecraft.net/en-us/get-minecraft) (Java Edition 1.16+)

### Quick Start

1. Clone this repository:
```
git clone https://github.com/expitau-dev/MineNewt.git
cd MineNewt
```

2. Train the neural network
```
cd training
cargo run -r
cd -
```

3. Generate the minecraft world
```
cd generation
python3 src/main.py
cd -
```

4. Copy the generated world to your Minecraft folder
```
cp -r generation/saves/output MINECRAFT_SAVES_DIRECTORY
```

## Usage

1. **Training Neural Networks**: Use the training library to train a network on a Rust function. Save your network with the `.newt` extension.

```rust
let _network = train_network(
  vec![8, 16, 16, 16, 8], // Network architecture, this one is a 8 -> 16 -> 16 -> 16 -> 8 network
  FloatDataFunction {
      f: Box::new(test_function), // The function to train on
      size: (8, 8), // The size of the inputs / outputs of the function
  },
  20, // Number of epochs
);

// Save the network to a file
let mut file = File::create("../example.newt").unwrap(); 
file.write_all(_network.to_string().as_bytes()).unwrap();
```

1. **(Optional) Simulating Networks**: Use the simulation library to run simulations on your trained network.

```rust
let network_data = read_neural_net_file(Path::new("../example.newt")).unwrap();

let input = vec![1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.0];

let output = propagate(&network_data, &input);
println!("{:?}", output);
```

1. **Generating Minecraft Worlds**: Use the generation library to create a Minecraft world from your trained network.

```python
from editor import world
from schema import network
import load

myWorld = world.World('saves/input')
networkData = load.read_neural_net_file('../example.newt')

network.network(networkData).write(myWorld, (0, 60, 0))

myWorld.close('saves/output')
```

This will create a world in "generation/saves/output" that contains the neural network. You can then copy this world to your Minecraft saves folder.

## Contributing

Please contribute! Submit garbage pull requests! I'm not picky.


[def]: #minenewt-neural-networks-in-minecraft
