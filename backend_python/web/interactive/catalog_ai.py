COURSES = [
    {
        'slug': 'how-ai-really-works',
        'title': 'How AI Really Works — From Neurons to ChatGPT',
        'category': 'ai',
        'age_range': '12-18+',
        'level': 'Beginner',
        'icon': 'neurology',
        'color': '#6366F1',
        'tagline': 'Train neurons, teach machines to see and discover how ChatGPT-style AI really works — by playing with it.',
        'description': (
            'Artificial Intelligence is not magic — it is elegant mathematics you can actually understand. '
            'This course takes you from zero to ChatGPT in eight hands-on lessons. You will label examples '
            'and watch a machine learn from them, tune a single neuron until it splits data perfectly, roll '
            'a ball down a loss landscape to see gradient descent in action, and build a tiny neural network '
            'that learns XOR. Then you will draw digits and watch a classifier decide what it sees, explore '
            'how language models tokenise and embed words, visualise the attention mechanism that powers '
            'transformers, and watch a Q-learning agent navigate a grid world by trial and error. A ninth '
            'lesson examines how biased training data skews AI decisions — critical knowledge for anyone '
            'building or using AI responsibly.'
        ),
        'skills': [
            'Pattern recognition and nearest-neighbour classification',
            'Perceptron math: weighted sums, bias and activation functions',
            'Gradient descent and loss landscapes',
            'Forward pass and back-propagation in a multi-layer network',
            'Convolutional edge detection and image classification',
            'Tokenisation, word embeddings and vector analogies',
            'Self-attention and the transformer architecture',
            'Q-learning and the exploration–exploitation trade-off',
            'Algorithmic bias detection and fairness metrics',
        ],
        'lessons': [
            # ----------------------------------------------------------------
            # Lesson 1
            # ----------------------------------------------------------------
            {
                'slug': 'what-is-ai',
                'title': 'What Is AI? The Pattern Machine',
                'icon': 'pattern',
                'minutes': 10,
                'sim': 'ai/pattern-machine',
                'sim_type': '2d',
                'summary': (
                    'Label a handful of points as circles or triangles, then watch a 1-nearest-neighbour '
                    'classifier predict new ones in real time. Discover that AI is pattern-matching from '
                    'examples — not magic, and nothing like traditional if-else programming.'
                ),
                'objectives': [
                    'Define AI as a system that learns rules from labelled examples rather than being explicitly programmed',
                    'Demonstrate 1-nearest-neighbour classification by labelling points and observing predictions',
                    'Explain the decision boundary as the line between two classes',
                    'Distinguish AI-based classification from hand-coded if-else rules and state the advantage of each',
                ],
                'knowledge': [
                    {
                        'heading': 'What makes something "Artificial Intelligence"?',
                        'body': (
                            'For most of computing history, programmers wrote explicit rules: '
                            '"if temperature > 100 then boil". Machine learning turned this upside down. '
                            'Instead of writing rules, we show the computer thousands of labelled examples '
                            'and let it extract the rules itself. The resulting system is called an AI model.\n\n'
                            'The classic test is generalisation: can the model correctly handle examples it '
                            'has never seen before? A spam filter that memorises every known spam email but '
                            'cannot catch a new one has not really learned anything useful. AI models are '
                            'evaluated on held-out test data to measure true generalisation ability.\n\n'
                            'Modern AI — from the image recogniser in your phone to ChatGPT — all follow '
                            'this same principle: learn patterns from data, then apply them to new inputs.'
                        ),
                    },
                    {
                        'heading': 'Pattern matching: the 1-Nearest-Neighbour algorithm',
                        'body': (
                            'The simplest classifier imaginable asks a single question: "Which labelled '
                            'example is most similar to this new input?" It then returns that example\'s '
                            'label. This is 1-Nearest Neighbour (1-NN), and despite its simplicity it '
                            'works remarkably well on many real problems.\n\n'
                            'Mathematically, similarity is usually measured as Euclidean distance: '
                            'd = √((x₁−x₂)² + (y₁−y₂)²). The "decision boundary" — the line '
                            'separating predicted classes — is automatically the set of all points '
                            'equidistant from two neighbouring examples of different classes. Add more '
                            'examples and the boundary reshapes itself instantly without rewriting a '
                            'single line of code. That is the power of learning from data.\n\n'
                            'The simulation colours the background to show which class the model would '
                            'predict everywhere in the feature space, and draws a dotted line to the '
                            'nearest labelled point when you move the cursor in Predict mode.'
                        ),
                    },
                    {
                        'heading': 'AI vs traditional programming',
                        'body': (
                            'Traditional programming is deterministic and transparent: a programmer writes '
                            'every rule, so you can read the code and understand exactly what it does. '
                            'It is ideal when rules are known and fixed — calculating taxes, sorting lists, '
                            'running physics simulations.\n\n'
                            'AI shines when the rules are too complex or too numerous to write by hand — '
                            'recognising a face in every possible lighting condition, translating between '
                            'languages, or understanding free-form speech. The trade-off is that the '
                            '"rules" are now millions of numbers (weights) rather than readable code, '
                            'which is why AI interpretability is an active research field.\n\n'
                            'Toggle "Show rule-based code" in the simulation to see the contrast: the '
                            'hand-written if-else rule breaks on data it was not designed for, while the '
                            '1-NN model adapts gracefully to wherever you place examples.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The nearest-neighbour algorithm was first described mathematically in 1951 by Fix and '
                    'Hodges at the US Air Force. Half a century later, almost exactly the same idea powers '
                    'the "Customers who bought this also bought…" recommendations on e-commerce sites.'
                ),
                'quiz': [
                    {
                        'q': 'What is the key difference between traditional programming and machine learning?',
                        'options': [
                            'Traditional programs are faster',
                            'ML programs write the rules automatically from labelled examples; traditional programs need rules coded by hand',
                            'ML uses more memory',
                            'Traditional programs cannot run on modern hardware',
                        ],
                        'answer': 1,
                        'explain': (
                            'Machine learning extracts rules from data; you supply examples and the algorithm '
                            'figures out the pattern. Traditional programming requires a human to specify '
                            'every rule explicitly in code.'
                        ),
                    },
                    {
                        'q': 'In a 1-Nearest-Neighbour classifier, how is a new point classified?',
                        'options': [
                            'By the class that appears most often in the entire dataset',
                            'By flipping a coin',
                            'By copying the label of the closest training example',
                            'By running a neural network',
                        ],
                        'answer': 2,
                        'explain': (
                            '1-NN finds the single nearest labelled point (by Euclidean distance) and '
                            'assigns its class to the new point. It is the simplest possible instance of '
                            'learning from examples.'
                        ),
                    },
                    {
                        'q': 'A hand-coded rule says "if x > 0.5 → Circle". Why might an AI approach be better for complex data?',
                        'options': [
                            'AI rules are always simpler',
                            'The hand-coded rule can only ever capture one straight boundary; an AI model adapts to any shape of boundary that the data shows',
                            'Hand-coded programs cannot run without internet',
                            'AI never makes mistakes',
                        ],
                        'answer': 1,
                        'explain': (
                            'A single if-else boundary is a straight vertical line. Real data often has '
                            'curved, irregular or multi-region boundaries that no simple rule can capture — '
                            'but a learned model adapts automatically to whatever structure the data has.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 2
            # ----------------------------------------------------------------
            {
                'slug': 'the-neuron',
                'title': 'The Artificial Neuron',
                'icon': 'hub',
                'minutes': 12,
                'sim': 'ai/perceptron',
                'sim_type': '2d',
                'summary': (
                    'Adjust weights w₁, w₂ and bias b on a single perceptron and watch the weighted sum '
                    'z = w₁x₁ + w₂x₂ + b flow through a step or sigmoid activation. The decision boundary '
                    'line moves live — grasp the full math of one artificial neuron.'
                ),
                'objectives': [
                    'Compute the weighted sum z = w₁x₁ + w₂x₂ + b for given inputs',
                    'Explain the role of the bias term in shifting the decision boundary',
                    'Compare the step function and sigmoid activation and state when each is preferred',
                    'Read the decision boundary equation w₁x₁ + w₂x₂ + b = 0 from first principles',
                    'Identify a limitation of a single neuron for non-linearly-separable data',
                ],
                'knowledge': [
                    {
                        'heading': 'The biological inspiration and the mathematical model',
                        'body': (
                            'A biological neuron fires an electrical spike when the sum of its synaptic '
                            'inputs exceeds a threshold. Warren McCulloch and Walter Pitts formalised this '
                            'in 1943 as a binary threshold unit, and Frank Rosenblatt built the first '
                            'trainable version — the perceptron — in 1957.\n\n'
                            'The artificial neuron takes n input numbers x₁, x₂, …, xₙ, multiplies each '
                            'by a learned weight wᵢ (positive weights excite, negative inhibit), adds a '
                            'bias b (which acts like a threshold), and passes the total through an '
                            'activation function f: output = f(w₁x₁ + w₂x₂ + … + wₙxₙ + b). The bias '
                            'matters because without it the decision boundary would always pass through the '
                            'origin, severely limiting what the neuron can learn.'
                        ),
                    },
                    {
                        'heading': 'Step functions, sigmoids and the geometry of the boundary',
                        'body': (
                            'The step (Heaviside) activation maps the weighted sum to exactly 0 or 1, '
                            'making the output crisp. The sigmoid σ(z) = 1/(1+e⁻ᶻ) squashes z into (0,1) '
                            'smoothly, which is useful when you want a probability — "87% chance this is a '
                            'cat" — and is essential for training via gradient descent because it has a '
                            'well-defined derivative everywhere.\n\n'
                            'The decision boundary is the set of all inputs where the neuron is exactly on '
                            'the threshold (z = 0), which gives the equation w₁x₁ + w₂x₂ + b = 0. In 2D '
                            'this is a straight line. Rearranging: x₂ = −(w₁x₁ + b)/w₂. Changing w₁ or w₂ '
                            'tilts the line; changing b shifts it parallel to itself. You can see this '
                            'directly in the simulation — move the sliders and watch the boundary respond.'
                        ),
                    },
                    {
                        'heading': 'The XOR problem and the need for multiple neurons',
                        'body': (
                            'A single neuron can only draw one straight line. This means it cannot solve '
                            'XOR: the class of a point (x₁, x₂) where y = 1 iff exactly one of x₁, x₂ is '
                            'large cannot be separated by any line. Minsky and Papert proved this in 1969, '
                            'which temporarily stopped neural-network research.\n\n'
                            'The solution — connecting layers of neurons — was already known in principle '
                            'but took until the 1986 backpropagation paper by Rumelhart, Hinton and '
                            'Williams to become practical. Each hidden neuron in a multi-layer network '
                            'draws its own line; their combination can carve out any shape. That is why '
                            'depth — having many layers — gives neural networks their power.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The first physical perceptron, the Mark I, was built at Cornell in 1958. It had '
                    '400 photocells as inputs, 512 motor-driven potentiometers as weights, and could '
                    'learn to distinguish simple shapes. It weighed several hundred kilograms. Your '
                    'phone does the same computation billions of times per second in a chip the size '
                    'of a thumbnail.'
                ),
                'quiz': [
                    {
                        'q': 'A neuron has w₁=2, w₂=−1, b=0.5 and inputs x₁=1, x₂=3. What is z?',
                        'options': ['3.5', '−0.5', '0.5', '5.5'],
                        'answer': 1,
                        'explain': 'z = w₁x₁ + w₂x₂ + b = 2×1 + (−1)×3 + 0.5 = 2 − 3 + 0.5 = −0.5.',
                    },
                    {
                        'q': 'Why does a single neuron fail to solve XOR?',
                        'options': [
                            'It uses too much memory',
                            'XOR is not a real problem',
                            'A single neuron can only separate data with a straight line, but XOR requires a curved boundary',
                            'The sigmoid activation cannot output 0 or 1',
                        ],
                        'answer': 2,
                        'explain': (
                            'XOR data is not linearly separable — no straight line can correctly divide '
                            'the four XOR input pairs. A single neuron\'s decision boundary is always '
                            'linear, so it cannot learn XOR. Multiple layers are required.'
                        ),
                    },
                    {
                        'q': 'What does the bias term b do in a neuron?',
                        'options': [
                            'It makes the neuron biased and unfair',
                            'It shifts the decision boundary away from the origin, allowing more flexible placement',
                            'It multiplies the output by a constant',
                            'It selects which activation function to use',
                        ],
                        'answer': 1,
                        'explain': (
                            'The bias acts as an adjustable threshold. Without bias, the decision boundary '
                            'always passes through the origin (0, 0), which is unnecessarily restrictive. '
                            'Bias lets the neuron shift the boundary to wherever the data requires.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 3
            # ----------------------------------------------------------------
            {
                'slug': 'teaching-by-mistakes',
                'title': 'Teaching by Mistakes: Gradient Descent',
                'icon': 'trending_down',
                'minutes': 14,
                'sim': 'ai/gradient-descent',
                'sim_type': '2d',
                'summary': (
                    'A ball rolls down a bumpy loss landscape L(w) under gradient descent. Set the '
                    'learning rate and watch overshoot at high rates, glacial progress at low ones, '
                    'and the ball settling in a local minimum. Real gradient steps, real maths.'
                ),
                'objectives': [
                    'Define a loss function and explain why minimising it corresponds to a better model',
                    'State the gradient descent update rule w ← w − α · dL/dw',
                    'Predict qualitatively what happens when the learning rate is too large or too small',
                    'Distinguish a local minimum from a global minimum and explain why this matters',
                ],
                'knowledge': [
                    {
                        'heading': 'The loss function: measuring how wrong the model is',
                        'body': (
                            'To train a model we need a number that measures how badly it is doing — the '
                            'loss function L. For regression this is often mean squared error: '
                            'L = (1/N)Σ(yᵢ − ŷᵢ)². For classification it is usually cross-entropy: '
                            'L = −(1/N)Σ[yᵢ log ŷᵢ + (1−yᵢ) log(1−ŷᵢ)]. Both functions return a '
                            'single positive number: zero when the model is perfect, large when it is wrong.\n\n'
                            'Training a model means finding the model parameters (weights and biases) that '
                            'make L as small as possible. With millions of parameters this is a very hard '
                            'optimisation problem — but gradient descent makes it tractable.'
                        ),
                    },
                    {
                        'heading': 'Gradient descent: following the slope downhill',
                        'body': (
                            'The gradient dL/dw tells you the slope of the loss surface at the current '
                            'parameter value. If dL/dw is positive, the loss increases as w increases — '
                            'so move w left. If negative, move right. The update rule is:\n\n'
                            'w ← w − α · dL/dw\n\n'
                            'where α is the learning rate, a positive number you choose. After many steps '
                            'w slides to a point where dL/dw ≈ 0, a minimum. With one parameter this is '
                            'easy to visualise as a ball rolling downhill on a curve. With a million '
                            'parameters it is the same idea, just in a million-dimensional space — the '
                            'gradient vector points in the direction of steepest ascent, so we step in '
                            'the opposite direction.'
                        ),
                    },
                    {
                        'heading': 'Learning rate, overshoot and local minima',
                        'body': (
                            'The learning rate α is the most critical hyperparameter. Too large and the '
                            'ball overshoots the minimum, bouncing from one side to the other or diverging '
                            'completely. Too small and training takes thousands of steps to converge — '
                            'wasting time and compute. In practice, "learning rate schedules" start large '
                            'and decay over time, combining fast early progress with precise fine-tuning.\n\n'
                            'Real loss surfaces have many local minima — valleys that are not the deepest '
                            'possible valley. Gradient descent can get trapped in one. Deep learning '
                            'networks have so many parameters that most local minima are actually close in '
                            'loss to the global minimum, which is why gradient descent works so well in '
                            'practice despite this theoretical concern. The simulation\'s loss function '
                            'L(w) = (w−2)² + 0.4 sin(4w) + 0.5 includes a global minimum near w = 2 '
                            'and a local minimum to the left — try starting from −3 with a moderate '
                            'learning rate to see the ball get trapped.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Stochastic Gradient Descent (SGD), which uses a random mini-batch of data to '
                    'estimate the gradient at each step, was popularised in neural network training in '
                    'the 1990s. It is still the foundation of every modern deep learning optimiser — '
                    'Adam, RMSProp and AdaGrad are all SGD with clever adaptive step sizes.'
                ),
                'quiz': [
                    {
                        'q': 'The gradient descent update rule is w ← w − α · dL/dw. What happens if you set α = 10 (very large)?',
                        'options': [
                            'The model converges instantly to the global minimum',
                            'The model trains more slowly but safely',
                            'The parameter w may overshoot the minimum and oscillate or diverge',
                            'Nothing — learning rate has no effect',
                        ],
                        'answer': 2,
                        'explain': (
                            'A very large α means each step is huge. The parameter jumps past the minimum '
                            'to the other side, then back again. With extreme values the loss grows '
                            'without bound — training diverges.'
                        ),
                    },
                    {
                        'q': 'At a local minimum, what is the value of dL/dw?',
                        'options': ['1', '−1', '0', 'Equal to the loss itself'],
                        'answer': 2,
                        'explain': (
                            'At any minimum (local or global) the slope of the loss surface is zero: '
                            'dL/dw = 0. Gradient descent then adds zero to w each step, so it has '
                            'converged. The ball has stopped rolling.'
                        ),
                    },
                    {
                        'q': 'Why is a local minimum potentially a problem for training neural networks?',
                        'options': [
                            'Local minima always give zero loss',
                            'Gradient descent may converge to a solution that is not the best possible',
                            'Local minima prevent the network from using all its weights',
                            'There are no local minima in modern deep learning',
                        ],
                        'answer': 1,
                        'explain': (
                            'A local minimum is a point where the gradient is zero but the loss is not '
                            'the smallest possible. Gradient descent cannot escape it without momentum '
                            'or other tricks. In practice deep networks have so many parameters that '
                            'most local minima have nearly the same loss as the global minimum.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 4
            # ----------------------------------------------------------------
            {
                'slug': 'neural-network',
                'title': 'Neural Networks in Action',
                'icon': 'account_tree',
                'minutes': 18,
                'sim': 'ai/neural-net-playground',
                'sim_type': '2d',
                'summary': (
                    'Build a two-layer network (2 inputs → hidden neurons → 1 output) and train it on '
                    'XOR, circle and spiral datasets using real forward pass + backpropagation. '
                    'Watch the decision boundary form, the loss curve fall, and the weight colours '
                    'show which connections matter.'
                ),
                'objectives': [
                    'Describe the architecture of a two-layer fully-connected neural network',
                    'Trace a data point through a forward pass, computing activations layer by layer',
                    'Explain back-propagation as the chain rule applied backwards through the network',
                    'Observe that more hidden neurons allow more complex decision boundaries',
                    'Identify overfitting by watching training loss fall while the boundary over-complexifies',
                ],
                'knowledge': [
                    {
                        'heading': 'Architecture: layers, neurons and connections',
                        'body': (
                            'A fully-connected (dense) neural network is arranged in layers. The input '
                            'layer has one node per input feature. Hidden layers transform the inputs '
                            'through cascaded linear+activation operations. The output layer produces '
                            'the final prediction.\n\n'
                            'In this simulation: 2 input nodes → 1 hidden layer of H neurons (each with '
                            'a ReLU activation: f(z) = max(0, z)) → 1 output node with sigmoid '
                            'activation (outputs a probability). Every neuron in one layer connects to '
                            'every neuron in the next — hence "fully connected". A network with 4 hidden '
                            'neurons has 2×4 + 4 + 4×1 + 1 = 17 learnable parameters in total.'
                        ),
                    },
                    {
                        'heading': 'Forward pass, loss and backpropagation',
                        'body': (
                            'The forward pass computes the prediction: for each hidden neuron i, '
                            'compute zᵢ = Σⱼ wᵢⱼ xⱼ + bᵢ, then aᵢ = ReLU(zᵢ). The output is '
                            'ŷ = σ(Σᵢ W₂ᵢ aᵢ + b₂). Binary cross-entropy loss measures error.\n\n'
                            'Back-propagation (backprop) computes how much each weight contributed to '
                            'the error using the chain rule of calculus. Starting at the output:\n'
                            'δout = ŷ − y (error signal)\n'
                            'dL/dW₂ᵢ = δout · aᵢ  (gradient for output weights)\n'
                            'For hidden weights: δᵢ = δout · W₂ᵢ · ReLU\'(zᵢ)\n'
                            'dL/dwᵢⱼ = δᵢ · xⱼ\n'
                            'Each weight is then nudged opposite to its gradient: w ← w − α · dL/dw. '
                            'This propagates credit (or blame) backwards through every layer.'
                        ),
                    },
                    {
                        'heading': 'Why depth and non-linearity matter',
                        'body': (
                            'Without non-linear activations, stacking linear layers is mathematically '
                            'equivalent to a single linear layer — depth buys nothing. Non-linearities '
                            'like ReLU allow each layer to create new feature combinations that the next '
                            'layer can exploit.\n\n'
                            'The universal approximation theorem (Cybenko, 1989) states that a '
                            'single hidden layer of enough neurons can approximate any continuous '
                            'function. In practice, deep networks (many thin layers) generalise better '
                            'than wide shallow ones because they build hierarchical representations — '
                            'each layer detects increasingly abstract features. GPT-4 has 96 transformer '
                            'layers; that depth allows it to reason over very long-range dependencies.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The word "backpropagation" was coined in the 1970s, but the algorithm became '
                    'famous in 1986 when Rumelhart, Hinton and Williams showed it could train '
                    'multi-layer networks to solve problems that single-layer perceptrons could not. '
                    'Every modern deep-learning framework — PyTorch, TensorFlow, JAX — implements '
                    'automatic differentiation to compute these same gradients.'
                ),
                'quiz': [
                    {
                        'q': 'What does a ReLU activation function compute?',
                        'options': [
                            '1 / (1 + e⁻ᶻ)',
                            'max(0, z)',
                            'z²',
                            'sign(z)',
                        ],
                        'answer': 1,
                        'explain': (
                            'ReLU (Rectified Linear Unit) returns z if z > 0, and 0 otherwise. '
                            'It is written max(0, z). It is the most popular hidden-layer activation '
                            'because it is fast to compute and avoids the vanishing-gradient problem '
                            'that plagued sigmoid activations in deep networks.'
                        ),
                    },
                    {
                        'q': 'In backprop, why do we multiply gradients by the derivative of the activation function?',
                        'options': [
                            'To increase the learning rate automatically',
                            'Because the chain rule requires multiplying by all intermediate derivatives on the path from loss to weight',
                            'To ensure the gradients are positive',
                            'It is a convention, not a mathematical necessity',
                        ],
                        'answer': 1,
                        'explain': (
                            'Back-propagation applies the chain rule: the gradient of the loss w.r.t. '
                            'a weight deep in the network equals the product of all partial derivatives '
                            'along the path from that weight to the loss. The activation derivative '
                            'is one factor in that chain.'
                        ),
                    },
                    {
                        'q': 'You add more hidden neurons and the decision boundary becomes very wiggly but training loss is low. What is happening?',
                        'options': [
                            'The network has converged to the global minimum',
                            'The network is overfitting — it has memorised training data but may not generalise',
                            'The learning rate is too low',
                            'The dataset is too easy',
                        ],
                        'answer': 1,
                        'explain': (
                            'A very complex boundary that fits training data perfectly but is jagged '
                            'or overly detailed is a sign of overfitting. The model has memorised noise '
                            'in the training set rather than learning the true underlying pattern. '
                            'Regularisation, dropout or fewer neurons can help.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 5
            # ----------------------------------------------------------------
            {
                'slug': 'teaching-machines-to-see',
                'title': 'Teaching Machines to See',
                'icon': 'visibility',
                'minutes': 16,
                'sim': 'ai/digit-classifier',
                'sim_type': '2d',
                'summary': (
                    'Draw a digit on an 8×8 pixel grid and watch a nearest-centroid classifier '
                    'recognise it in real time. Toggle edge detection to see a Sobel convolution '
                    'kernel extract outlines — the building block of convolutional neural networks.'
                ),
                'objectives': [
                    'Represent an image as a grid of pixel values and flatten it to a feature vector',
                    'Explain nearest-centroid classification using cosine similarity',
                    'Describe how a convolutional kernel computes a spatial feature map',
                    'Show that edge detection is a specific convolution with the Sobel kernel',
                    'Explain conceptually how CNNs stack convolution layers to recognise complex shapes',
                ],
                'knowledge': [
                    {
                        'heading': 'Images as numbers: pixels, grids and feature vectors',
                        'body': (
                            'A digital image is a rectangular grid of pixels. Each pixel stores one '
                            'intensity value per colour channel — typically 0 (black) to 255 (white) '
                            'for a greyscale image. An 8×8 greyscale image is therefore a vector of '
                            '64 numbers, and classifying it means mapping those 64 numbers to a label.\n\n'
                            'The nearest-centroid classifier stores one "template" (centroid) per class '
                            '— the average pixel pattern of all training examples of that digit. A new '
                            'drawing is classified by computing the cosine similarity between it and '
                            'each centroid and returning the label of the most similar one. Cosine '
                            'similarity measures the angle between two vectors regardless of their '
                            'magnitude, making it robust to how hard or softly you draw.'
                        ),
                    },
                    {
                        'heading': 'Convolution: sliding a filter across an image',
                        'body': (
                            'A convolutional layer applies a small matrix of weights — a kernel or '
                            'filter — to every position in the image by taking the dot product of the '
                            'kernel with the overlapping patch of pixels. Sliding the kernel across '
                            'the whole image produces a new image called a feature map.\n\n'
                            'The Sobel edge-detection kernel is:\n'
                            '  Kₓ = [−1 0 +1 / −2 0 +2 / −1 0 +1]\n'
                            'When applied to a row of pixels, it computes the horizontal gradient — a '
                            'large value where pixel intensity changes sharply from left to right, '
                            'i.e., where there is a vertical edge. A separate kernel detects '
                            'horizontal edges. Toggle the edge-detection mode in the simulation and '
                            'compare the raw pixel grid with the Sobel output.'
                        ),
                    },
                    {
                        'heading': 'Convolutional Neural Networks (CNNs)',
                        'body': (
                            'A CNN replaces handcrafted Sobel kernels with learned kernels. The first '
                            'convolutional layer learns simple detectors (edges, blobs, corners). '
                            'The second layer combines those into textures and curves. Deeper layers '
                            'recognise parts of objects (eyes, wheels), and the deepest layers '
                            'recognise whole objects.\n\n'
                            'LeNet-5 (LeCun, 1998) was the first practical CNN — it read handwritten '
                            'ZIP codes on postal envelopes. AlexNet (2012) stacked five convolutional '
                            'layers and dramatically won the ImageNet competition, launching the modern '
                            'deep-learning era. Vision transformers (ViT, 2020) later replaced '
                            'convolutions with self-attention but the core idea — learning spatial '
                            'feature detectors hierarchically — remains the same.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The MNIST handwritten-digit dataset contains 70,000 labelled examples and has '
                    'been called the "hello world" of machine learning. A well-trained CNN achieves '
                    '99.7% accuracy on it — better than most humans on rushed handwriting.'
                ),
                'quiz': [
                    {
                        'q': 'An 8×8 greyscale image is represented as a feature vector. How many elements does that vector have?',
                        'options': ['8', '16', '64', '256'],
                        'answer': 2,
                        'explain': (
                            '8 rows × 8 columns = 64 pixels. Each pixel is one number, so the '
                            'flattened feature vector has 64 elements.'
                        ),
                    },
                    {
                        'q': 'What does a Sobel kernel detect when applied to an image?',
                        'options': [
                            'The overall brightness of the image',
                            'Edges — regions where pixel intensity changes sharply',
                            'The colour of each pixel',
                            'The frequency content of the image',
                        ],
                        'answer': 1,
                        'explain': (
                            'The Sobel kernel computes the spatial gradient of intensity. Where the '
                            'gradient is large (rapid change from dark to light), there is an edge. '
                            'This is exactly the same principle deep CNNs learn automatically in '
                            'their first convolutional layer.'
                        ),
                    },
                    {
                        'q': 'In a CNN, what is a "feature map"?',
                        'options': [
                            'A lookup table of pixel colours',
                            'The label assigned to each image',
                            'The output of applying a convolutional kernel across the entire input image',
                            'A compressed version of the image',
                        ],
                        'answer': 2,
                        'explain': (
                            'A feature map is the result of sliding a kernel across the input, '
                            'computing the dot product at each position. Each entry in the feature '
                            'map measures how much the corresponding image patch matches the pattern '
                            'the kernel is looking for (e.g., a vertical edge).'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 6
            # ----------------------------------------------------------------
            {
                'slug': 'how-ai-understands-words',
                'title': 'How AI Understands Words',
                'icon': 'text_fields',
                'minutes': 15,
                'sim': 'ai/tokenizer-embeddings',
                'sim_type': '2d',
                'summary': (
                    'Split text into tokens, then explore a 2D embedding space where similar words '
                    'cluster together. Run the classic vector analogy king − man + woman ≈ queen '
                    'interactively and see the maths light up on screen.'
                ),
                'objectives': [
                    'Explain tokenisation as splitting text into sub-word units for processing',
                    'Define a word embedding as a dense vector representing a word\'s meaning',
                    'Interpret clustering in embedding space as semantic similarity',
                    'Perform a vector analogy A − B + C and identify the nearest resulting word',
                    'Explain why embeddings enable AI to handle unseen words via interpolation',
                ],
                'knowledge': [
                    {
                        'heading': 'From characters to tokens: how LLMs read text',
                        'body': (
                            'A language model cannot directly read English characters — it needs numbers. '
                            'The first step is tokenisation: splitting text into a vocabulary of '
                            'sub-word units. GPT-4 uses Byte-Pair Encoding (BPE), which starts from '
                            'individual characters and iteratively merges the most frequent pair until '
                            'reaching a target vocabulary size of ~50,000 tokens.\n\n'
                            'Common words become single tokens ("the", "cat"); rare words are split '
                            '("unhappiness" → "un", "happiness"). This balances vocabulary size against '
                            'the ability to handle any text. The simulation uses a simplified '
                            'word-level tokeniser for clarity — try different sentences and count '
                            'the tokens produced.'
                        ),
                    },
                    {
                        'heading': 'Word embeddings: meaning as coordinates',
                        'body': (
                            'Each token is mapped to a dense vector of floating-point numbers — its '
                            'embedding. GPT-3 uses 12,288-dimensional embeddings; the simulation '
                            'shows a 2D projection for visualisation. The model learns these vectors '
                            'during training so that tokens with similar meanings end up close together '
                            'in the vector space.\n\n'
                            'Why does this work? Tokens that appear in similar contexts have similar '
                            'co-occurrence statistics, and the training objective pushes their vectors '
                            'together. The result is a rich geometric structure: royalty words cluster '
                            'near each other, animal words cluster elsewhere, and the direction from '
                            '"man" to "woman" is similar to the direction from "king" to "queen" — '
                            'because gender is encoded as a consistent direction in the space.'
                        ),
                    },
                    {
                        'heading': 'Vector arithmetic and analogies',
                        'body': (
                            'The famous word2vec analogy king − man + woman ≈ queen was published by '
                            'Mikolov et al. in 2013. It demonstrates that linear algebra in embedding '
                            'space captures semantic relationships. Subtracting "man" from "king" '
                            'removes the "male adult" concept, leaving the "royalty" concept. Adding '
                            '"woman" brings back the female adult, giving a vector closest to "queen".\n\n'
                            'The nearest vector is found by cosine similarity: '
                            'sim(a, b) = (a·b) / (|a||b|). Cosine similarity ignores vector magnitude, '
                            'focusing on direction — which encodes meaning. This same principle '
                            'underlies semantic search (finding documents similar in meaning, not just '
                            'keywords) and retrieval-augmented generation (RAG), used in modern '
                            'AI assistants to look up relevant knowledge before answering.'
                        ),
                    },
                ],
                'fun_fact': (
                    'Word2Vec embeddings trained on Google News (100 billion words) famously captured '
                    'analogies like "Paris : France :: Berlin : Germany" and even '
                    '"CEO : company :: President : country". The model was never taught these facts '
                    'explicitly — it discovered them purely from co-occurrence patterns in text.'
                ),
                'quiz': [
                    {
                        'q': 'What is Byte-Pair Encoding (BPE) used for in language models?',
                        'options': [
                            'Compressing weights to reduce model size',
                            'Tokenising text into sub-word units to balance vocabulary size and coverage',
                            'Encrypting data for privacy',
                            'Reducing the number of attention heads',
                        ],
                        'answer': 1,
                        'explain': (
                            'BPE starts from characters and merges the most frequent adjacent pairs '
                            'iteratively to build a sub-word vocabulary. This means common words '
                            'get single tokens while rare words are split into recognisable pieces, '
                            'giving the model coverage of virtually any text.'
                        ),
                    },
                    {
                        'q': 'In the analogy king − man + woman ≈ queen, what operation links the four words?',
                        'options': [
                            'Pixel subtraction',
                            'Cosine distance',
                            'Vector addition and subtraction in embedding space',
                            'Matrix multiplication',
                        ],
                        'answer': 2,
                        'explain': (
                            'Each word is a vector. Subtracting the "man" vector removes a direction '
                            'encoding maleness; adding the "woman" vector adds femaleness. The result '
                            'vector points toward "queen" — demonstrating that semantic relationships '
                            'are encoded as consistent directions in embedding space.'
                        ),
                    },
                    {
                        'q': 'Why do "cat" and "kitten" cluster near each other in a word embedding space?',
                        'options': [
                            'They have the same number of letters',
                            'They appear in similar contexts in training text, so their embeddings are pushed together',
                            'The algorithm sorts words alphabetically',
                            'They were manually placed close together by engineers',
                        ],
                        'answer': 1,
                        'explain': (
                            'Word embeddings are learned from context. "Cat" and "kitten" appear in '
                            'very similar sentences (with words like "purrs", "meows", "pet"), so '
                            'the training objective moves their vectors close together. Meaning '
                            'emerges from co-occurrence statistics, not explicit programming.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 7
            # ----------------------------------------------------------------
            {
                'slug': 'attention-and-transformers',
                'title': 'Attention Is All You Need',
                'icon': 'center_focus_strong',
                'minutes': 20,
                'sim': 'ai/attention',
                'sim_type': '2d',
                'summary': (
                    'Visualise the self-attention matrix for a chosen sentence — see which words '
                    'attend to which, highlight a query token to read its full attention row, and '
                    'inspect predicted next-token probabilities. Understand how this mechanism '
                    'powers GPT and every modern large language model.'
                ),
                'objectives': [
                    'Explain the Query–Key–Value formulation of self-attention',
                    'Calculate attention weights as softmax(QKᵀ/√d) and explain the scaling factor',
                    'Interpret an attention heatmap: rows are queries, columns are keys',
                    'Explain how multi-head attention lets a token attend to different aspects simultaneously',
                    'Describe the transformer architecture at a block level: attention + FFN + layer norm + residual',
                ],
                'knowledge': [
                    {
                        'heading': 'The attention mechanism: queries, keys and values',
                        'body': (
                            'Self-attention allows each token to "look at" every other token in the '
                            'sequence and weight their importance. Each token position is projected '
                            'into three vectors:\n\n'
                            '• Query (Q): "what am I looking for?"\n'
                            '• Key (K): "what do I contain?"\n'
                            '• Value (V): "what do I communicate?"\n\n'
                            'Attention weights are computed as:\n'
                            'A = softmax(QKᵀ / √d)\n\n'
                            'where d is the dimension of the query vectors. The scaling by √d prevents '
                            'the dot products from becoming very large when d is large, which would '
                            'push softmax into a saturated region with near-zero gradients. The output '
                            'for each token is the weighted sum of all value vectors: output = A·V.'
                        ),
                    },
                    {
                        'heading': 'What attention learns and why it matters',
                        'body': (
                            'In the sentence "The cat sat on the mat that she liked", the word "she" '
                            'should attend strongly to "cat" to resolve the pronoun reference. '
                            'Empirically, attention heads in trained transformers learn to track '
                            'such syntactic and semantic relationships automatically.\n\n'
                            'Multi-head attention runs h independent attention functions in parallel, '
                            'each in a smaller subspace of dimension d/h. Head 1 might track '
                            'subject-verb agreement; head 2 might track coreference; head 3 might '
                            'track positional proximity. The outputs are concatenated and linearly '
                            'projected. GPT-3 uses 96 attention heads across 96 layers — '
                            '9,216 independent attenders in total.'
                        ),
                    },
                    {
                        'heading': 'The transformer block and why it scales',
                        'body': (
                            'Each transformer block consists of:\n'
                            '1. Multi-head self-attention (models inter-token relationships)\n'
                            '2. Feed-forward network (a two-layer MLP applied per-token)\n'
                            '3. Layer normalisation (stabilises training)\n'
                            '4. Residual connections (input added to output, preventing vanishing gradients)\n\n'
                            'Unlike RNNs, transformers process all tokens in parallel, making them '
                            'extremely GPU-friendly. This parallelism enabled scaling to billions of '
                            'parameters. GPT-3 has 175 billion parameters trained on 300 billion '
                            'tokens; GPT-4 is estimated to be larger. The "emergent" abilities '
                            '(reasoning, code generation, analogy) appear once models exceed a '
                            'certain scale — a phenomenon still being studied.'
                        ),
                    },
                ],
                'fun_fact': (
                    'The seminal 2017 paper "Attention Is All You Need" by Vaswani et al. introduced '
                    'the transformer architecture. It was written to improve machine translation '
                    'and had no idea it would become the foundation of ChatGPT, GitHub Copilot, '
                    'DALL-E, AlphaFold 2 and almost every frontier AI system within five years.'
                ),
                'quiz': [
                    {
                        'q': 'In self-attention, what does the attention weight A[i][j] represent?',
                        'options': [
                            'The distance in pixels between tokens i and j',
                            'How much token i attends to (borrows information from) token j',
                            'Whether tokens i and j rhyme',
                            'The weight of the connection from layer i to layer j',
                        ],
                        'answer': 1,
                        'explain': (
                            'A[i][j] is the softmax-normalised dot product between query i and key j. '
                            'A large A[i][j] means token i finds token j highly relevant and borrows '
                            'a large portion of j\'s value vector when computing its output.'
                        ),
                    },
                    {
                        'q': 'Why is the dot product QKᵀ divided by √d before softmax?',
                        'options': [
                            'To make the attention weights sum to d instead of 1',
                            'To prevent large dot products from pushing softmax into saturation, which kills gradients',
                            'To convert angles to radians',
                            'Because d is the number of attention heads',
                        ],
                        'answer': 1,
                        'explain': (
                            'For d-dimensional random vectors with unit variance, the dot product has '
                            'variance d. Dividing by √d normalises the variance back to 1, keeping '
                            'softmax in a region with useful gradients during training.'
                        ),
                    },
                    {
                        'q': 'What major architectural advantage do transformers have over recurrent networks (RNNs) for training?',
                        'options': [
                            'Transformers use less memory',
                            'Transformers can only process 512 tokens at a time',
                            'Transformers process all tokens in parallel, making them vastly faster to train on GPUs',
                            'Transformers do not require back-propagation',
                        ],
                        'answer': 2,
                        'explain': (
                            'RNNs process tokens sequentially — each step depends on the previous — '
                            'so they cannot be fully parallelised. Transformers compute attention '
                            'for all token pairs simultaneously as a matrix operation, which GPUs '
                            'execute extremely efficiently. This parallelism enabled training at '
                            'the scale needed for large language models.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 8
            # ----------------------------------------------------------------
            {
                'slug': 'ai-that-learns-by-playing',
                'title': 'AI That Learns by Playing',
                'icon': 'sports_esports',
                'minutes': 18,
                'sim': 'ai/reinforcement-learning',
                'sim_type': '2d',
                'summary': (
                    'Watch a grid-world agent learn via Q-learning (full Q-table updates) to reach '
                    'the goal and avoid pits. Tune the learning rate, discount factor and epsilon-greedy '
                    'exploration, and watch the value map heat up as the agent discovers the optimal '
                    'policy over hundreds of episodes.'
                ),
                'objectives': [
                    'Define a Markov Decision Process in terms of states, actions, rewards and transitions',
                    'State the Q-learning update rule and identify each term',
                    'Explain the exploration–exploitation trade-off and the role of epsilon-greedy policy',
                    'Interpret a Q-value heatmap as learned expected future reward',
                    'Describe how deep Q-networks (DQNs) extend tabular Q-learning to continuous state spaces',
                ],
                'knowledge': [
                    {
                        'heading': 'Reinforcement learning: agents, environments and rewards',
                        'body': (
                            'In reinforcement learning (RL) an agent interacts with an environment over '
                            'discrete time steps. At each step: the agent observes the current state s, '
                            'chooses an action a, receives a reward r and transitions to a new state s\'.\n\n'
                            'The goal is to maximise cumulative discounted reward: '
                            'G = r₀ + γr₁ + γ²r₂ + … where γ ∈ (0,1) is the discount factor. '
                            'A discount factor close to 1 values future rewards nearly as much as '
                            'immediate ones (far-sighted agent); close to 0 makes the agent greedy '
                            'for immediate reward (short-sighted). This framework, the Markov Decision '
                            'Process (MDP), applies to games (chess, Go, Atari), robotics, '
                            'recommendation systems and drug discovery.'
                        ),
                    },
                    {
                        'heading': 'Q-learning: the Bellman equation made computable',
                        'body': (
                            'Q(s, a) is the expected discounted total reward starting from state s, '
                            'taking action a, and then acting optimally. The Bellman optimality equation '
                            'tells us the true Q values satisfy:\n\n'
                            'Q*(s,a) = E[r + γ · max_{a\'} Q*(s\', a\')]\n\n'
                            'Q-learning (Watkins, 1989) iteratively approaches Q* using the update:\n\n'
                            'Q(s,a) ← Q(s,a) + α[r + γ·max_{a\'} Q(s\',a\') − Q(s,a)]\n\n'
                            'The term in brackets is the temporal difference (TD) error — the difference '
                            'between the current estimate and the bootstrapped target. With enough '
                            'exploration and a decaying learning rate, Q-learning is proven to converge '
                            'to Q* in tabular environments.'
                        ),
                    },
                    {
                        'heading': 'Exploration vs exploitation and deep Q-networks',
                        'body': (
                            'The epsilon-greedy policy balances exploration and exploitation: with '
                            'probability ε choose a random action (explore new possibilities); with '
                            'probability 1−ε choose the action with the highest Q-value (exploit '
                            'current knowledge). ε is usually started high (lots of exploration) '
                            'and decayed over episodes as the agent builds confidence.\n\n'
                            'In the grid world, early episodes have the agent wandering randomly; '
                            'after hundreds of episodes it reliably navigates to the goal. The value '
                            'map heats up — dark cells become golden as the agent learns they lead '
                            'toward reward.\n\n'
                            'Deep Q-Networks (DQN, DeepMind 2015) replaced the Q-table with a neural '
                            'network that takes raw pixels as input and outputs Q-values for all '
                            'actions. DQN achieved superhuman performance on 49 Atari games using '
                            'the same algorithm — only the function approximator changed from a table '
                            'to a convolutional neural network.'
                        ),
                    },
                ],
                'fun_fact': (
                    'AlphaGo (2016) used a combination of deep RL (policy gradient) and Monte Carlo '
                    'tree search to beat world champion Lee Sedol 4–1 at Go — a game with more '
                    'possible positions than atoms in the universe. AlphaZero (2017) learned chess, '
                    'shogi and Go from scratch using only self-play, with no human game data at all.'
                ),
                'quiz': [
                    {
                        'q': 'In Q-learning, Q(s, a) represents:',
                        'options': [
                            'The probability of choosing action a in state s',
                            'The expected total discounted reward from taking action a in state s and acting optimally thereafter',
                            'The immediate reward received after taking action a',
                            'The number of times action a was taken in state s',
                        ],
                        'answer': 1,
                        'explain': (
                            'Q(s,a) is the "quality" of action a in state s — the expected sum of '
                            'all future discounted rewards the agent can achieve by taking a and then '
                            'following the optimal policy. Maximising Q values gives the optimal policy.'
                        ),
                    },
                    {
                        'q': 'What is the purpose of the discount factor γ in the Q-learning update?',
                        'options': [
                            'It controls how many episodes the agent trains for',
                            'It makes the agent prefer immediate rewards over distant future rewards',
                            'It replaces the learning rate',
                            'It sets the exploration probability',
                        ],
                        'answer': 1,
                        'explain': (
                            'Future rewards are multiplied by γᵏ where k is how far in the future they '
                            'are. With γ < 1, distant rewards count less — the agent is somewhat '
                            'impatient. This also ensures the sum converges mathematically. γ = 0.9 '
                            'means a reward 10 steps away is worth 0.9¹⁰ ≈ 35% of an immediate reward.'
                        ),
                    },
                    {
                        'q': 'What is the exploration–exploitation trade-off in reinforcement learning?',
                        'options': [
                            'Whether to train on GPUs or CPUs',
                            'Balancing the risk of trying new actions (exploration) against using the best known action (exploitation)',
                            'Deciding how many hidden layers to use',
                            'Choosing between Q-learning and policy gradient methods',
                        ],
                        'answer': 1,
                        'explain': (
                            'If the agent always exploits, it may never discover better strategies '
                            'than the first one it found. If it always explores, it never uses what '
                            'it has learned. Epsilon-greedy, UCB and Thompson sampling are all '
                            'principled ways to balance this trade-off.'
                        ),
                    },
                ],
            },

            # ----------------------------------------------------------------
            # Lesson 9 (optional ethics lesson)
            # ----------------------------------------------------------------
            {
                'slug': 'ai-ethics',
                'title': 'When AI Gets It Wrong: Bias and Fairness',
                'icon': 'balance',
                'minutes': 14,
                'sim': 'ai/bias-explorer',
                'sim_type': '2d',
                'summary': (
                    'See how skewed historical training data causes a classifier to accept Group A at '
                    'a higher rate than Group B — even when both groups have the same underlying ability. '
                    'Measure disparity with the 80% rule, observe false positive rates, and explore '
                    'mitigation strategies.'
                ),
                'objectives': [
                    'Explain how historical bias in training data propagates into model predictions',
                    'Define disparate impact and apply the 80% (four-fifths) rule',
                    'Distinguish demographic parity, equal opportunity and individual fairness as fairness criteria',
                    'Identify at least three mitigation strategies for algorithmic bias',
                    'Discuss why optimising accuracy alone is insufficient for fair AI systems',
                ],
                'knowledge': [
                    {
                        'heading': 'How training data encodes historical inequality',
                        'body': (
                            'AI models learn patterns from historical data. If past decisions were '
                            'discriminatory — for example, if a minority group was historically '
                            'less likely to be hired regardless of qualification — the model learns '
                            'to replicate those decisions. It does not recognise them as unjust; it '
                            'optimises accuracy on the training set, which faithfully reproduces '
                            'the historical imbalance.\n\n'
                            'Famous real-world examples include COMPAS (a recidivism-prediction tool '
                            'that rated Black defendants as higher risk than white defendants with '
                            'identical criminal histories), Amazon\'s internal hiring algorithm '
                            '(trained on historical CVs, it penalised CVs containing the word '
                            '"women\'s"), and facial-recognition systems that had significantly '
                            'higher error rates on darker-skinned faces due to under-representation '
                            'in training data (Joy Buolamwini & Timnit Gebru, 2018).'
                        ),
                    },
                    {
                        'heading': 'Measuring fairness: disparity, parity and opportunity',
                        'body': (
                            'There is no single "correct" definition of algorithmic fairness — different '
                            'definitions can conflict mathematically. Three commonly used criteria are:\n\n'
                            '• Demographic parity: the acceptance rate is the same across groups.\n'
                            '• Equal opportunity: the true positive rate (recall) is equal across groups '
                            '— qualified individuals have the same chance of being accepted regardless '
                            'of group membership.\n'
                            '• Individual fairness: similar individuals are treated similarly.\n\n'
                            'The US Equal Employment Opportunity Commission\'s "four-fifths rule" states '
                            'that if a selection rate for one group is less than 80% of the highest '
                            'group\'s rate, there is evidence of disparate impact — a legal threshold '
                            'for employment law. The simulation computes this ratio in real time so you '
                            'can see how historical bias drives it below 0.8.'
                        ),
                    },
                    {
                        'heading': 'Mitigation strategies and responsible AI',
                        'body': (
                            'Addressing bias requires intervention at multiple stages:\n\n'
                            '1. Data collection: gather representative data from all groups. Audit '
                            'for selection bias in how historical outcomes were recorded.\n'
                            '2. Pre-processing: re-sample or reweight training data to balance group '
                            'representation. Apply data augmentation for under-represented groups.\n'
                            '3. In-processing: add fairness constraints to the optimisation objective '
                            '(e.g., enforce equal opportunity as a Lagrangian penalty).\n'
                            '4. Post-processing: adjust classifier thresholds separately for each group '
                            'to equalise false positive or true positive rates.\n'
                            '5. Ongoing auditing: regularly test deployed models for drift and emergent '
                            'bias on real-world outcomes.\n\n'
                            'There is no purely technical fix. Fairness is fundamentally a social '
                            'question — which definition of fair is appropriate depends on context, '
                            'stakeholder values and applicable law. Engineers, ethicists, lawyers and '
                            'affected communities all need a seat at the table.'
                        ),
                    },
                ],
                'fun_fact': (
                    'In 2016, Microsoft\'s Tay chatbot was released on Twitter and began producing '
                    'offensive content within 16 hours — it had learned from adversarial user inputs. '
                    'Microsoft shut it down the same day. The incident became a canonical example of '
                    'why responsible AI deployment requires more than just a working model.'
                ),
                'quiz': [
                    {
                        'q': 'Group A has a 70% acceptance rate; Group B has a 50% acceptance rate. What is the disparity ratio?',
                        'options': ['0.50', '0.71', '1.40', '0.20'],
                        'answer': 1,
                        'explain': (
                            'Disparity ratio = (lower rate) / (higher rate) = 50% / 70% ≈ 0.71. '
                            'Since 0.71 < 0.8, this falls below the EEOC four-fifths threshold '
                            'and would be considered evidence of disparate impact.'
                        ),
                    },
                    {
                        'q': 'An AI hiring tool is 95% accurate on the training data but systematically rejects qualified Group B candidates. Why is accuracy alone insufficient?',
                        'options': [
                            '95% is too low — you need 99% minimum',
                            'Accuracy measures overall correctness but can hide systematic errors concentrated in one group',
                            'The tool needs to be retrained with more data',
                            'Accuracy is always the right metric for evaluating fairness',
                        ],
                        'answer': 1,
                        'explain': (
                            'If Group B is a small fraction of the dataset, the model can fail all '
                            'Group B candidates and still report high overall accuracy. Fairness '
                            'metrics — equal opportunity, demographic parity, precision per group — '
                            'must be examined separately to detect group-level disparities.'
                        ),
                    },
                    {
                        'q': 'Which of the following is a post-processing mitigation for algorithmic bias?',
                        'options': [
                            'Collecting more balanced training data',
                            'Adding fairness penalties to the loss function',
                            'Adjusting classification thresholds separately per group to equalise error rates',
                            'Using a larger neural network',
                        ],
                        'answer': 2,
                        'explain': (
                            'Post-processing adjusts the model\'s outputs after training — for example, '
                            'choosing a lower acceptance threshold for Group B to equalise true positive '
                            'rates. It does not change the model itself. Pre-processing changes data; '
                            'in-processing changes the training objective.'
                        ),
                    },
                ],
            },
        ],
    },
]
