use std::fmt;

pub enum Activation {
    ReLU,
    Sigmoid,
    Tanh,
    Linear,
    Stochastic,
}

pub enum LayerType {
    // Fully connected
    Dense,

    // Map inputs directly
    Input,
}

// #[derive(Clone)]
pub struct Layer {
    pub activation_type: Activation,
    pub input_size: usize,
    pub nodes: usize,
    pub input_configuration: LayerType,
    pub weights: Vec<Vec<f64>>,
    pub biases: Vec<f64>,
}

impl fmt::Debug for Layer {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} Layer {:?} + {:?}",
            match self.activation_type {
                Activation::ReLU => "ReLU",
                Activation::Sigmoid => "Sigmoid",
                Activation::Tanh => "Tanh",
                Activation::Linear => "Linear",
                Activation::Stochastic => "Stochastic",
                _ => todo!(),
            },
            self.weights
                .iter()
                // .map(|v| v.iter().map(|x| x * 1.0).collect())
                .map(|v| v.iter().map(|x| (x * 10.0).round() / 10.0).collect())
                .collect::<Vec<Vec<f64>>>(),
            self.biases
                .iter()
                // .map(|x| x * 1.0)
                .map(|x| (x * 100.0).round() / 100.0)
                .collect::<Vec<f64>>()
        )
    }
}

impl ToString for Layer {
    fn to_string(&self) -> String {
        let precision = 3;
        format!("{}", self.weights.iter().zip(&self.biases).map(|(weights, bias)| {
            format!(
                "{} {}",
                weights
                    .iter()
                    .map(|x| (x * (10.0_f64).powi(precision)).round() / (10.0_f64).powi(precision))
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join(" "),
                (bias * (10.0_f64).powi(precision)).round() / (10.0_f64).powi(precision)
            )
        }).collect::<Vec<String>>().join("\n"))
    }
}

impl Layer {
    pub fn new(
        activation_type: Activation, input_size: usize, nodes: usize,
        input_configuration: LayerType,
    ) -> Self {
        Self {
            activation_type: activation_type,
            input_size: input_size,
            nodes: nodes,
            input_configuration: input_configuration,
            weights: (0..nodes)
                .map(|_| {
                    (0..input_size)
                        .map(|_| rand::random::<f64>() * 0.5 - 0.25)
                        .collect()
                })
                .collect(),
            biases: (0..nodes)
                .map(|_| rand::random::<f64>() * 0.5 - 0.25)
                .collect(),
        }
    }

    pub fn activation(&self, x: f64) -> f64 {
        match self.activation_type {
            Activation::Sigmoid => 1.0 / (1.0 + (-x).exp()),
            Activation::Tanh => x.tanh(),
            Activation::ReLU => {
                if x < 0.0 {
                    0.0
                } else {
                    x
                }
            }
            Activation::Stochastic => (x - 1.0).tanh(),
            Activation::Linear => x,
            _ => todo!(),
        }
    }

    pub fn activation_derivative(&self, x: f64) -> f64 {
        match self.activation_type {
            Activation::Sigmoid => self.activation(x) * (1.0 - self.activation(x)),
            Activation::Tanh => 1.0 - x.tanh() * x.tanh(),
            Activation::ReLU => {
                if x < 0.0 {
                    0.0
                } else {
                    1.0
                }
            }
            Activation::Stochastic => 1.0 - (x - 1.0).tanh() * (x - 1.0).tanh(),
            Activation::Linear => 1.0,
            _ => todo!(),
        }
    }

    pub fn weighted_sum(&self, inputs: &Vec<f64>) -> Vec<f64> {
        self.weights
            .iter()
            .enumerate()
            .map(|(i, v)| {
                v.iter()
                    .enumerate()
                    .map(|(j, w)| w * inputs[j])
                    .sum::<f64>()
                    + self.biases[i]
            })
            .collect()
    }

    pub fn outputs(&self, inputs: &Vec<f64>) -> Vec<f64> {
        self.weighted_sum(inputs)
            .iter()
            .map(|&x| self.activation(x))
            .collect()
    }

    // The error for the i-th layer is the derivative of its activation function times the aggregate of the errors of the next layer
    pub fn get_errors(&self, inputs: &Vec<f64>, next_errors: Vec<f64>) -> Vec<f64> {
        let weighted_inputs = self.weighted_sum(inputs);
        self.weights
            .iter()
            .enumerate()
            .map(|(j, weights)| {
                self.activation_derivative(weighted_inputs[j])
                    * weights
                        .iter()
                        .enumerate()
                        .map(|(l, w)| w * next_errors[l])
                        .sum::<f64>()
            })
            .collect()
    }

    pub fn adjust_weights(
        &mut self, weight_gradients: Vec<Vec<f64>>, bias_gradients: Vec<f64>, scale: f64,
    ) {
        self.weights = self
            .weights
            .iter()
            .enumerate()
            .map(|(node_index, node_weights)| {
                node_weights
                    .iter()
                    .enumerate()
                    .map(|(weight_index, w)| w - weight_gradients[node_index][weight_index] * scale)
                    .collect()
            })
            .collect();

        self.biases = self
            .biases
            .iter()
            .enumerate()
            .map(|(i, bias)| bias - bias_gradients[i] * scale)
            .collect();
    }
}
