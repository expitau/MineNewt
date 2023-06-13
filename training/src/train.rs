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

pub fn train_network<T: Trainable>(
    configuration: Vec<usize>, f: T, epochs: usize,
) -> Network {
    
    let mut data = Vec::new();

    for i in 0..100000 {
        let input = f.input(i);
        data.push(DataPoint {
            inputs: input.clone(),
            target: f.sample(input),
        });
    }

    let mut network = Network::new(configuration.clone(), vec![Activation::Stochastic; configuration.len() - 1]);

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

pub trait Trainable {
    fn input(&self, i: usize) -> Vec<f64>;
    fn sample(&self, inputs: Vec<f64>) -> Vec<f64>;
    fn size(&self) -> (usize, usize);
}

pub struct FloatDataFunction {
    pub size: (usize, usize),
    pub f: Box<dyn Fn(Vec<f64>) -> Vec<f64>>,
}

impl Trainable for FloatDataFunction {
    fn input(&self, i: usize) -> Vec<f64> {
        let mut v = Vec::new();

        for _ in 0..self.size.0 {
            v.push(rand::random::<f64>() * 2.0 - 1.0);
        }

        v
    }

    fn sample(&self, inputs: Vec<f64>) -> Vec<f64> {
        (self.f)(inputs)
    }

    fn size(&self) -> (usize, usize) {
        self.size
    }
}
