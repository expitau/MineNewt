mod data;
use crate::data::DataPoint;

use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

use rand::*;
use std::fmt;

const STOCHASTIC_SIZE: usize = 50000;

#[derive(Clone)]
struct Stochastic {
    pub bits: Vec<bool>,
}

impl fmt::Debug for Stochastic {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{:?}",
            self.bits
                .iter()
                .map(|x| if *x { "1" } else { "0" })
                .collect::<Vec<&str>>()
                .join("")
        )
    }
}

impl Stochastic {
    pub fn new(p: f64) -> Self {
        let mut rng = rand::thread_rng();
        let mut bits = vec![false; STOCHASTIC_SIZE];

        let available: Vec<f64> = (0..15).map(|i| -1.0 + 2.0 * (i as f64) / 15.0).collect();

        let q = available.iter().fold(available[0], |a, &b| {
            if (p - a).abs() < (p - b).abs() {
                a
            } else {
                b
            }
        });

        for i in 0..STOCHASTIC_SIZE {
            if rng.gen::<f64>() < (q / 2.0 + 0.5) {
                bits[i] = true;
            }
        }
        Self { bits }
    }
    pub fn mult(&self, other: &Self) -> Self {
        Self {
            bits: self
                .bits
                .iter()
                .zip(&other.bits)
                .map(|(a, b)| !(a ^ b))
                .collect::<Vec<bool>>(),
        }
    }
    pub fn tanh(v: &Vec<Stochastic>) -> Stochastic {
        let mut bits = vec![false; STOCHASTIC_SIZE];
        let clamp = (v.len() as f64).log2().round() as i32;
        let mut stot: i32 = 0;
        for i in 0..STOCHASTIC_SIZE {
            let mut s: i32 = 0;
            for j in 0..v.len() {
                if v[j].at(i as u32) == 1 {
                    s += 1;
                } else {
                    s -= 1;
                }
            }

            if s > 0 {
                stot += 1;
            } else {
                stot -= 1;
            }

            if stot > clamp {
                stot = clamp;
            } else if stot < -clamp {
                stot = -clamp;
            }

            if stot > 0 {
                bits[i] = true;
            }
        }
        let out = Self { bits };

        out
    }
    pub fn to_f64(&self) -> f64 {
        let mut count = 0;
        for i in 0..STOCHASTIC_SIZE {
            if self.bits[i] {
                count += 1;
            }
        }
        (count as f64 / STOCHASTIC_SIZE as f64 - 0.5) * 2.0
    }
    fn at(&self, i: u32) -> u8 {
        if self.bits[i as usize] {
            1
        } else {
            0
        }
    }
}

pub fn propagate(network: &Vec<Vec<Vec<f64>>>, input: &Vec<f64>) -> Vec<f64> {
    let stoc_output = network.iter().fold(
        input
            .iter()
            .map(|i| Stochastic::new(*i))
            .collect::<Vec<Stochastic>>(),
        |current_inputs, layer| {
            layer.iter()
                .map(|neuron| {
                    let mut weighted_inputs = neuron[1..]
                        .iter()
                        .zip(current_inputs.iter())
                        .map(|(w, i)| Stochastic::new(*w).mult(i))
                        .collect::<Vec<Stochastic>>();
                    weighted_inputs.push(Stochastic::new(neuron[0]));
                    Stochastic::tanh(&weighted_inputs)
                })
                .collect::<Vec<Stochastic>>()
        },
    );

    stoc_output.iter().map(|o| o.to_f64()).collect::<Vec<f64>>()
}

fn read_neural_net_file(filename: &Path) -> io::Result<Vec<Vec<Vec<f64>>>> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);

    let mut lines = reader.lines();
    let layer_nodes: Vec<usize> = match lines.next() {
        Some(line) => line?
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect(),
        None => return Err(io::Error::new(io::ErrorKind::InvalidInput, "File is empty")),
    };

    let mut layers = Vec::new();

    for num_nodes in layer_nodes {
        let mut layer = Vec::new();
        for _ in 0..num_nodes {
            let node: Vec<f64> = match lines.next() {
                Some(line) => line?
                    .split_whitespace()
                    .map(|s| s.parse().unwrap())
                    .collect(),
                None => {
                    return Err(io::Error::new(
                        io::ErrorKind::UnexpectedEof,
                        "Unexpected end of file",
                    ))
                }
            };
            layer.push(node);
        }
        layers.push(layer);
    }

    Ok(layers)
}

fn main() {
    let network_data = read_neural_net_file(Path::new("../example.newt")).unwrap();

    let input = vec![1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.0];

    let output = propagate(&network_data, &input);
    println!("{:?}", output);
}
