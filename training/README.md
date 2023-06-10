# Neural Network

- Layer
  - Input configuration
  - Activations
  - Size
  - getOutputs()
  - learn(rate, gradients)
- Network
  - Sizes
  - 


Layer 5 node 1 -> Layer 6 node 3 weights

<!-- The error for the weight from L5[1] to L6[3] is output of L5[1] times the error of L6[3] -->
$$\frac{\partial E_d}{\partial w_{13}^5} = \delta_3^6g(a_1^{5})$$
<!-- The error for L6[3] is -->
<!--    = derivative of activation of  -->
<!--    * sum of activations node leads to -->
$$\delta_3^6 = g'(a_3^6)\sum_x w_{3,x}^{6}\delta_x^{7}$$
$$\delta_x^{7} = g'(a_x^7)\cdot \text{cost}(o_x^7)$$
<!-- $$\Delta w_{ij}^5 = -\alpha\frac{\partial E(X,\theta)}{\partial w_{ij}^5}$$ -->
<!-- $$\delta_1^m = g'_o(a_1^m)(\hat y_d - y_d)$$ -->
