#![allow(unused_imports)]
#![allow(unused)]
#![allow(dead_code)]
mod data;
mod layer;
mod network;

use std::fs::File;
use std::io::prelude::*;
use std::vec;

use crate::data::DataPoint;
use crate::layer::Activation;
use crate::network::*;

fn get_accuracy(network: &Network, data: Vec<DataPoint>) -> f64 {
    data.iter()
        .map(|data_point| {
            match network.classify(data_point.inputs.clone())
                == data_point
                    .target
                    .clone()
                    .iter()
                    .enumerate()
                    .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
                    .unwrap()
                    .0
            {
                true => 1,
                false => 0,
            }
        })
        .sum::<i32>() as f64
        / data.len() as f64
}

fn get_cost(network: &Network, data: Vec<DataPoint>) -> f64 {
    let total_cost = data
        .iter()
        .map(|data_point| {
            let outputs = network.sample(&data_point.inputs.clone());
            outputs
                .iter()
                .zip(data_point.target.clone())
                .map(|(a, b)| (a - b).powi(2))
                .sum::<f64>()
        })
        .sum::<f64>();
    total_cost / data.len() as f64
}

fn train_network(
    configuration: (Vec<usize>, Vec<Activation>), data: Vec<DataPoint>, epochs: usize,
) -> Network {
    let mut network = Network::new(configuration.0, configuration.1);

    let batch_size = 250;
    let training_split: usize = (0.95 * data.len() as f64) as usize;
    let training_data: Vec<DataPoint> = data[0..training_split].try_into().unwrap();
    let test_data: Vec<DataPoint> = data[training_split..data.len()].try_into().unwrap();
    println!(
        "Training network... ({}, {})",
        training_data.len(),
        test_data.len()
    );
    for i in 0..epochs {
        println!("=== Iteration {} ===", i);
        for j in 0..(training_data.len() / batch_size) {
            let batch: Vec<DataPoint> = training_data
                [(j * batch_size)..(j * batch_size + batch_size)]
                .try_into()
                .unwrap();
            network.learn(batch.clone());
            if j % 5 == 0 {
                println!("{}/{}", j, training_data.len() / batch_size);
            }
            if j % 25 == 0 {
                println!("test cost {:?}", get_cost(&network, test_data.clone()));
                // println!(
                //     "test accuracy {:?}%",
                //     100.0 * get_accuracy(&network, test_data.clone())
                // );
            }
        }
        println!("test cost {:?}", get_cost(&network, test_data.clone()));
        // println!(
        //     "test accuracy {:?}%",
        //     get_accuracy(&network, test_data.clone()) * 100.0
        // );
    }
    network
}

trait Trainable {
    fn input(&self, i: usize) -> Vec<f64>;
    fn sample(&self, inputs: Vec<f64>) -> Vec<f64>;
    fn size(&self) -> (usize, usize);
}

fn get_data<T: Trainable>(f: T, iterations: usize) -> Vec<DataPoint> {
    let mut output = Vec::new();

    for i in 0..iterations {
        let input = f.input(i);
        output.push(DataPoint {
            inputs: input.clone(),
            target: f.sample(input),
        });
    }
    output
}

struct TestF {}

impl Trainable for TestF {
    fn input(&self, i: usize) -> Vec<f64> {
        // Random vector of size 4
        let out = vec![
            rand::random::<f64>() * 2.0 - 1.0,
            rand::random::<f64>() * 2.0 - 1.0,
            rand::random::<f64>() * 2.0 - 1.0,
            rand::random::<f64>() * 2.0 - 1.0,
        ];
        // println!("Input: {:?}", out);
        out

        // vec![i % 2, (i / 2) % 2, (i / 4) % 2, (i / 8) % 2].iter().map(|&x| if x == 0 { -1.0 } else { 1.0 }).collect()
    }

    fn sample(&self, inputs: Vec<f64>) -> Vec<f64> {
        let normalized_input = inputs.iter().map(|&x| if x < 0.0 { 0 } else { 1 }).collect::<Vec<u32>>();
        let a = normalized_input[1] + 2 * normalized_input[0];
        let b = normalized_input[3] + 2 * normalized_input[2];
        let c = a + b;
        vec![(c / 4) % 2, (c / 2) % 2, c % 2, c % 3].iter().map(|&x| if x == 0 { -1.0 } else { 1.0 }).collect()
        // inputs.iter().map(|&x| if x < -0.5 { -1.0 } else { if x > 0.5 { 1.0 } else { 0.0 }}).collect()
        // let alternating = inputs[0] > 0.0;
        // let starts_with_zero = inputs[1] > 0.0;

        // match (alternating, starts_with_zero) {
        //     (true, true) => vec![-1.0, 1.0, -1.0, 1.0],
        //     (true, false) => vec![1.0, -1.0, 1.0, -1.0],
        //     (false, true) => vec![-1.0, -1.0, -1.0, -1.0],
        //     (false, false) => vec![1.0, 1.0, 1.0, 1.0],
        // }
    }

    fn size(&self) -> (usize, usize) {
        (4, 4)
    }
}

fn main() {
    // let data = data::get_training_data();
    let data = get_data(TestF {}, 50000);

    // println!("Data: {:?}", data);

    // let _network = train_network((vec![28 * 28, 100, 10], vec![Activation::Tanh, Activation::Tanh]), data.clone(), 3);
    let _network = train_network(
        (vec![4, 4, 4], vec![Activation::Stochastic, Activation::Stochastic]),
        data.clone(),
        5,
    );

    let mut file = File::create("example.newt").unwrap();
    file.write_all(_network.to_string().as_bytes()).unwrap();

    println!("Sampled: {:?}", _network.sample(&vec![1.0, -1.0, 1.0, -1.0]));
    // println!("Data: {:?}", &data.clone()[0..10])
}
