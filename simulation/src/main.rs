mod data;
use crate::data::DataPoint;

use rand::*;
use std::fmt;

const STOCHASTIC_SIZE: usize = 1000;

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

        let available = [
            -1.0,
            -0.8666666666666667,
            -0.7333333333333334,
            -0.6,
            -0.4666666666666667,
            -0.33333333333333337,
            -0.19999999999999996,
            -0.06666666666666665,
            0.06666666666666665,
            0.19999999999999996,
            0.33333333333333326,
            0.46666666666666656,
            0.6000000000000001,
            0.7333333333333334,
            0.8666666666666667,
            1.0,
        ];

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
        // println!(
        //     "{:.2} tanh: {:?}, expected: {:?}",
        //     (out.to_f64() - (v.iter().map(|x| x.to_f64()).sum::<f64>() - 1.0).tanh()).powi(2),
        //     out.to_f64(),
        //     (v.iter().map(|x| x.to_f64()).sum::<f64>() - 1.0).tanh()
        // );

        // out
        Stochastic::new((v.iter().map(|x| x.to_f64()).sum::<f64>() - 1.0).tanh())
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

pub fn propagate(
    network: &Vec<Vec<Vec<f64>>>,
    input: &Vec<f64>,
) -> Vec<f64> {
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

    let output = stoc_output.iter().map(|o| o.to_f64()).collect::<Vec<f64>>();
    // let output: Vec<f64> = weights.iter().zip(biases).fold(
    //     input.clone(),
    //     |current_inputs, (layer_weights, layer_biases)| {
    //         layer_weights
    //             .iter()
    //             .zip(layer_biases)
    //             .map(|(neuron_weights, neuron_bias)| {
    //                 let mut weighted_inputs = neuron_weights
    //                     .iter()
    //                     .zip(current_inputs.iter())
    //                     .map(|(w, i)| w * i)
    //                     .collect::<Vec<f64>>();
    //                 weighted_inputs.push(*neuron_bias);
    //                 weighted_inputs.iter().sum::<f64>().tanh()
    //             })
    //             .collect::<Vec<f64>>()
    //     },
    // );
    // println!("{:?}", output);
    output
}

use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

fn parse_csv_line(filename: &str) -> Result<(Vec<Vec<Vec<f64>>>, Vec<Vec<f64>>), Box<dyn Error>> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut lines: Vec<String> = vec![];
    for l in reader.lines() {
        lines.push(l?);
    }

    let weights: Vec<Vec<Vec<f64>>> = lines
        .iter()
        .map(|line| {
            line.split('+').collect::<Vec<&str>>()[0]
                .split(";")
                .map(|s| {
                    s.split(',')
                        .map(|s| s.trim().parse::<f64>().unwrap())
                        .collect::<Vec<f64>>()
                })
                .collect::<Vec<Vec<f64>>>()
        })
        .collect();
    let biases: Vec<Vec<f64>> = lines
        .iter()
        .map(|line| {
            line.split('+').collect::<Vec<&str>>()[1]
                .split(',')
                .map(|s| s.trim().parse::<f64>().unwrap())
                .collect::<Vec<f64>>()
        })
        .collect();

    // .split(',')
    //     .map(|s| s.trim().parse::<f64>().unwrap())
    //     .collect();

    Ok((weights, biases))
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
    let network_data = read_neural_net_file(Path::new("../training/example.newt")).unwrap();

    let output = propagate(&network_data, &vec![1.0, -1.0, -1.0, 1.0]);
    println!("{:?}", output);
    // let a = Stochastic::new(0.5);
    // let b = Stochastic::new(0.7);
    // println!("a    {:?}", a);
    // println!("b    {:?}", b);
    // println!("a*b  {:?}", a.mult(&b));
    // println!("tanh {:?}", Stochastic::tanh(&vec![a.clone(), b.clone()]));
    // println!("--------");
    // println!("a    {:?}", a.to_f64());
    // println!("b    {:?}", b.to_f64());
    // println!("a*b  {:?}", a.mult(&b).to_f64());
    // println!(
    //     "tanh {:?}",
    //     Stochastic::tanh(&vec![a.clone(), b.clone()]).to_f64()
    // );
    // let data = data::get_training_data();
    // let network = parse_csv_line("../training/example.csv").unwrap();

    // let mut total = 0;
    // let mut count = 0;

    // for i in 0..100 {
    //     let c: u32 = propagate(&network.0, &network.1, &data[i].inputs)
    //         .clone()
    //         .iter()
    //         .enumerate()
    //         .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
    //         .unwrap()
    //         .0 as u32;
    //     if c == data[i].n as u32 {
    //         total += 1;
    //     }
    //     count += 1;
    //     println!("{:?} {:?}", c, data[i].n);
    // }
    // println!("{:?}", total as f64 / count as f64);

    // println!(
    //     "{:?}",
    //     propagate(
    //         &vec![vec![vec![0.15, 0.2], vec![0.25, 0.3]], vec![vec![0.4, 0.45], vec![0.5, 0.55]]],
    //         &vec![vec![0.35, 0.35], vec![0.6, 0.6]],
    //         &vec![0.05, 0.10]
    //     )
    // )
}
