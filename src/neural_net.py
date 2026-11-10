import numpy as np

class SimpleAutoencoder:
    def __init__(self, input_dim: int, hidden_dim: int = 4, lr: float = 0.01):
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2. / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, input_dim) * np.sqrt(2. / hidden_dim)
        self.b2 = np.zeros((1, input_dim))
        self.lr = lr

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def _sigmoid_deriv(self, x):
        return x * (1 - x)

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self._sigmoid(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self._sigmoid(self.z2)
        return self.a2

    def backward(self, X, output):
        n = X.shape[0]
        error = output - X
        d_z2 = error * self._sigmoid_deriv(output)
        d_W2 = (self.a1.T @ d_z2) / n
        d_b2 = np.sum(d_z2, axis=0, keepdims=True) / n
        d_a1 = d_z2 @ self.W2.T
        d_z1 = d_a1 * self._sigmoid_deriv(self.a1)
        d_W1 = (X.T @ d_z1) / n
        d_b1 = np.sum(d_z1, axis=0, keepdims=True) / n

        self.W2 -= self.lr * d_W2
        self.b2 -= self.lr * d_b2
        self.W1 -= self.lr * d_W1
        self.b1 -= self.lr * d_b1

    def train(self, X, epochs: int = 1000):
        for _ in range(epochs):
            output = self.forward(X)
            self.backward(X, output)

    def reconstruction_error(self, X):
        output = self.forward(X)
        return np.mean((output - X) ** 2, axis=1)
