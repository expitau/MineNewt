use crate::data::*;
use crate::layer::*;
use std::fmt;

pub struct Network {
    pub layers: Vec<Layer>,
}

impl fmt::Debug for Network {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

impl ToString for Network {
    fn to_string(&self) -> String {
        format!("{}\n{}",
        self.layers.iter().map(|l| l.nodes.to_string()).collect::<Vec<String>>().join(" "),
        self.layers
            .iter()
            .map(|layer| layer.to_string())
            .collect::<Vec<String>>()
            .join("\n"))
    }
}

impl Network {
    pub fn new(sizes: Vec<usize>, activations: Vec<Activation>) -> Self {
        Self {
            layers: sizes
                .windows(2)
                .zip(activations)
                .map(|(t, a)| Layer::new(a, t[0], t[1], LayerType::Dense))
                .collect(),
        }
    }
    pub fn sample(&self, inputs: &Vec<f64>) -> Vec<f64> {
        self.layers
            .iter()
            .fold(inputs.to_vec(), |acc, layer| layer.outputs(&acc))
    }

    pub fn classify(&self, inputs: Vec<f64>) -> usize {
        self.sample(&inputs)
            .iter()
            .enumerate()
            .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal))
            .unwrap()
            .0
    }

    pub fn learn(&mut self, training_data: Vec<DataPoint>) {
        let training_size = training_data.len();

        let mut weight_gradients: Vec<Vec<Vec<f64>>> = (0..self.layers.len())
            .map(|i| {
                (0..self.layers[i].nodes)
                    .map(|_| (0..self.layers[i].input_size).map(|_| 0.0).collect())
                    .collect()
            })
            .collect();
        let mut bias_gradients: Vec<Vec<f64>> = (0..self.layers.len())
            .map(|i| (0..self.layers[i].nodes).map(|_| 0.0).collect())
            .collect();

        for data_point in training_data.iter() {
            let mut weighted_inputs: Vec<Vec<f64>> = (0..self.layers.len())
                .map(|i| (0..self.layers[i].nodes).map(|_| 0.0).collect())
                .collect();
            let mut outputs: Vec<Vec<f64>> = (0..self.layers.len())
                .map(|i| (0..self.layers[i].nodes).map(|_| 0.0).collect())
                .collect();
            let mut errors: Vec<Vec<f64>> = (0..self.layers.len())
                .map(|i| (0..self.layers[i].nodes).map(|_| 0.0).collect())
                .collect();

            // 1) Calculate the forward phase for each datapoint, and store the outputs + activations for each node
            for layer_index in 0..self.layers.len() {
                let current_input = match layer_index {
                    0 => data_point.inputs.clone(),
                    _ => outputs[layer_index - 1].clone(),
                };

                outputs[layer_index] = self.layers[layer_index].outputs(&current_input);
                weighted_inputs[layer_index] =
                    self.layers[layer_index].weighted_sum(&current_input);
            }

            // 2) Calculate the backward phrase for each datapoint, and store the errors for each node
            for layer_index in (0..self.layers.len()).rev() {
                // a) Evaluate the error term for the final layer
                let costs: Vec<f64> = match layer_index {
                    x if x == self.layers.len() - 1 => outputs[layer_index]
                        .iter()
                        .enumerate()
                        .map(|(node_index, actual)| actual - data_point.target[node_index])
                        .collect(),
                    _ => (0..self.layers[layer_index].nodes)
                        .map(|node_index| {
                            self.layers[layer_index + 1]
                                .weights
                                .iter()
                                .zip(&errors[layer_index + 1])
                                .map(|(w, e)| w[node_index] * e)
                                .sum::<f64>()
                        })
                        .collect(),
                };
                // b) Backpropagate the error terms for the hidden layers
                errors[layer_index] = weighted_inputs[layer_index]
                    .iter()
                    .zip(&costs)
                    .map(|(a, cost)| self.layers[layer_index].activation_derivative(*a) * cost)
                    .collect();

                // c) Evaluate the partial derivatives of the individual error with respect to the weights and biases
                for node_index in 0..self.layers[layer_index].nodes {
                    for weight_index in 0..self.layers[layer_index].input_size {
                        let prev_layer_output = match layer_index {
                            0 => data_point.inputs[weight_index],
                            _ => outputs[layer_index - 1][weight_index],
                        };
                        weight_gradients[layer_index][node_index][weight_index] +=
                            errors[layer_index][node_index] * prev_layer_output;
                    }
                    bias_gradients[layer_index][node_index] += errors[layer_index][node_index]
                }
            }
        }

        // 3) Combine the individual gradients to get the total gradient
        // 4) Update the weights according to the total gradient
        for layer_index in 0..self.layers.len() {
            self.layers[layer_index].adjust_weights(
                weight_gradients[layer_index].clone(),
                bias_gradients[layer_index].clone(),
                0.5 / training_size as f64,
            )
        }
    }
}
