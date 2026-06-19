COURSES = [
    {
        'slug': 'ai-from-scratch',
        'title': 'Artificial Intelligence — From Scratch',
        'category': 'ai',
        'age_range': '12+',
        'level': 'Beginner',
        'icon': 'neurology',
        'color': '#6366F1',
        'tagline': 'No maths degree, no coding needed — build a neuron, train a network and meet the ideas behind ChatGPT, hands-on.',
        'description': 'Artificial intelligence can feel like magic, but it is built from surprisingly simple ideas that anyone can understand and even play with. In this course you will discover what AI really is, light up a single 3D neuron and watch it think, train a tiny neural network by nudging it with examples, draw a line that separates cats from dogs, watch a model recognise handwritten shapes, and peek inside the architecture that powers ChatGPT. Every lesson pairs a real, working simulation with plain-language explanation — by the end you will not just have heard of AI, you will have built pieces of it yourself.',
        'skills': [
            'What AI, machine learning and deep learning actually mean',
            'How an artificial neuron turns inputs into an output',
            'How training uses examples and error to improve a model',
            'Linear classification and decision boundaries',
            'The basics of neural networks and how language models work',
        ],
        'lessons': [
            {
                'slug': 'what-is-ai',
                'title': 'What Is AI, Really?',
                'icon': 'smart_toy',
                'minutes': 11,
                'sim': 'ai/what-is-ai',
                'sim_type': '2d',
                'summary': 'Sort the world into "things a computer can just be told" versus "things it has to learn from examples" — and meet the simple idea that makes modern AI possible.',
                'objectives': [
                    'Distinguish traditional programming from machine learning',
                    'Explain what AI, ML and deep learning are and how they relate',
                    'Recognise where AI already appears in everyday life',
                    'Give one example of a task AI is good at and one it struggles with',
                ],
                'knowledge': [
                    {
                        'heading': 'Telling versus learning',
                        'body': 'For most of computing history, a program could only do exactly what a human wrote down as rules. Want a computer to spot spam email? You write rules: if it contains "FREE MONEY", if it has too many capitals, if it comes from a blocked sender… The trouble is that list never ends, and spammers adapt faster than you can write rules.\n\nMachine learning flips the problem. Instead of giving the computer rules, you give it hundreds of examples of spam and not-spam, and let it discover the patterns itself. The computer writes its own rules — far more, and far subtler, than any human could. That single shift, from "tell the computer" to "let it learn", is the engine behind almost every AI breakthrough you have heard of.',
                    },
                    {
                        'heading': 'The three nested circles',
                        'body': 'Artificial intelligence is the big umbrella — any technique that makes a machine seem to think. Inside AI sits machine learning (ML): systems that improve at a task by learning from data rather than following hand-written rules. Inside ML sits deep learning: machine learning that uses many-layered neural networks, inspired by the wiring of the brain.\n\nSo every deep learning system is machine learning, and every machine learning system is AI — but not the other way round. ChatGPT, image generators and self-driving vision are deep learning; a spam filter might be simpler ML; a chess-playing program that searches millions of moves is classic AI without much learning at all. In the simulation, drag each example into the ring where it belongs.',
                    },
                    {
                        'heading': 'AI is already everywhere',
                        'body': 'You use AI dozens of times a day. When your phone unlocks by recognising your face, that is deep learning on an image. When YouTube suggests a video you actually want, that is a recommender system learning your taste. When Google Translate turns Nepali into English in an instant, when a map app predicts your arrival time, when a doctor gets an early warning from an X-ray — all AI.\n\nBut AI has real limits. It is only as good as its training data, it can be confidently wrong, and it has no common sense or true understanding. It spots statistical patterns brilliantly; it does not "know" anything in the human sense. Knowing both the power and the limits is the first step to using AI well — and the rest of this course shows you exactly how that power is built.',
                    },
                ],
                'fun_fact': 'The term "artificial intelligence" was coined back in 1956 at a small summer workshop at Dartmouth College — yet it took almost 60 years of faster computers and bigger datasets before AI became the everyday tool it is today.',
                'quiz': [
                    {
                        'q': 'What is the key difference between traditional programming and machine learning?',
                        'options': ['ML is faster', 'ML learns patterns from data instead of following hand-written rules', 'ML needs no data', 'ML uses bigger computers'],
                        'answer': 1,
                        'explain': 'In ML, the machine discovers its own rules from examples; in traditional programming a human must write every rule.',
                    },
                    {
                        'q': 'Which is the correct nesting?',
                        'options': ['ML contains AI contains deep learning', 'AI contains deep learning contains ML', 'AI contains ML contains deep learning', 'They are all the same thing'],
                        'answer': 2,
                        'explain': 'AI is the broadest field; ML is a subset of AI; deep learning is a subset of ML that uses neural networks.',
                    },
                    {
                        'q': 'A face-unlock feature on a phone is an example of…',
                        'options': ['A hand-written rule', 'Deep learning on images', 'A calculator', 'Not AI at all'],
                        'answer': 1,
                        'explain': 'Recognising a face needs pattern learning from millions of face images — a classic deep-learning task.',
                    },
                ],
            },
            {
                'slug': 'meet-the-neuron',
                'title': 'Meet the Neuron',
                'icon': 'hub',
                'minutes': 14,
                'sim': 'ai/neuron',
                'sim_type': '3d',
                'summary': 'Light up a single 3D artificial neuron: feed it inputs, weight them, push the sum through an activation function and watch it fire.',
                'objectives': [
                    'Describe an artificial neuron as weighted inputs plus an activation',
                    'Explain what weights and biases do',
                    'Show how a non-linear activation lets a neuron "fire"',
                    'Predict whether a neuron will output high or low for given inputs',
                ],
                'knowledge': [
                    {
                        'heading': 'A neuron is a tiny decision-maker',
                        'body': 'An artificial neuron is a simplified mathematical model of a brain cell, and it is the atom from which all neural networks are built. It takes several numbered inputs — think of them as signals arriving along wires — multiplies each by a number called a weight, and adds them all up along with a bias term. The weight says how important each input is; the bias shifts the whole score up or down.\n\nThat sum is then passed through an activation function, which squashes the result into a final output. If the weighted sum is high enough, the neuron "fires" and outputs a value near 1; if not, it stays quiet near 0. A single neuron is, in effect, a tiny decision-maker: "given these inputs, with these importances, should I switch on?"',
                    },
                    {
                        'heading': 'Weights and bias',
                        'body': 'The weights are where the neuron\'s knowledge lives. Suppose a neuron decides "should I take an umbrella?" from two inputs: is it cloudy, and did the forecast say rain. If cloudiness matters less than the forecast, the forecast input gets a bigger weight. The neuron multiplies each input by its weight, adds them, and the bigger the total, the more it leans towards "yes, take one".\n\nThe bias is like the neuron\'s default mood — a number added to the sum before the activation. A high positive bias makes the neuron trigger easily ("paranoid, always carries an umbrella"); a strongly negative bias makes it reluctant. Tweaking the weights and bias is exactly what training does: learning is the slow adjustment of these numbers until the neuron gives the right answers.',
                    },
                    {
                        'heading': 'Why activation matters',
                        'body': 'Without an activation function, a neuron would just multiply and add — and a whole network of pure adders could be collapsed back into one big linear equation, able only to draw straight boundaries. The activation function bends that line, letting the neuron respond non-linearly: small inputs are ignored, then suddenly the neuron snaps on.\n\nThe most popular activation today is called ReLU (Rectified Linear Unit): it outputs zero for any negative sum and the raw value for any positive one — dead simple, yet stacked in millions it produces everything from image recognition to ChatGPT. In the simulation, drag the input sliders, watch the weighted sum add up on the glowing wires, and see the output light up when it crosses the activation threshold.',
                    },
                ],
                'fun_fact': 'The human brain has roughly 86 billion neurons, each connected to thousands of others — but a single artificial neuron, on its own, can already decide simple yes/no questions surprisingly well.',
                'quiz': [
                    {
                        'q': 'Inside a neuron, each input is first…',
                        'options': ['Ignored', 'Multiplied by a weight', 'Turned into text', 'Stored permanently'],
                        'answer': 1,
                        'explain': 'Each input is multiplied by its weight (its importance), then the weighted inputs are summed with the bias.',
                    },
                    {
                        'q': 'What is the role of the bias term?',
                        'options': ['It makes the neuron faster', 'It shifts the activation threshold up or down', 'It stores images', 'It connects neurons'],
                        'answer': 1,
                        'explain': 'The bias is added to the weighted sum, setting how easily the neuron fires — like a built-in default lean.',
                    },
                    {
                        'q': 'Why do we need a non-linear activation function?',
                        'options': ['To slow the network down', 'So stacked neurons can learn complex, curved patterns', 'To store more data', 'Activation is optional'],
                        'answer': 1,
                        'explain': 'Non-linear activations bend the decision boundary, letting networks of neurons learn patterns far beyond straight lines.',
                    },
                ],
            },
            {
                'slug': 'how-machines-learn',
                'title': 'How Machines Learn',
                'icon': 'model_training',
                'minutes': 15,
                'sim': 'ai/how-ml-learns',
                'sim_type': '2d',
                'summary': 'Watch a tiny network learn in real time: scatter points, press train, and see the loss fall and the network gradually fit the pattern — the core loop of all machine learning.',
                'objectives': [
                    'Explain the train-and-test loop of machine learning',
                    'Describe a loss function as a measure of wrongness',
                    'Show how gradient descent nudges weights to reduce error',
                    'Distinguish underfitting from overfitting',
                ],
                'knowledge': [
                    {
                        'heading': 'The learning loop',
                        'body': 'Machine learning, however fancy the model, almost always boils down to the same loop. You show the model an example, it makes a guess, you compare the guess to the right answer, and you measure how wrong it was with a single number called the loss. Then you tweak the model\'s internal numbers (the weights) a tiny step in the direction that would have made the loss smaller. Repeat thousands or millions of times, and the model slowly gets better.\n\nThis loop — predict, measure, adjust — is the heartbeat of training. A modern neural network might run it billions of times across millions of examples, each time shaving a sliver off the error. In the simulation you can watch a real (tiny) network train before your eyes: press Train, and you will see the loss number fall as the model\'s predictions creep closer to the true pattern.',
                    },
                    {
                        'heading': 'Loss and gradient descent',
                        'body': 'The loss is a score for how badly the model is doing — zero means perfect. There are many ways to compute it (mean squared error for numbers, cross-entropy for categories), but the goal is always the same: make it smaller. The clever part is knowing which way to nudge each weight to achieve that.\n\nImagine you are blindfolded on a hilly landscape, trying to reach the lowest valley. You feel the slope under your feet and take a step downhill. That is gradient descent: the model computes the slope of the loss with respect to each weight, then takes a small step (set by the learning rate) downhill. Too big a step and you leap across the valley; too small and you crawl. Getting this right is much of the art of training AI.',
                    },
                    {
                        'heading': 'Underfitting and overfitting',
                        'body': 'A model that has barely learned anything is too simple to capture the pattern — it draws a straight line through curvy data. This is underfitting: high loss on both training and new data. At the other extreme, a model with too much capacity can memorise the training examples, including their noise, and fail completely on anything new. This is overfitting: tiny training loss but terrible real-world performance.\n\nGood machine learning finds the sweet spot: a model flexible enough to capture the real pattern, but not so flexible that it memorises accidents. We guard against overfitting by splitting data into training and test sets, by adding regularisation, and — most honestly — by always checking the model on data it has never seen. In the simulation you can crank up the complexity and watch overfitting appear as the line wiggles violently to chase every point.',
                    },
                ],
                'fun_fact': 'Training a large language model like GPT-4 can take months across thousands of GPUs and cost tens of millions of dollars in electricity — yet the core loop it runs is the same predict-measure-adjust you will play with here.',
                'quiz': [
                    {
                        'q': 'In the training loop, the loss is…',
                        'options': ['The number of weights', 'A measure of how wrong the prediction was', 'The learning rate', 'The amount of data'],
                        'answer': 1,
                        'explain': 'Loss quantifies the error between the model\'s prediction and the correct answer — training aims to minimise it.',
                    },
                    {
                        'q': 'Gradient descent chooses how to change each weight by…',
                        'options': ['Random guessing', 'Following the slope of the loss downhill', 'Always increasing it', 'Copying the input'],
                        'answer': 1,
                        'explain': 'It computes the gradient (slope) of the loss for each weight and nudges the weight a small step in the direction that reduces loss.',
                    },
                    {
                        'q': 'A model that has memorised the training data, noise and all, and fails on new data is…',
                        'options': ['Underfitting', 'Overfitting', 'Perfectly trained', 'Untrained'],
                        'answer': 1,
                        'explain': 'Overfitting fits the training data too closely, including its quirks, so it generalises poorly to new examples.',
                    },
                ],
            },
            {
                'slug': 'line-of-decision',
                'title': 'Drawing the Line: Classifiers',
                'icon': 'show_chart',
                'minutes': 13,
                'sim': 'ai/perceptron',
                'sim_type': '2d',
                'summary': 'Scatter red and blue dots, then drag a dividing line until it separates the two groups — and watch a perceptron find that line automatically.',
                'objectives': [
                    'Explain a classifier as drawing a boundary between groups',
                    'Show how a perceptron learns a linear decision boundary',
                    'Describe what is meant by features in machine learning',
                    'Recognise when data is not linearly separable',
                ],
                'knowledge': [
                    {
                        'heading': 'Sort by drawing a line',
                        'body': 'Many machine-learning tasks come down to sorting things into groups: is this email spam or not, is this cell healthy or cancerous, is this image a cat or a dog? The simplest possible classifier, the perceptron, does this by drawing a single straight line through the data: points on one side are class A, points on the other are class B.\n\nTo draw that line, the perceptron needs to measure each example with numbers called features. To tell cats from dogs you might use "height" and "ear length" as two features, plotting each animal as a dot. The perceptron learns the line that best separates the cat-dots from the dog-dots. Drag the line in the simulation and watch the classification flip across it.',
                    },
                    {
                        'heading': 'How the perceptron learns',
                        'body': 'The perceptron starts with a random line, which is almost certainly wrong. Then it looks at each point in turn: if the point is already on the correct side, nothing happens; if it is on the wrong side, the perceptron nudges the line slightly towards placing it correctly. After enough passes through the data, the line settles into a position that separates the groups — assuming such a line exists.\n\nThis elegant rule, invented in 1958, was the first machine-learning algorithm ever implemented in hardware. It cannot solve every problem (more on that next), but it captures the essence of all classifiers: find a boundary in feature space that sorts the examples correctly. Modern classifiers do the same thing, just with curved, high-dimensional boundaries learned by deep networks.',
                    },
                    {
                        'heading': 'When a line is not enough',
                        'body': 'Some data simply cannot be separated by a straight line. The classic example is the XOR problem: four points arranged so that no single line can put the right pairs together. For years this stumped early neural network research, because a one-neuron perceptron provably cannot solve it.\n\nThe breakthrough was stacking perceptrons into layers — a multi-layer network, or multi-layer perceptron. With a hidden layer in between, the network can combine several straight lines into curved, complex boundaries, solving XOR and vastly more intricate problems. That insight, that depth creates power, is what eventually grew into the deep learning that runs modern AI. Toggle the "hidden layer" in the simulation and watch a curved boundary appear where no straight line could ever work.',
                    },
                ],
                'fun_fact': 'The perceptron was first built as a physical machine in 1958 — the Mark I Perceptron, a cabinet of motors and photocells that learned to recognise simple shapes projected onto a 20×20 grid of light sensors.',
                'quiz': [
                    {
                        'q': 'A classifier like a perceptron separates groups by…',
                        'options': ['Memorising each example', 'Drawing a decision boundary through the feature space', 'Sorting alphabetically', 'Deleting the data'],
                        'answer': 1,
                        'explain': 'A classifier learns a boundary in feature space; examples on each side are assigned to a different class.',
                    },
                    {
                        'q': 'In machine learning, "features" are…',
                        'options': ['The classes themselves', 'Measured numbers describing each example', 'The names of the programmers', 'Random noise'],
                        'answer': 1,
                        'explain': 'Features are the measurable properties (like height, weight, pixel values) used as inputs to describe each example.',
                    },
                    {
                        'q': 'Why can a single perceptron not solve the XOR problem?',
                        'options': ['It is too slow', 'The four XOR points cannot be separated by any straight line', 'It has no inputs', 'XOR uses too many features'],
                        'answer': 1,
                        'explain': 'XOR is not linearly separable — no single line works. A multi-layer network, combining several lines, is needed.',
                    },
                ],
            },
            {
                'slug': 'teaching-machines-to-see',
                'title': 'Teaching Machines to See',
                'icon': 'image_search',
                'minutes': 14,
                'sim': 'ai/image-classifier',
                'sim_type': '2d',
                'summary': 'Draw a digit, and watch a simple image classifier guess what you wrote — then peek inside to see how it turns pixels into a prediction.',
                'objectives': [
                    'Describe an image as a grid of pixel numbers',
                    'Explain how a classifier maps pixels to a class probability',
                    'Recognise why convolutional networks excel at images',
                    'Interpret a confusion matrix and class probabilities',
                ],
                'knowledge': [
                    {
                        'heading': 'An image is just numbers',
                        'body': 'To a computer, a photograph is not a picture at all — it is a grid of numbers. A small grey image of 28 by 28 pixels is just 784 numbers, each between 0 (black) and 255 (white). A colour photo is three such grids stacked together, for red, green and blue. Everything a vision system does begins with these raw numbers.\n\nThe miracle is that, given enough examples, a neural network can learn which arrangements of these numbers correspond to "a cat", "a stop sign" or "the digit 7". It does so by learning patterns at every scale: tiny edges, then shapes built from edges, then objects built from shapes — layer by layer, more and more abstract. Draw a digit in the simulation and the classifier will turn your strokes into 784 numbers and read them.',
                    },
                    {
                        'heading': 'From pixels to prediction',
                        'body': 'A simple image classifier works much like the neuron you met earlier, just with hundreds of inputs instead of two. Each of the 784 pixels feeds into the network with its own learned weight; the network multiplies and adds, passes the result through activations, and finally outputs a score for each possible class — "I am 92% sure this is a 7, 5% sure it is a 1, and so on."\n\nThat final layer of probabilities is what we call the model\'s prediction. The class with the highest score wins. In the simulation, after you draw, you will see the full list of probabilities light up — even when the model is wrong, you can see its second or third guess, which is often revealing about which features it got confused by.',
                    },
                    {
                        'heading': 'Why convolutions changed everything',
                        'body': 'Treating every pixel independently works for tiny digits, but real photographs have structure that a flat network throws away: an eye is an eye whether it is in the top-left or bottom-right of the photo. Convolutional neural networks (CNNs) exploit this by sliding small pattern-detectors across the whole image, so a feature learned in one place automatically works everywhere.\n\nThis single idea — local, reusable pattern detectors stacked in layers — is what made modern computer vision possible. It powers face recognition, medical image diagnosis, self-driving cars and the vision systems in your phone. The classifier you draw on here is deliberately small and fast, but it uses the same core idea: turn pixels into progressively more meaningful features, then read off a prediction.',
                    },
                ],
                'fun_fact': 'A famous 2012 system called AlexNet cut the error rate on a giant image-recognition benchmark almost in half overnight — the moment the world realised deep learning was real, and the spark that lit the modern AI boom.',
                'quiz': [
                    {
                        'q': 'To a computer, a 28×28 greyscale image is…',
                        'options': ['A single number', '784 pixel values arranged in a grid', 'A photograph', 'A line of text'],
                        'answer': 1,
                        'explain': '28×28 = 784 pixels, each a number from 0 (black) to 255 (white). Vision begins with these numbers.',
                    },
                    {
                        'q': 'The output of an image classifier is typically…',
                        'options': ['A single true/false', 'A probability for each possible class', 'A new image', 'A random guess'],
                        'answer': 1,
                        'explain': 'Classifiers output a score (often a probability) for each class; the highest-scoring class is the prediction.',
                    },
                    {
                        'q': 'Convolutional networks are powerful for images because they…',
                        'options': ['Use bigger computers', 'Slide pattern-detectors across the image so features work in any position', 'Memorise every photo', 'Ignore pixels'],
                        'answer': 1,
                        'explain': 'Convolutions learn local patterns (edges, shapes) that are shared across the image, making vision far more efficient and accurate.',
                    },
                ],
            },
            {
                'slug': 'neural-networks-in-3d',
                'title': 'Inside a Neural Network',
                'icon': 'account_tree',
                'minutes': 14,
                'sim': 'ai/network-3d',
                'sim_type': '3d',
                'summary': 'Fly through a 3D neural network: watch signals travel along weighted connections from input layer to output, lighting up neurons as they fire.',
                'objectives': [
                    'Describe the structure of a feed-forward neural network',
                    'Explain the role of input, hidden and output layers',
                    'Show how information flows forward through weighted connections',
                    'Connect network depth to the complexity of patterns it can learn',
                ],
                'knowledge': [
                    {
                        'heading': 'Layers of neurons',
                        'body': 'A single neuron can only make simple decisions, but wire many together in layers and something remarkable emerges. A typical feed-forward network has an input layer (one neuron per feature — for a 28×28 image, 784 inputs), one or more hidden layers in the middle, and an output layer (one neuron per possible answer — say, 10 neurons for the digits 0–9).\n\nEach neuron in one layer connects to every neuron in the next, and each connection carries its own weight. The hidden layers are where the real work happens: early hidden neurons detect simple features, and deeper layers combine those into ever more abstract concepts — edges become shapes, shapes become objects. The whole network is just millions of the tiny neurons you met earlier, wired in sequence.',
                    },
                    {
                        'heading': 'The forward pass',
                        'body': 'When you feed the network an input, a wave of activity travels forward from layer to layer — the forward pass. Each neuron receives weighted signals from all the neurons behind it, sums them, adds its bias, applies its activation, and passes its own output onward. By the time the signal reaches the final layer, the output neurons hold the network\'s answer — a probability for each possible class.\n\nIn the 3D model you can watch this happen as light flowing along the connections, with neurons glowing brighter as they fire more strongly. The thickness or colour of each wire reflects its weight: strong connections dominate the signal, weak ones barely matter. After training, this tangled web of weights is, literally, the network\'s learned knowledge encoded as numbers.',
                    },
                    {
                        'heading': 'Why depth matters',
                        'body': 'A network with a single hidden layer can, in principle, approximate almost any function — but it might need an astronomical number of neurons to do so. Depth turns out to be far more efficient: stacking many modest layers lets each one build on the last, composing simple features into complex ones with relatively few total neurons.\n\nThis is why the field is called deep learning — "deep" simply means many layers. A modern image network might have 50 to 200 layers; a large language model like GPT-4 has around 100. Each added layer gives the network the capacity to represent one more level of abstraction, which is why depth, more than width or raw neuron count, has driven the leap from digit-recognition to systems that can hold a conversation.',
                    },
                ],
                'fun_fact': 'The "deep" in deep learning has no precise definition — researchers jokingly define it as "more layers than the previous paper used". Today\'s largest models stack over a hundred.',
                'quiz': [
                    {
                        'q': 'In a feed-forward network, the hidden layers sit between the…',
                        'options': ['Output and the user', 'Input layer and the output layer', 'Weights and biases', 'Computer and the internet'],
                        'answer': 1,
                        'explain': 'Hidden layers are the intermediate layers between the input features and the final output neurons.',
                    },
                    {
                        'q': 'During a forward pass, information flows…',
                        'options': ['From output to input', 'From the input layer forward to the output', 'In random directions', 'Only within one layer'],
                        'answer': 1,
                        'explain': 'In a forward pass each neuron computes its output from the layer behind it and passes the signal onward to the next layer.',
                    },
                    {
                        'q': 'Why are deep (many-layered) networks often more powerful than a single huge layer?',
                        'options': ['They are faster', 'Each layer can compose features from the last, building abstractions efficiently', 'They use less data', 'They have no weights'],
                        'answer': 1,
                        'explain': 'Depth lets each layer build on the previous one, composing simple features into complex patterns with far fewer total neurons.',
                    },
                ],
            },
            {
                'slug': 'how-language-models-work',
                'title': 'How ChatGPT Works',
                'icon': 'forum',
                'minutes': 15,
                'sim': 'ai/llm-intro',
                'sim_type': '2d',
                'summary': 'Type a few words and watch a language model predict the next one — the simple, surprising mechanism behind every chatbot from ChatGPT to Gemini.',
                'objectives': [
                    'Explain a language model as next-token prediction',
                    'Describe how text is broken into tokens',
                    'Show how attention lets a model focus on relevant context',
                    'Distinguish training a model from using (prompting) it',
                ],
                'knowledge': [
                    {
                        'heading': 'Guess the next word',
                        'body': 'Despite all the magic, a large language model like ChatGPT is doing essentially one thing: predicting the next piece of text. Given "The cat sat on the…", it computes the most likely next word — almost certainly "mat". Then it takes "The cat sat on the mat" as the new input and predicts the next word again, and again, building up a response one piece at a time. That is the entire trick.\n\nWhat makes this powerful is scale. Trained on billions of pages of text, the model has effectively memorised the statistical patterns of human language — grammar, facts, reasoning styles, even tone. Predict the next word well enough, across enough context, and the result looks astonishingly like genuine understanding. In the simulation you can type the start of a sentence and watch the model\'s ranked guesses for what comes next.',
                    },
                    {
                        'heading': 'Tokens, not words',
                        'body': 'Language models do not actually work with whole words — they work with tokens, small chunks that might be a word, part of a word, or even a single character. "ChatGPT" might be one token; "unbelievable" might be split into "un", "believ" and "able". A typical token is about four characters. Breaking text this way lets one model handle any language, including ones with no spaces between words, and lets it spell out even rare words it has never seen.\n\nThe number of tokens also dictates the model\'s context window — how much recent text it can keep in mind at once. A small model might remember a few thousand tokens; the largest models today handle over a million, enough to read a whole book in one go. Beyond the window, earlier text simply falls out of view.',
                    },
                    {
                        'heading': 'Attention is all you need',
                        'body': 'In 2017 a single research paper titled "Attention Is All You Need" changed AI forever. It introduced the Transformer, an architecture built around a mechanism called attention that lets every token look back at every earlier token and decide which ones matter most for its prediction. To predict "it" in "the dog chased the cat because it…", attention lets the model focus on "dog" or "cat" to decide what "it" refers to.\n\nThis ability to weigh relevant context, no matter how far back, is what made Transformers so good at language that they swept the field. Every major modern model — GPT, Gemini, Llama — is a Transformer. They are still, at heart, predicting the next token; attention is what makes that prediction context-aware enough to produce fluent, useful, and sometimes astonishingly intelligent-seeming text.',
                    },
                ],
                'fun_fact': 'The "GPT" in ChatGPT stands for "Generative Pre-trained Transformer" — three words that together describe exactly what it is: a Transformer that generates text, pre-trained on a huge corpus before you ever talk to it.',
                'quiz': [
                    {
                        'q': 'At its core, a large language model is trained to…',
                        'options': ['Translate languages only', 'Predict the next token of text', 'Store facts permanently', 'Recognise faces'],
                        'answer': 1,
                        'explain': 'LLMs are next-token predictors: given the text so far, they estimate the most likely next piece of text.',
                    },
                    {
                        'q': 'A "token" in a language model is…',
                        'options': ['Always a whole word', 'A small chunk of text, often part of a word', 'A single letter only', 'A password'],
                        'answer': 1,
                        'explain': 'Tokens are sub-word chunks that let one model handle any language and spell out even rare or unseen words.',
                    },
                    {
                        'q': 'The Transformer architecture is powerful because of a mechanism called…',
                        'options': ['Gradient descent', 'Attention, which weighs relevant context', 'Activation', 'The bias term'],
                        'answer': 1,
                        'explain': 'Attention lets each token focus on the most relevant earlier tokens, giving Transformers their context-aware power.',
                    },
                ],
            },
            {
                'slug': 'ai-in-your-life',
                'title': 'AI Ethics, Bias & Your Future',
                'icon': 'psychology',
                'minutes': 12,
                'sim': 'ai/ethics',
                'sim_type': '2d',
                'summary': 'Spot the bias in a hiring algorithm, weigh the risks of a self-driving car, and decide where you would — and would not — trust an AI to make a decision.',
                'objectives': [
                    'Explain how bias enters AI through training data',
                    'Describe privacy, fairness and accountability concerns',
                    'Recognise tasks where AI is trustworthy versus risky',
                    'Form a balanced view of AI\'s benefits and harms',
                ],
                'knowledge': [
                    {
                        'heading': 'AI inherits human bias',
                        'body': 'A machine learning model can only learn from the data it is given — and that data was made by humans, complete with all our prejudices. If a hiring model is trained on past hiring decisions from a company that historically favoured men, the model will dutifully learn to favour men too, because that is the pattern in the data. The AI is not neutral; it is a mirror held up to society.\n\nThis has caused real harm: face-recognition systems that fail on dark-skinned faces because they were trained mostly on light-skinned ones, credit-scoring models that penalise postcodes in poorer neighbourhoods, translation tools that default doctors to "he" and nurses to "she". Spotting and removing such bias is one of the hardest and most important problems in AI today — and it begins with diverse data and diverse teams.',
                    },
                    {
                        'heading': 'Who is responsible?',
                        'body': 'When a self-driving car crashes, or an AI denies someone a loan, who is to blame? The programmer? The company? The model itself? Our laws and ethics were built around humans making decisions; an AI that makes millions of decisions per second does not fit neatly into that frame. This is the accountability problem, and it is unsolved.\n\nClosely tied is privacy. Modern AI is fed on vast troves of personal data — what you click, where you walk, the photos you upload. That data can power wonderfully useful services, but it can also be misused for surveillance, manipulation or discrimination. Asking "who owns this data, who can see it, and what is it used to decide about me?" is now a basic digital literacy skill.',
                    },
                    {
                        'heading': 'Tools, not replacements',
                        'body': 'Despite the headlines, AI today is best thought of as a powerful tool that augments humans, not a replacement for them. A doctor with an AI assistant that flags suspicious X-rays catches more cancers than either alone; a programmer with an AI coding helper ships faster; a student with an AI tutor gets patient, personalised explanations. The pattern is human-plus-AI outperforming either alone.\n\nBut that only holds where we use AI thoughtfully — checking its work, understanding its limits, and never delegating high-stakes moral decisions to a statistical pattern-matcher. Some jobs will indeed change or disappear, just as they did with electricity and the internet; new ones will be created. Your best preparation is not to compete with AI but to learn how to use it well, critically and ethically. The future belongs to people who can tell a good AI output from a confident-sounding wrong one.',
                    },
                ],
                'fun_fact': 'One famous image-recognition system was once tricked into classifying a picture of a turtle as a rifle — a reminder that AI "sees" patterns, not meaning, and can be fooled in ways no human ever would be.',
                'quiz': [
                    {
                        'q': 'Bias in an AI system usually comes from…',
                        'options': ['The computer hardware', 'The training data, which reflects human prejudices', 'Too few pixels', 'The user\'s keyboard'],
                        'answer': 1,
                        'explain': 'Models learn the patterns in their data; if that data is biased, the model faithfully reproduces and amplifies the bias.',
                    },
                    {
                        'q': 'When a self-driving car crashes, the hardest question is…',
                        'options': ['The repair cost', 'Who is accountable — programmer, company, or user?', 'The colour of the car', 'Whether it used electricity'],
                        'answer': 1,
                        'explain': 'Accountability for AI decisions is an open ethical and legal problem with no neat answer yet.',
                    },
                    {
                        'q': 'A healthy way to think about modern AI is as…',
                        'options': ['A perfect oracle', 'A tool that augments humans, used critically', 'A replacement for all thinking', 'Always dangerous'],
                        'answer': 1,
                        'explain': 'Human-plus-AI generally beats either alone — provided we check AI outputs and keep humans responsible for high-stakes decisions.',
                    },
                ],
            },
        ],
    },
]
