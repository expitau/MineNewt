use std::fmt;
use std::fs;

#[derive(Clone, Debug)]
pub struct DataPoint {
    pub inputs: Vec<f64>,
    pub target: Vec<f64>,
}

#[derive(Clone)]
pub struct Image {
    pub width: usize,
    pub height: usize,
    pub pixels: Vec<f64>,
}

impl fmt::Debug for Image {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                write!(
                    f,
                    "{}",
                    if self.pixels[x as usize + (y * self.width) as usize] > 0.5 {
                        '#'
                    } else {
                        ' '
                    }
                )?;
            }
            writeln!(f, "")?;
        }
        write!(f, "")
    }
}

pub fn get_training_data() -> Vec<DataPoint> {
    let image_data = fs::read("../data/mnist/train-images-idx3-ubyte").unwrap();
    let label_data = fs::read("../data/mnist/train-labels-idx1-ubyte").unwrap();
    let image_magic_number = u32::from_be_bytes(image_data[0..4].try_into().unwrap());
    let label_magic_number = u32::from_be_bytes(label_data[0..4].try_into().unwrap());
    let number_of_images = u32::from_be_bytes(image_data[4..8].try_into().unwrap());
    let number_of_labels = u32::from_be_bytes(label_data[4..8].try_into().unwrap());
    let n_rows = u32::from_be_bytes(image_data[8..12].try_into().unwrap());
    let n_cols = u32::from_be_bytes(image_data[12..16].try_into().unwrap());
    println!("Image metadata loaded - Magic number {};  Number of images {};  Number of rows {};  Number of columns {}", image_magic_number, number_of_images, n_rows, n_cols);
    println!(
        "Label metadata loaded - Magic number {};  Number of labels {};",
        label_magic_number, number_of_labels
    );
    let mut output: Vec<DataPoint> = vec![];

    println!("Loading training data... this may take a while");
    for i in 0..number_of_images {
        let index = (i + 8) as usize;
        let label = match u8::from_be_bytes(label_data[index..(index + 1)].try_into().unwrap()) {
            // 0 => vec![1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            // 1 => vec![0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            // 2 => vec![0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            // 3 => vec![0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            // 4 => vec![0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            // 5 => vec![0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            // 6 => vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            // 7 => vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            // 8 => vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            // 9 => vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            0 => vec![1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            1 => vec![-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            2 => vec![-1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            3 => vec![-1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            4 => vec![-1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            5 => vec![-1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0],
            6 => vec![-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0],
            7 => vec![-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0],
            8 => vec![-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0],
            9 => vec![-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0],
            _ => panic!("Label did not match expected range (0-9)"),
        };

        let mut image: Image = Image {
            width: n_cols as usize,
            height: n_rows as usize,
            pixels: vec![],
        };
        for y in 0..n_rows {
            for x in 0..n_cols {
                let index = (16 + x + y * n_cols + i * n_cols * n_rows) as usize;
                let pixel = (u8::from_be_bytes(image_data[index..(index + 1)].try_into().unwrap())
                    as f64)
                    / 256.0;
                image.pixels.push(pixel);
            }
        }

        output.push(DataPoint {
            inputs: image.pixels,
            target: label,
        });
    }

    output
}
