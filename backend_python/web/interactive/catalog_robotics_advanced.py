COURSES = [
    {
        'slug': 'robotics-engineer',
        'title': 'Robotics Engineer Lab',
        'category': 'robotics',
        'age_range': '16-19',
        'level': 'Advanced',
        'icon': 'precision_manufacturing',
        'color': '#075985',
        'tagline': 'IK solvers, PID loops, state machines and a Mars rover — the real engineering toolkit.',
        'description': 'This is the deep end. You will solve inverse kinematics analytically, tune a live PID controller, design autonomous behavior with finite state machines, and finally drive a six-wheel rover across procedurally generated Martian terrain. These are the exact tools professional robotics engineers use daily.',
        'skills': ['Inverse kinematics', 'PID control theory', 'Finite state machines', 'Terrain navigation', 'Control tuning', 'Systems thinking'],
        'lessons': [
            {
                'slug': 'inverse-kinematics',
                'title': 'Inverse Kinematics',
                'icon': 'open_with',
                'minutes': 18,
                'sim': 'robotics/inverse-kinematics',
                'sim_type': '3d',
                'summary': 'Drag a target and watch a 2-link arm solve its own joint angles analytically — including the moment it fails.',
                'objectives': [
                    'Contrast forward kinematics with inverse kinematics',
                    'Derive how the law of cosines yields the elbow angle',
                    'Switch between elbow-up and elbow-down solutions',
                    'Identify the reachable workspace and what happens outside it',
                ],
                'knowledge': [
                    {
                        'heading': 'The inverse problem',
                        'body': 'Forward kinematics is easy: given joint angles, compute where the hand ends up. Inverse kinematics (IK) flips the question — given where I WANT the hand, what angles must the joints take? This is the question that matters in practice, because tasks are defined by targets, not by angles.\n\nIK is harder because it can have two solutions, one solution, or none at all, depending on where the target sits.',
                    },
                    {
                        'heading': 'Solving with the law of cosines',
                        'body': 'For a 2-link arm with lengths L1 and L2 reaching distance d, the triangle formed by the two links and the target line is fully determined. The law of cosines gives the elbow: cos(theta2) = (d² - L1² - L2²) / (2·L1·L2).\n\nThe shoulder angle then combines the direct angle to the target with a correction term, atan2(L2·sin(theta2), L1 + L2·cos(theta2)). Two formulas, evaluated instantly — that is an analytic solution, with no trial-and-error needed.',
                    },
                    {
                        'heading': 'Elbow-up or elbow-down?',
                        'body': 'Notice that cos(theta2) accepts both a positive and a negative elbow angle — the arm can reach the same point with its elbow above the line or below it. These are the elbow-up and elbow-down configurations, and the toggle in the simulation switches between them.\n\nReal arms choose based on context: avoiding a table, dodging their own base, or staying within joint limits. Industrial 6-axis arms can have up to eight distinct IK solutions for one pose!',
                    },
                    {
                        'heading': 'The reachable workspace',
                        'body': 'An arm cannot reach everywhere. Targets farther than L1 + L2 are out of range — the arm stretches flat toward them and the target marker turns red in the simulation. Targets closer than |L1 - L2| are also unreachable, hidden inside a dead zone near the base.\n\nThe donut-shaped region between these limits is called the workspace. Engineers always check the workspace before installing an arm; a welding robot that cannot reach the weld is expensive furniture.',
                    },
                ],
                'fun_fact': 'Animators use the same IK math as roboticists — every video game character planting its feet on uneven stairs is running an inverse kinematics solver per foot, per frame!',
                'quiz': [
                    {
                        'q': 'Inverse kinematics answers which question?',
                        'options': ['Where is the hand, given the angles?', 'What angles reach a desired hand position?', 'How heavy is the arm?', 'How fast can joints spin?'],
                        'answer': 1,
                        'explain': 'IK works backwards from a desired end-effector position to the joint angles that achieve it.',
                    },
                    {
                        'q': 'Which theorem solves the elbow angle of a 2-link arm analytically?',
                        'options': ['Pythagoras only', 'The law of cosines', 'Newton\'s third law', 'Ohm\'s law'],
                        'answer': 1,
                        'explain': 'The two links and the target distance form a triangle, and the law of cosines extracts the elbow angle from it.',
                    },
                    {
                        'q': 'Why are there usually two IK solutions for one target?',
                        'options': ['Sensor noise', 'The elbow can bend up or down to reach the same point', 'Two motors per joint', 'Rounding errors'],
                        'answer': 1,
                        'explain': 'Elbow-up and elbow-down configurations mirror each other yet place the hand at the identical target.',
                    },
                    {
                        'q': 'A target beyond L1 + L2 is…',
                        'options': ['Reachable with effort', 'Reachable elbow-down only', 'Outside the workspace, unreachable', 'Closer than it looks'],
                        'answer': 2,
                        'explain': 'The fully stretched arm spans at most L1 + L2; anything farther lies outside the reachable workspace.',
                    },
                ],
            },
            {
                'slug': 'pid-controller',
                'title': 'The PID Controller',
                'icon': 'timeline',
                'minutes': 20,
                'sim': 'robotics/pid-controller',
                'sim_type': '2d',
                'summary': 'Tune Kp, Ki and Kd live on a cart that must hold position, and watch overshoot, oscillation and damping on a scrolling graph.',
                'objectives': [
                    'Explain what the P, I and D terms each contribute',
                    'Reproduce overshoot and oscillation by over-tuning Kp',
                    'Use Kd to damp oscillations and Ki to remove steady-state error',
                    'Tune the controller to recover quickly from a disturbance',
                ],
                'knowledge': [
                    {
                        'heading': 'Proportional: push harder when farther',
                        'body': 'The P term outputs a force proportional to the error: output = Kp × error. Far from the target, it pushes hard; close to it, gently. It is intuitive and forms the backbone of nearly every controller.\n\nBut P alone has two flaws you can reproduce in the sim: crank Kp high and the cart overshoots and oscillates like a pendulum; keep Kp low against a constant disturbance and the cart settles slightly off-target, never quite arriving.',
                    },
                    {
                        'heading': 'Derivative: the brake pedal',
                        'body': 'The D term watches how fast the error is changing and pushes against that motion: it is a brake. Approaching the target quickly? D pushes back early, so the cart glides in instead of slamming past.\n\nAdding Kd to an oscillating P controller visibly calms it — engineers call this damping. Too much Kd, though, makes the system sluggish and twitchy against sensor noise, since the derivative amplifies rapid little changes.',
                    },
                    {
                        'heading': 'Integral: the grudge holder',
                        'body': 'The I term accumulates error over time. If the cart sits even slightly off-target for a while, the integral grows and grows until the push is strong enough to close that last stubborn gap. This eliminates steady-state error.\n\nThe risk is integral windup: during a long disturbance the accumulated sum becomes huge, then overshoots wildly once released. Real implementations clamp the integral — the simulation does too.',
                    },
                    {
                        'heading': 'PID runs the world',
                        'body': 'PID control, invented for ship steering over a century ago, now lives in drones (three nested PID loops per axis), 3D printer hotends, car cruise control, water treatment plants and the temperature controller in an electric rice cooker.\n\nTuning is a craft: a common recipe is to raise Kp until oscillation appears, add Kd to damp it, then add just enough Ki to erase the residual offset. Try exactly this sequence with the presets in the simulation.',
                    },
                ],
                'fun_fact': 'A racing drone executes its full PID control loop up to 8,000 times per second — over a hundred times faster than your eye can refresh!',
                'quiz': [
                    {
                        'q': 'The proportional term reacts to…',
                        'options': ['How long the error existed', 'The current size of the error', 'How fast the error changes', 'Battery level'],
                        'answer': 1,
                        'explain': 'P output equals Kp times the present error — bigger error, harder push, right now.',
                    },
                    {
                        'q': 'Which symptom indicates Kp is too high?',
                        'options': ['Sustained overshoot and oscillation', 'The cart never moves', 'The graph flatlines', 'Quiet, fast settling'],
                        'answer': 0,
                        'explain': 'Excessive proportional gain keeps overcorrecting, swinging the cart back and forth past the target.',
                    },
                    {
                        'q': 'Which term eliminates steady-state error from a constant disturbance?',
                        'options': ['Proportional', 'Derivative', 'Integral', 'None of them'],
                        'answer': 2,
                        'explain': 'The integral accumulates persistent error over time until the output fully cancels the disturbance.',
                    },
                    {
                        'q': 'The derivative term acts most like…',
                        'options': ['An accelerator', 'A brake that damps fast motion', 'A battery', 'A timer'],
                        'answer': 1,
                        'explain': 'D opposes the rate of change of error, slowing approaches and damping oscillation like a brake.',
                    },
                ],
            },
            {
                'slug': 'logic-and-state-machines',
                'title': 'Logic & State Machines',
                'icon': 'account_tree',
                'minutes': 18,
                'sim': 'robotics/state-machine',
                'sim_type': '2d',
                'summary': 'Watch a robot vacuum run a finite state machine — SEARCH, BACKUP, TURN, DOCK — and see why states beat spaghetti code.',
                'objectives': [
                    'Define states, transitions and events in an FSM',
                    'Trace the vacuum\'s behavior through the live state diagram',
                    'Predict what the battery-low event does in every state',
                    'Argue why FSMs are easier to debug than tangled if-else code',
                ],
                'knowledge': [
                    {
                        'heading': 'What is a finite state machine?',
                        'body': 'A finite state machine (FSM) organizes behavior into a fixed set of states — distinct modes like SEARCH or DOCK — with the rule that the robot is in exactly one state at any moment. Arrows called transitions connect states and fire when specific events occur: a bump, a timer expiring, a battery threshold.\n\nThe state diagram in the simulation is the entire program, drawn as a picture. The glowing node tells you precisely what the robot is doing and why.',
                    },
                    {
                        'heading': 'The vacuum\'s brain, four states',
                        'body': 'SEARCH drives forward sweeping the floor. Hitting a wall fires the bump event, transitioning to BACKUP, which reverses for a fixed time, then hands off to TURN, which rotates a random angle before returning to SEARCH. This three-state cycle alone covers a whole room surprisingly well.\n\nThe fourth state, DOCK, is special: when battery drops below the threshold, every state yields to DOCK, and the robot steers toward its charger instead of cleaning.',
                    },
                    {
                        'heading': 'Why not just use if-else?',
                        'body': 'You could write this as nested if-else statements, but as behaviors grow, the conditions tangle: was I already backing up? For how long? Did the bump happen while turning? Programmers call this spaghetti code, and it breeds bugs that only appear in rare sequences.\n\nAn FSM untangles it: each state owns its simple logic, transitions are explicit and listable, and you can test every state in isolation. Adding a new behavior means adding a node, not rewriting the whole tangle.',
                    },
                    {
                        'heading': 'FSMs across engineering',
                        'body': 'Traffic lights, ATM menus, elevator logic, video game enemy AI, network protocols and spacecraft fault handling all run on state machines. NASA reviews mission FSM diagrams line by line, because a missing transition in space can end a mission.\n\nModern robotics layers FSMs into hierarchies and behavior trees, but the principle endures: make every mode explicit, make every transition deliberate, and the machine\'s behavior becomes something you can reason about, prove and trust.',
                    },
                ],
                'fun_fact': 'The Curiosity Mars rover\'s fault-protection software is a giant state machine — when anything goes wrong, it transitions to a "safe mode" state and waits for instructions from Earth!',
                'quiz': [
                    {
                        'q': 'In an FSM, how many states is the machine in at once?',
                        'options': ['All of them', 'Exactly one', 'At most two', 'Zero between transitions'],
                        'answer': 1,
                        'explain': 'The defining property of an FSM: exactly one active state at any moment.',
                    },
                    {
                        'q': 'What causes a transition between states?',
                        'options': ['Random chance only', 'An event such as a bump or low battery', 'Painting the diagram', 'Nothing — states never change'],
                        'answer': 1,
                        'explain': 'Transitions fire when their triggering event occurs, moving the machine to the next state.',
                    },
                    {
                        'q': 'The vacuum is in TURN and battery drops below threshold. What happens?',
                        'options': ['It finishes cleaning first', 'It ignores the battery', 'It transitions to DOCK and seeks the charger', 'It shuts down instantly'],
                        'answer': 2,
                        'explain': 'The low-battery event overrides every cleaning state and sends the robot to DOCK.',
                    },
                    {
                        'q': 'A key advantage of FSMs over tangled if-else code is…',
                        'options': ['They run faster on all CPUs', 'Behavior is explicit, testable state by state', 'They need no sensors', 'They use less battery'],
                        'answer': 1,
                        'explain': 'Each state isolates its own logic and transitions are enumerable, making behavior easy to inspect and debug.',
                    },
                ],
            },
            {
                'slug': 'mars-rover-sandbox',
                'title': 'Mars Rover Sandbox',
                'icon': 'rocket_launch',
                'minutes': 20,
                'sim': 'robotics/rover-sandbox',
                'sim_type': '3d',
                'summary': 'Drive a six-wheel rover across procedural Martian terrain, watch your tilt, dodge rocks — and learn why real rovers must drive themselves.',
                'objectives': [
                    'Drive a rover over uneven terrain using the D-pad or arrow keys',
                    'Monitor tilt and explain why rollover is a mission-ending risk',
                    'Relate wheel-terrain contact to the rocker suspension idea',
                    'Explain why Mars rovers need onboard autonomy due to signal delay',
                ],
                'knowledge': [
                    {
                        'heading': 'Driving on another world',
                        'body': 'Mars is not a parking lot. The ground is a chaos of sand drifts, bedrock slabs and scattered rocks, and a rover must crawl over all of it without a tow truck within 200 million kilometres. That is why real rovers move at a careful walking-pace crawl — Perseverance tops out around 0.15 km/h.\n\nIn the sandbox, feel how slopes tip the rover and rocks block its path. The tilt warning on the HUD is your mission-safety instrument: real rovers obey strict tilt limits, because a rolled-over rover is a dead rover.',
                    },
                    {
                        'heading': 'Six wheels and clever suspension',
                        'body': 'Every NASA Mars rover since Sojourner has used six wheels with a rocker-bogie suspension — a pivoting linkage that lets each wheel rise and fall independently, keeping all six pressed onto uneven ground without any springs.\n\nThis lets rovers climb obstacles taller than a wheel\'s radius while the body tilts only half as much as the terrain does. Watch the simulation\'s rover wheels follow the terrain height as you drive: that ground-hugging contact is what real suspension engineering fights for.',
                    },
                    {
                        'heading': 'The 20-minute problem',
                        'body': 'A radio command from Earth takes between 4 and 24 minutes to reach Mars, depending on where the planets are. Joysticking a rover live is impossible: by the time you saw a cliff on your screen, the rover would have driven over it minutes ago.\n\nSo engineers send a day\'s driving goals each morning, and the rover navigates by itself — building 3D terrain maps from stereo cameras, scoring safe paths, and refusing moves that exceed tilt or obstacle limits. Perseverance\'s auto-navigation can plan while driving, covering hundreds of metres per Martian day unsupervised.',
                    },
                    {
                        'heading': 'Everything you learned, on one robot',
                        'body': 'A Mars rover is this whole course in one machine. Differential steering turns its six wheels. Ultrasonic-style ranging becomes stereo vision and hazard cameras. PID loops hold wheel speeds and arm joints steady. A vast state machine governs driving, science, communication and fault recovery, and inverse kinematics aims the drill on its robotic arm.\n\nEvery one of those subsystems started as a simple lesson like the ones you just completed. Engineering is layers: master the small loops, and you can build machines that explore other planets.',
                    },
                ],
                'fun_fact': 'NASA\'s Opportunity rover was designed for a 90-day mission — it kept driving for almost 15 years and over 45 km, the off-world driving record until today!',
                'quiz': [
                    {
                        'q': 'Why can\'t engineers drive a Mars rover live with a joystick?',
                        'options': ['Rovers have no radios', 'Radio signals take minutes to travel between Earth and Mars', 'Joysticks freeze on Mars', 'NASA forbids fun'],
                        'answer': 1,
                        'explain': 'With 4-24 minutes of one-way signal delay, live control is impossible — the rover must navigate autonomously.',
                    },
                    {
                        'q': 'The rocker-bogie suspension exists to…',
                        'options': ['Make the rover bounce', 'Keep all six wheels in contact with uneven ground', 'Save battery', 'Look impressive'],
                        'answer': 1,
                        'explain': 'Its pivoting linkages let wheels rise and fall independently, maintaining traction over rocks and dips.',
                    },
                    {
                        'q': 'Why does the rover monitor its tilt angle?',
                        'options': ['To take better photos', 'Excessive tilt risks an unrecoverable rollover', 'Tilt charges the battery', 'It does not'],
                        'answer': 1,
                        'explain': 'No one can flip a rover back upright on Mars, so tilt limits are hard safety constraints.',
                    },
                    {
                        'q': 'Which of these does a real Mars rover use?',
                        'options': ['PID control only', 'State machines only', 'Kinematics only', 'All of them, layered together'],
                        'answer': 3,
                        'explain': 'A rover integrates control loops, state machines, kinematics and sensing — every topic in this course combined.',
                    },
                ],
            },
        ],
    },
]
