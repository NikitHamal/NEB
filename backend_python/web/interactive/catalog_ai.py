def _lesson(slug, title, icon, minutes, summary, objectives, knowledge, quiz, fun_fact=None):
    lesson = {
        'slug': slug,
        'title': title,
        'icon': icon,
        'minutes': minutes,
        'sim': 'ai/ai-lab',
        'sim_type': 'lab',
        'summary': summary,
        'objectives': objectives,
        'knowledge': knowledge,
        'quiz': quiz,
    }
    if fun_fact:
        lesson['fun_fact'] = fun_fact
    return lesson


COURSES = [
    {
        'slug': 'ai-from-scratch-to-advanced',
        'title': 'AI From Scratch to Advanced',
        'category': 'ai',
        'age_range': '10+',
        'level': 'Beginner to Advanced',
        'icon': 'neurology',
        'color': '#4F46E5',
        'tagline': 'Rules, data, training, neural networks, vision, language models, transformers, safety and deployment as hands-on simulations.',
        'description': 'This course teaches artificial intelligence from first principles without pretending AI is magic. Learners compare rules with learned models, train classifiers, tune neural-network weights, inspect computer-vision features, tokenize language, step through attention inside a transformer and evaluate bias, privacy and reliability. Every lesson includes a live 2D/3D simulation so the model behavior is visible.',
        'skills': [
            'Separate rule-based programs from learned models',
            'Collect clean training data and detect bias',
            'Train and evaluate classifiers with accuracy, precision and recall',
            'Understand neurons, layers, loss and gradient descent',
            'Explore computer vision, language models and transformers',
            'Design safer AI systems for real users',
        ],
        'lessons': [
            _lesson(
                'what-is-ai',
                'What AI Really Is',
                'psychology',
                12,
                'Compare a hand-written rule system with a learned model and watch where each succeeds or fails.',
                [
                    'Define AI as software that performs perception, prediction or decision-making tasks',
                    'Explain the difference between programmed rules and learned patterns',
                    'Identify why a model can fail outside the data it learned from',
                ],
                [
                    {
                        'heading': 'AI is a system, not magic',
                        'body': 'Artificial intelligence is software that performs tasks we normally associate with human intelligence: recognizing patterns, predicting outcomes, planning actions, understanding language or making recommendations. Some AI is rule-based: humans write explicit if-then instructions. Modern machine learning is different: the computer adjusts a model from examples.\n\nIn the simulation, switch between a rule robot and a learned robot. The rule robot follows exact thresholds. The learned robot draws a boundary from examples. Both can be useful, and both can fail.',
                    },
                    {
                        'heading': 'Learning means fitting a pattern',
                        'body': 'A model is a simplified mathematical representation of the world. It cannot know everything; it only captures patterns present in its training data. If the training examples are narrow, noisy or biased, the model inherits those weaknesses.\n\nThat is why serious AI work starts with careful problem definition, data collection and testing. A model that works in a demo can still fail for a real student, school or language community if those users were absent from the data.',
                    },
                ],
                [
                    {
                        'q': 'What is the main difference between a rule-based AI and a learned model?',
                        'options': ['A rule system follows human-written instructions; a learned model fits patterns from examples', 'A learned model never makes mistakes', 'Rule systems are always more powerful', 'Only learned models run on computers'],
                        'answer': 0,
                        'explain': 'Rule systems use explicit instructions. Machine-learning models adjust parameters from examples and can generalize within the limits of their data.',
                    },
                    {
                        'q': 'Why can an AI fail on a new kind of input?',
                        'options': ['It has emotions', 'The input may be outside the distribution it learned from', 'Computers cannot compare numbers', 'Because all AI is random'],
                        'answer': 1,
                        'explain': 'Models learn patterns from data. If the new case is very different from training examples, the learned pattern may not apply.',
                    },
                ],
                'The word "robot" entered popular culture through a 1920 Czech play about artificial workers.',
            ),
            _lesson(
                'data-is-the-teacher',
                'Data Is the Teacher',
                'dataset',
                14,
                'Build a tiny dataset, add biased examples and watch the decision boundary move in 2D and 3D.',
                [
                    'Explain features, labels and examples',
                    'Show how biased or imbalanced data changes model behavior',
                    'Split data into training and testing examples',
                ],
                [
                    {
                        'heading': 'Examples become the lesson',
                        'body': 'Supervised learning uses examples with inputs and correct answers. The inputs are features: measurable pieces of information such as height, color, exam score, word frequency or pixel brightness. The correct answer is the label. A learning algorithm searches for a rule that maps features to labels.\n\nGood data is not just a large pile of records. It should represent the people and situations where the model will be used. Missing groups, wrong labels and duplicate examples can make a model look accurate while hiding serious errors.',
                    },
                    {
                        'heading': 'Train-test split protects honesty',
                        'body': 'If you test a model on the same examples it trained on, you only learn whether it memorized the answers. A test set uses examples held out from training. Performance on that unseen set gives a more honest estimate of how the model may behave in practice.\n\nThe simulation lets you move data points between classes and change the train-test split. Watch the accuracy change when the test examples no longer match the training pattern.',
                    },
                ],
                [
                    {
                        'q': 'In supervised learning, what is a label?',
                        'options': ['The correct answer attached to an example', 'A random model weight', 'The color of a chart', 'A computer brand'],
                        'answer': 0,
                        'explain': 'The label is the target answer the model tries to learn, such as spam/not spam or disease/no disease.',
                    },
                    {
                        'q': 'Why keep a test set separate?',
                        'options': ['To make training slower', 'To estimate performance on unseen examples', 'To delete bad data automatically', 'To avoid using labels'],
                        'answer': 1,
                        'explain': 'A separate test set helps detect memorization and gives a more realistic performance estimate.',
                    },
                ],
            ),
            _lesson(
                'classification-boundaries',
                'Classification and Decision Boundaries',
                'scatter_plot',
                14,
                'Train a classifier by moving a boundary through points, then inspect true positives, false positives and false negatives.',
                [
                    'Define classification as choosing among discrete classes',
                    'Interpret a decision boundary',
                    'Compute accuracy, precision and recall from outcomes',
                ],
                [
                    {
                        'heading': 'A classifier divides feature space',
                        'body': 'Classification predicts a category: pass/fail, plant/animal, safe/unsafe, spam/not spam. When inputs have two features, you can draw them on a plane. A classifier creates regions in that plane. Points on one side receive one label; points on the other side receive another.\n\nSimple linear classifiers draw a straight boundary. More advanced models can curve the boundary, but the idea is the same: the model partitions the space according to patterns in the data.',
                    },
                    {
                        'heading': 'Accuracy is not enough',
                        'body': 'Accuracy is the fraction of predictions that are correct. But in many real problems, the kind of mistake matters. A false positive says something is true when it is not. A false negative misses something that is true. Precision asks: when the model says yes, how often is it right? Recall asks: of all real yes cases, how many did it find?\n\nA medical screening model with high accuracy but low recall could miss sick patients. A moderation model with low precision could wrongly punish innocent users. Metrics must match the task.',
                    },
                ],
                [
                    {
                        'q': 'What does a decision boundary do?',
                        'options': ['Separates regions assigned to different classes', 'Stores passwords', 'Makes a dataset larger', 'Turns text into sound'],
                        'answer': 0,
                        'explain': 'The boundary divides feature space so points in different regions receive different predicted classes.',
                    },
                    {
                        'q': 'Which metric asks how many real positive cases the model found?',
                        'options': ['Recall', 'File size', 'Frame rate', 'Temperature'],
                        'answer': 0,
                        'explain': 'Recall = true positives divided by all actual positives.',
                    },
                ],
            ),
            _lesson(
                'neural-network-neurons',
                'Neurons, Weights and Layers',
                'hub',
                15,
                'Adjust weights inside a tiny neural network and watch signals flow from inputs to output.',
                [
                    'Describe a neuron as a weighted sum followed by an activation function',
                    'Explain layers, weights and bias terms',
                    'Show how hidden layers combine simple features into useful representations',
                ],
                [
                    {
                        'heading': 'A neuron is a weighted calculator',
                        'body': 'An artificial neuron takes numbers as inputs, multiplies each by a weight, adds a bias and passes the result through an activation function. The activation decides how strongly the neuron fires. A neural network connects many neurons into layers.\n\nWeights are the memory of the network. Training changes those weights until the output becomes closer to the desired answer. Hidden layers are useful because they can build intermediate features that humans did not directly program.',
                    },
                    {
                        'heading': 'Depth builds representation',
                        'body': 'A single neuron can only draw a simple boundary. Multiple layers can combine features: one layer may detect edges in an image, another combines edges into shapes, and a later layer recognizes an object. In language, early layers may track spelling and positions, while later layers model meaning and relationships.\n\nThe 3D view shows depth as stacked layers. Signals brighten as they pass forward, making it easier to see why a network is a computation graph rather than a brain copy.',
                    },
                ],
                [
                    {
                        'q': 'What changes during neural-network training?',
                        'options': ['Weights and biases', 'The laws of physics', 'The user screen size', 'The keyboard layout'],
                        'answer': 0,
                        'explain': 'Training adjusts weights and biases to reduce the difference between predictions and labels.',
                    },
                    {
                        'q': 'Why are hidden layers useful?',
                        'options': ['They can build intermediate features', 'They remove the need for data', 'They make every answer correct', 'They hide code from users'],
                        'answer': 0,
                        'explain': 'Hidden layers transform raw inputs into more useful internal representations.',
                    },
                ],
            ),
            _lesson(
                'gradient-descent-training',
                'Training With Gradient Descent',
                'trending_down',
                16,
                'Walk down a loss landscape and see how learning rate affects convergence, overshooting and local minima.',
                [
                    'Define loss as a measure of prediction error',
                    'Explain gradient descent as stepping downhill in loss',
                    'Tune learning rate to avoid slow training or overshooting',
                ],
                [
                    {
                        'heading': 'Loss gives the model a target',
                        'body': 'A model needs a way to know whether it is improving. The loss function measures prediction error as a number. High loss means predictions are poor. Low loss means they are closer to the labels. Training is the process of changing parameters to reduce loss.\n\nGradient descent uses the slope of the loss landscape. If the slope points upward in one direction, the model steps the other way. Repeating this many times moves the parameters toward a lower-loss region.',
                    },
                    {
                        'heading': 'Learning rate controls step size',
                        'body': 'A tiny learning rate is safe but painfully slow. A huge learning rate can jump over the best region and even make training unstable. Real AI systems often use schedules: larger steps early, smaller steps later.\n\nThe simulation lets you drag the learning rate. Watch the dot crawl, settle or overshoot. This is a simplified view, but the same idea trains models with millions or billions of parameters.',
                    },
                ],
                [
                    {
                        'q': 'What does a loss function measure?',
                        'options': ['How wrong the model is', 'How bright the screen is', 'How old the dataset is', 'How many users are online'],
                        'answer': 0,
                        'explain': 'Loss turns prediction error into a number the optimizer can reduce.',
                    },
                    {
                        'q': 'What can happen if the learning rate is too high?',
                        'options': ['The optimizer can overshoot and become unstable', 'The data becomes perfectly balanced', 'The model stops needing labels', 'The code changes language'],
                        'answer': 0,
                        'explain': 'Large steps can jump past the low-loss region instead of settling into it.',
                    },
                ],
            ),
            _lesson(
                'computer-vision-features',
                'Computer Vision: Pixels to Meaning',
                'visibility',
                15,
                'Turn pixels into edges, shapes and object scores using a simplified convolution-style pipeline.',
                [
                    'Describe images as grids of pixel values',
                    'Explain how filters detect local features such as edges',
                    'Connect early visual features to object recognition',
                ],
                [
                    {
                        'heading': 'Images are numbers',
                        'body': 'A digital image is a grid of pixels. Each pixel stores brightness or color values. A computer-vision model does not see a cat or a leaf directly; it receives arrays of numbers. The first task is to extract useful patterns from those numbers.\n\nSmall filters scan across an image to detect features such as vertical edges, horizontal edges, corners and color changes. Convolutional neural networks learn many such filters automatically from training data.',
                    },
                    {
                        'heading': 'Features combine into objects',
                        'body': 'Early layers may detect edges. Middle layers combine edges into textures and parts. Later layers combine parts into objects. This hierarchy is why vision models can recognize complicated scenes, but also why they can be fooled by unusual lighting, angles or patterns.\n\nThe simulation shows a pixel grid, an edge map and a 3D feature stack so learners can see the transformation from raw values to meaning.',
                    },
                ],
                [
                    {
                        'q': 'What is a digital image to a model?',
                        'options': ['A grid of numeric pixel values', 'A sentence', 'A microphone signal only', 'A database password'],
                        'answer': 0,
                        'explain': 'Vision models process arrays of pixel values, then transform them into learned features.',
                    },
                    {
                        'q': 'What does an edge filter detect?',
                        'options': ['Sudden changes in brightness or color', 'Usernames', 'Battery level', 'Random labels'],
                        'answer': 0,
                        'explain': 'Edges are locations where pixel values change sharply.',
                    },
                ],
            ),
            _lesson(
                'language-tokenization',
                'Language AI: Tokens and Embeddings',
                'translate',
                15,
                'Break text into tokens, map tokens into vectors and compare semantic closeness in a 2D/3D embedding space.',
                [
                    'Explain tokenization as splitting text into model-readable pieces',
                    'Describe embeddings as vectors that capture relationships',
                    'Inspect why language support depends heavily on training data',
                ],
                [
                    {
                        'heading': 'Models read tokens, not raw thoughts',
                        'body': 'Language models convert text into tokens: pieces such as words, subwords, punctuation or characters. Each token becomes an ID, then an embedding vector. The vector is a list of numbers that lets the model compare and combine meanings.\n\nTokenization matters for Nepali and other languages. If a tokenizer handles a language poorly, common words may split into many pieces, making the model slower and often less capable for that language.',
                    },
                    {
                        'heading': 'Embeddings place related ideas nearby',
                        'body': 'Embeddings are learned from context. Words or phrases used in similar situations often land near each other in vector space. This lets models connect "teacher" with "school", "photosynthesis" with "plant" and "Kathmandu" with "Nepal".\n\nThe simulation projects vectors into 2D or 3D. Real embeddings have hundreds or thousands of dimensions, but the visual idea is the same: distance and direction carry information.',
                    },
                ],
                [
                    {
                        'q': 'What is tokenization?',
                        'options': ['Splitting text into model-readable pieces', 'Drawing a graph on paper', 'Measuring battery voltage', 'Deleting all punctuation forever'],
                        'answer': 0,
                        'explain': 'Tokenization converts text into pieces that can be mapped to IDs and vectors.',
                    },
                    {
                        'q': 'What is an embedding?',
                        'options': ['A numeric vector representing a token or item', 'A type of exam paper', 'A web browser tab', 'A hardware cable'],
                        'answer': 0,
                        'explain': 'Embeddings are vectors learned so related items have useful geometric relationships.',
                    },
                ],
            ),
            _lesson(
                'attention-transformers',
                'Attention and Transformers',
                'graph_5',
                18,
                'Step through self-attention: queries, keys, values, attention weights and layered transformer blocks.',
                [
                    'Explain self-attention as weighted information lookup among tokens',
                    'Identify query, key and value roles',
                    'Describe why transformers can model long-range relationships',
                ],
                [
                    {
                        'heading': 'Attention chooses what to use',
                        'body': 'Self-attention lets each token look at other tokens and decide how much information to take from each one. A query represents what the current token is looking for. Keys represent what other tokens offer. Values carry the information that gets mixed. The query-key match produces attention weights.\n\nThis is why a transformer can connect a pronoun to a noun many words earlier, or relate a question to the exact part of a passage that answers it.',
                    },
                    {
                        'heading': 'Transformers stack attention and feed-forward layers',
                        'body': 'A transformer block usually contains self-attention, a feed-forward network, residual connections and normalization. Stacking many blocks lets the model refine meaning repeatedly. Large language models are built from this repeated pattern at enormous scale.\n\nThe 3D view shows tokens as columns and attention as weighted bridges. Bright bridges mean stronger information flow.',
                    },
                ],
                [
                    {
                        'q': 'In self-attention, what do attention weights represent?',
                        'options': ['How strongly one token uses information from another', 'The age of the dataset', 'The screen brightness', 'The number of files downloaded'],
                        'answer': 0,
                        'explain': 'Attention weights control how much value information flows from each token to the current token.',
                    },
                    {
                        'q': 'Why are transformers powerful for language?',
                        'options': ['They can model relationships among tokens across a sequence', 'They never need training', 'They only work with numbers below ten', 'They erase all context'],
                        'answer': 0,
                        'explain': 'Self-attention lets tokens exchange information across the sequence, making long-range relationships easier to learn.',
                    },
                ],
            ),
            _lesson(
                'generative-ai-limits',
                'Generative AI and Hallucinations',
                'auto_awesome',
                16,
                'Sample next-token probabilities, change temperature and see why confident text can still be false.',
                [
                    'Explain generation as repeated next-token prediction',
                    'Show how temperature changes randomness',
                    'Define hallucination as plausible but unsupported output',
                ],
                [
                    {
                        'heading': 'Generation predicts one step at a time',
                        'body': 'A language model generates text by predicting a probability distribution for the next token, choosing one token, appending it and repeating. The result can feel like reasoning because the model has learned patterns from enormous text corpora, but the mechanism is still statistical prediction guided by context.\n\nTemperature controls randomness. Low temperature chooses safer high-probability tokens. High temperature explores more surprising tokens, which can be creative but also unstable.',
                    },
                    {
                        'heading': 'Fluent does not mean true',
                        'body': 'A hallucination is output that sounds plausible but is not supported by reliable evidence. Language models can hallucinate because they optimize likely text, not direct truth. Retrieval, citations, tool use, verification and domain-specific tests reduce risk but do not remove it completely.\n\nThe simulation shows how a token path can produce fluent sentences even when a fact node is missing. This is why serious educational tools must separate explanation from verified source material.',
                    },
                ],
                [
                    {
                        'q': 'What does temperature control in text generation?',
                        'options': ['How random token selection is', 'The phone battery temperature', 'The number of model layers', 'The font size'],
                        'answer': 0,
                        'explain': 'Higher temperature samples more broadly from the probability distribution; lower temperature is more conservative.',
                    },
                    {
                        'q': 'What is an AI hallucination?',
                        'options': ['A plausible but unsupported or false output', 'A required database index', 'A screen animation', 'A perfect answer'],
                        'answer': 0,
                        'explain': 'Hallucinations can be fluent and confident while still wrong or unsupported.',
                    },
                ],
            ),
            _lesson(
                'ai-safety-deployment',
                'Responsible AI Deployment',
                'verified_user',
                18,
                'Run an AI release checklist: privacy, bias, evaluation, human oversight, monitoring and rollback.',
                [
                    'Identify common AI risks: bias, privacy leakage, over-trust and misuse',
                    'Design evaluation tests before deployment',
                    'Explain why monitoring and human escalation are necessary',
                ],
                [
                    {
                        'heading': 'Responsible AI is engineering discipline',
                        'body': 'A model is only one part of an AI product. Real deployment needs data governance, consent, security, evaluation, accessibility, user feedback, abuse prevention, human review and monitoring. The higher the stakes, the stronger the safeguards must be.\n\nEducational AI should be especially careful. Students may trust confident explanations, so systems should show uncertainty, cite source material where possible and encourage verification rather than replacing learning.',
                    },
                    {
                        'heading': 'Measure before and after release',
                        'body': 'Before release, teams test accuracy across groups, edge cases and languages. After release, they monitor failures, latency, user reports and distribution shift. If the real world changes, a model can become stale. A rollback plan matters as much as the launch plan.\n\nThe simulation turns deployment into a systems board. Move risk sliders and watch the readiness score respond. The goal is not zero risk; it is explicit, managed risk with accountable humans.',
                    },
                ],
                [
                    {
                        'q': 'Which item belongs in a responsible AI release checklist?',
                        'options': ['Bias testing and monitoring', 'Only a logo color', 'Ignoring user feedback', 'Removing all human oversight'],
                        'answer': 0,
                        'explain': 'Bias testing, monitoring, privacy controls and escalation paths are core deployment safeguards.',
                    },
                    {
                        'q': 'Why monitor an AI system after launch?',
                        'options': ['Real-world data and user behavior can change', 'Monitoring makes models magical', 'It replaces all tests', 'It prevents every possible error'],
                        'answer': 0,
                        'explain': 'Distribution shift, new abuse patterns and hidden failures often appear only after deployment.',
                    },
                ],
            ),
        ],
    }
]
