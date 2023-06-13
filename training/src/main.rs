#![allow(unused_imports)]
#![allow(unused)]
#![allow(dead_code)]
mod data;
mod layer;
mod network;
mod train;

use std::fs::File;
use std::io::prelude::*;
use std::vec;

use crate::data::DataPoint;
use crate::layer::Activation;
use crate::network::*;
use crate::train::*;

fn test_function(inputs: Vec<f64>) -> Vec<f64> {
    let normalized_input = inputs
        .iter()
        .map(|&x| if x < 0.0 { 0 } else { 1 })
        .collect::<Vec<u32>>();
    let a = normalized_input[3]
        + 2 * normalized_input[2]
        + 4 * normalized_input[1]
        + 8 * normalized_input[0];
    let b = normalized_input[7]
        + 2 * normalized_input[6]
        + 4 * normalized_input[5]
        + 8 * normalized_input[4];
    let c = a + b;
    vec![
        (c / 16) % 2,
        (c / 8) % 2,
        (c / 4) % 2,
        (c / 2) % 2,
        c % 2,
        c % 3,
        c % 5,
        c % 7,
    ]
    .iter()
    .map(|&x| if x == 0 { -1.0 } else { 1.0 })
    .collect::<Vec<f64>>()
}

fn main() {
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
}
