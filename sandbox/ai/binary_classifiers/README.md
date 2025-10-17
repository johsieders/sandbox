# Binary Classifier Study

A systematic study of neural network classifiers on binary functions with known geometric structures. This project compares different network architectures, loss functions, and optimizers by testing them on functions with varying complexity and linear separability.

## Overview

Rather than training classifiers on real-world datasets with unknown structure, this study uses binary functions with precisely defined decision boundaries. This allows us to:

- **Understand classifier behavior** on problems with known optimal solutions
- **Compare architectures** by observing how topology affects learning
- **Isolate the effect** of different loss functions and optimizers
- **Visualize decision boundaries** for functions in 2D space

## Test Functions

### Linearly Separable
- **Boolean Operations**: AND, OR (classical logic gates)
- **Half-planes**: Linear decision boundaries defined by weights and bias

### Non-Linearly Separable
- **XOR**: The canonical non-linearly separable problem
- **Circle**: Points inside/outside a circle of given radius
- **Square**: Points inside/outside a square (max-norm)
- **Concentric Rings**: Alternating classification between rings (particularly challenging)

## Classifier Architectures

All classifiers are implemented using PyTorch and tested with various configurations:

### Single Layer
- **Regressor (2→1 + Sigmoid)**: MSE loss, rounded predictions
- **Binary Classifier (2→1)**: BCEWithLogitsLoss
- **Multi-class Classifier (2→2)**: CrossEntropyLoss

### Two Layers
- **Regressor (2→5→1)**: MSE loss with hidden layer
- **Binary Classifier (2→5→1)**: BCEWithLogitsLoss with hidden layer
- **Multi-class Classifier (2→5→2)**: CrossEntropyLoss with hidden layer

### Three Layers
- **Deep Classifier (2→8→3→2)**: CrossEntropyLoss with multiple hidden layers

### Perceptron Implementations
- **Custom Perceptron**: Manual implementation with configurable learning rate
- **Sklearn Perceptron**: Reference implementation for comparison

## Module Structure

```
booleans/
├── classifier_fcts.py      # Binary functions: AND, OR, XOR, plane, circle, square, rings
├── classifiers.py          # Classifier wrapper for training and prediction
├── perceptron.py           # Custom perceptron implementation
├── booleans.ipynb          # Main experimental notebook
├── losses.ipynb            # Loss function analysis
└── tests/
    └── test_classifier_fcts.py  # Comprehensive test suite
```

### `classifier_fcts.py`
Factory functions that create binary classifiers for geometric regions:
- `plane(weight, bias)` → Returns function for half-plane classification
- `circle(radius)` → Returns function for circle interior
- `square(length)` → Returns function for square interior (max-norm)
- `rings(radius)` → Returns function for concentric ring pattern
- `_and()`, `_or()`, `_xor()` → Boolean operations on tensors

### `classifiers.py`
Generic `Classifier` wrapper class that encapsulates:
- Neural network module (`nn.Module`)
- Optimizer (Adam, Adagrad, etc.)
- Loss function (MSE, BCE, CrossEntropy)
- Prediction function (rounding, heaviside, argmax)
- Optional data preparation (e.g., one-hot encoding)

### `perceptron.py`
Simple perceptron implementation with:
- Configurable dimensions and learning rate
- Manual weight updates (no autograd)
- Online learning (sample-by-sample updates)

## Key Findings

### Linear Separability
- Single-layer networks successfully learn AND, OR, and half-plane problems
- Perceptrons converge quickly on linearly separable problems
- XOR requires hidden layers (not linearly separable)

### Non-Linear Problems
- Circles and squares require at least one hidden layer
- Two-layer networks with 5 hidden units handle most geometric shapes
- Concentric rings remain challenging even for deeper networks

### Loss Functions
- **CrossEntropyLoss** generally performs best for classification
- **BCEWithLogitsLoss** works well for binary problems
- **MSE loss** (regression approach) less suitable for sharp decision boundaries

### Architecture Trade-offs
- More layers help with complex boundaries but risk overfitting
- 5 hidden units sufficient for simple non-linear problems
- Deeper networks (3+ layers) beneficial for rings but require careful tuning

## Usage

### Training a Classifier
```python
from classifiers import Classifier
from classifier_fcts import circle
import torch.nn as nn
import torch.optim as optim

# Define architecture
M = nn.Sequential(nn.Linear(2, 5), nn.Sigmoid(), nn.Linear(5, 1))
optimizer = optim.Adam(M.parameters(), lr=0.01)
loss_fct = nn.BCEWithLogitsLoss()
pred_fct = lambda Y: torch.heaviside(Y, torch.zeros(1))

clf = Classifier(M, optimizer, loss_fct, pred_fct)

# Generate training data
X = torch.rand((300, 2)) * 10
c = circle(5)
Y = c(X)

# Train
history = clf.fit(X, Y, n_epochs=1000)

# Predict
Y_pred = clf.predict(X)
```

### Using Classifier Functions
```python
from classifier_fcts import plane, _xor
import torch

# Boolean XOR
X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
Y = _xor(X)  # Returns [[0.], [1.], [1.], [0.]]

# Half-plane (AND gate)
f_and = plane([1, 1], -1.5)
Y_and = f_and(X)  # Returns [[0.], [0.], [0.], [1.]]
```

## Running Tests

```bash
pytest tests/ai/test_classifier_fcts.py -v
```

The test suite includes:
- Boolean function correctness (AND, OR, XOR)
- Geometric region classification (circles, squares, planes)
- Ring pattern verification
- Shape validation for all functions

## Notebooks

### `booleans.ipynb`
Main experimental notebook with:
- Comparison of all architectures on boolean operations
- Training curves and loss analysis
- Confusion matrices for each classifier
- Performance on geometric test functions

### `losses.ipynb`
Deep dive into loss function behavior and optimization

## Dependencies

- PyTorch
- scikit-learn (for Perceptron reference)
- matplotlib (for visualization)
- numpy

## Future Directions

- **More geometric functions**: Ellipses, spirals, checkerboard patterns
- **Activation functions**: Compare ReLU, tanh, Swish effects
- **Regularization**: Test dropout, L2 regularization on complex boundaries
- **3D functions**: Extend to higher-dimensional decision boundaries
- **Adversarial examples**: Test robustness near decision boundaries

## References

This study follows classical machine learning pedagogy where simple, well-understood problems illuminate classifier behavior before tackling real-world datasets with unknown structure.