# Neural Network for recognizing hand drawn doodles

A convolutional neural network using Tensorflow and Google's Quick, Draw! [dataset](https://github.com/googlecreativelab/quickdraw-dataset) to recognize hand drawn images made by [Lars Wächter](https://larswaechter.dev/).

Read his [blog post](https://larswaechter.dev/blog/recognizing-hand-drawn-doodles/) for more information.

## Setup

Create a virtual enviroment and install the dependencies:

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

If you don't have the dataset yet download it by running the command:

```
python download_dataset.py
```

Train the model by running the command:

```
python train.py
```
