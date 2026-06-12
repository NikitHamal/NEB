from .catalog_robotics_advanced import COURSES as _ADVANCED_COURSES

COURSES = [
    {
        'slug': 'robotics-explorer',
        'title': 'Robotics Explorer',
        'category': 'robotics',
        'age_range': '8-11',
        'level': 'Beginner',
        'icon': 'smart_toy',
        'color': '#0EA5E9',
        'tagline': 'Meet your first robot and discover what makes it tick!',
        'description': 'Say hello to Robo, your friendly 3D robot buddy! In this course you will poke, spin and play with every part of a robot — its brain, its muscles, its senses and its energy. By the end, you will know exactly how robots see the world and move around in it.',
        'skills': ['Robot body parts', 'Batteries & circuits', 'Gears & motion', 'Sensors & echoes', 'How robots think'],
        'lessons': [
            {
                'slug': 'meet-the-robot',
                'title': 'Meet the Robot',
                'icon': 'smart_toy',
                'minutes': 12,
                'sim': 'robotics/robot-anatomy',
                'sim_type': '3d',
                'summary': 'Tap every part of a friendly 3D robot to discover what its brain, sensors, motors and battery actually do.',
                'objectives': [
                    'Name the five main parts every robot has',
                    'Match each robot part to a part of your own body',
                    'Explain what a controller (the robot brain) does',
                    'Spot sensors, motors and the battery on a real robot picture',
                ],
                'knowledge': [
                    {
                        'heading': 'Robots are built like you!',
                        'body': 'A robot might look like a machine, but it is built a lot like you. You have eyes and ears to sense the world — a robot has sensors. You have a brain to think — a robot has a tiny computer called a controller. You have muscles to move — a robot has motors.\n\nAnd just like you need dal bhat for energy, a robot needs a battery! When you tap each part in the simulation, think about which part of your body it matches.',
                    },
                    {
                        'heading': 'The brain: the controller',
                        'body': 'Deep inside the robot sits a small computer chip called a controller. It reads messages from the sensors, decides what to do, and tells the motors how to move. It does this thinking hundreds of times every second — much faster than you can blink!\n\nThe controller only does what its program says. A robot is not magic: somewhere, a person wrote instructions for it, step by step, just like a recipe.',
                    },
                    {
                        'heading': 'Muscles and bones: motors and chassis',
                        'body': 'Motors are the robot\'s muscles. They spin wheels, lift arms and turn heads. Without motors, a robot would just sit still like a statue.\n\nThe chassis is the robot\'s skeleton — the strong frame that holds everything together. It can be made of metal or plastic. In Nepal, students in robotics clubs often build their first chassis from simple acrylic sheets or even recycled materials, and they work great!',
                    },
                    {
                        'heading': 'Food for robots: the battery',
                        'body': 'Nothing in a robot works without energy. The battery is the robot\'s lunchbox — it stores electrical energy and shares it with the brain, the sensors and the motors.\n\nWhen the battery runs low, the robot gets slow and sleepy, just like you before dinner. Some robots, like robot vacuums, are clever enough to drive themselves back to a charger when they feel hungry!',
                    },
                ],
                'fun_fact': 'The word "robot" comes from the Czech word "robota", which means hard work — it was first used in a play in 1920, more than 100 years ago!',
                'quiz': [
                    {
                        'q': 'Which part is the robot\'s brain?',
                        'options': ['The motor', 'The controller', 'The battery', 'The wheel'],
                        'answer': 1,
                        'explain': 'The controller is a small computer that reads sensors, makes decisions and commands the motors — just like your brain.',
                    },
                    {
                        'q': 'What do sensors do for a robot?',
                        'options': ['They make it move', 'They store energy', 'They help it sense the world, like eyes and ears', 'They hold it together'],
                        'answer': 2,
                        'explain': 'Sensors are how a robot notices light, distance, sound and touch — its version of eyes, ears and skin.',
                    },
                    {
                        'q': 'A robot\'s motors are most like your…',
                        'options': ['Muscles', 'Stomach', 'Hair', 'Teeth'],
                        'answer': 0,
                        'explain': 'Motors create movement, exactly like your muscles move your arms and legs.',
                    },
                    {
                        'q': 'What happens if the battery is empty?',
                        'options': ['The robot moves faster', 'Nothing changes', 'The robot cannot work at all', 'The robot grows a new one'],
                        'answer': 2,
                        'explain': 'Every part of a robot needs electrical energy, so with an empty battery the whole robot stops.',
                    },
                ],
            },
            {
                'slug': 'robot-power',
                'title': 'Robot Power!',
                'icon': 'bolt',
                'minutes': 12,
                'sim': 'robotics/robot-power',
                'sim_type': 'lab',
                'summary': 'Build a simple circuit with a battery, a switch and a motor — then watch electricity flow and make a fan spin.',
                'objectives': [
                    'Explain why a circuit must be a complete loop',
                    'Use a switch to turn a motor on and off',
                    'Predict what happens to motor speed when voltage goes up',
                    'Trace the path electricity takes from battery to motor and back',
                ],
                'knowledge': [
                    {
                        'heading': 'Electricity loves a loop',
                        'body': 'Electricity is a stream of tiny particles that flows from a battery, through wires, into a motor, and back to the battery. This round trip is called a circuit, which means "circle".\n\nIf the circle is broken anywhere — a loose wire, an open switch — the flow stops instantly and the motor goes quiet. In the simulation, flip the switch and watch the glowing dots: they only flow when the loop is complete!',
                    },
                    {
                        'heading': 'The switch: a drawbridge for electricity',
                        'body': 'A switch is just a tiny gap in the circuit that you can open and close. Open the switch and the bridge is up — no electricity can cross. Close it and the bridge comes down — the current zooms around the loop.\n\nEvery light switch in your home works exactly the same way. When you switch on a light in your room, you are closing a circuit, just like in this lab.',
                    },
                    {
                        'heading': 'Voltage: the push behind the flow',
                        'body': 'Voltage measures how hard the battery pushes electricity around the loop. A small 1.5V battery, like one from a TV remote, gives a gentle push. A 9V battery pushes much harder, so the motor spins much faster.\n\nTry sliding the voltage up and down in the lab. More push means more current, and more current means more speed. But real engineers are careful — too much voltage can overheat a small motor!',
                    },
                    {
                        'heading': 'Why robots care about power',
                        'body': 'Everything a robot does — thinking, sensing, moving — costs energy. Robot designers must choose batteries carefully: big batteries last longer but are heavy, small ones are light but run out fast.\n\nIn places where electricity comes and goes, like during load-shedding hours that Nepal used to have, hobby builders learned to be extra clever with rechargeable batteries and even solar panels. Saving power is a robotics superpower!',
                    },
                ],
                'fun_fact': 'An electric eel can produce around 600 volts — that is enough push to run about 400 small robot motors at once!',
                'quiz': [
                    {
                        'q': 'What does a circuit need so electricity can flow?',
                        'options': ['A complete, unbroken loop', 'A very long wire', 'Two batteries', 'A loud motor'],
                        'answer': 0,
                        'explain': 'Current only flows when there is a closed loop from the battery, through the parts, and back to the battery.',
                    },
                    {
                        'q': 'What happens when you open the switch?',
                        'options': ['The motor spins faster', 'The flow stops and the motor stops', 'The battery charges up', 'The wires get longer'],
                        'answer': 1,
                        'explain': 'An open switch breaks the loop, so the current cannot complete its round trip and the motor stops.',
                    },
                    {
                        'q': 'If you raise the voltage from 1.5V to 9V, the motor will…',
                        'options': ['Spin slower', 'Stay the same', 'Spin faster', 'Turn backwards'],
                        'answer': 2,
                        'explain': 'Higher voltage pushes more current through the motor, making it spin faster.',
                    },
                ],
            },
            {
                'slug': 'gears-in-motion',
                'title': 'Gears in Motion',
                'icon': 'settings',
                'minutes': 14,
                'sim': 'robotics/gears-motion',
                'sim_type': '3d',
                'summary': 'Spin meshing 3D gears, swap gear sizes and discover how robots trade speed for strength.',
                'objectives': [
                    'Show that meshing gears spin in opposite directions',
                    'Read a gear ratio like 2:1 and say what it means',
                    'Explain the trade between speed and turning strength',
                    'Find gears hiding in everyday machines around you',
                ],
                'knowledge': [
                    {
                        'heading': 'Teeth that push teeth',
                        'body': 'A gear is a wheel with teeth around its edge. When two gears mesh, the teeth of one push the teeth of the other, so spinning the first gear makes the second one spin too.\n\nHere is the surprise: the second gear always spins the opposite way! Watch the arrows in the simulation — if the driver turns clockwise, its partner turns counter-clockwise. Add a third gear and the direction flips back again.',
                    },
                    {
                        'heading': 'Gear ratio: the magic number',
                        'body': 'Count the teeth! If a small gear with 12 teeth drives a big gear with 24 teeth, the big gear has twice the teeth, so it turns only half as fast. We write this as a 2:1 ratio.\n\nIn the sim, switch between 1:1, 2:1 and 3:1 and watch the RPM readouts. RPM means "rotations per minute" — how many full spins a gear makes in one minute.',
                    },
                    {
                        'heading': 'Speed or strength: pick one',
                        'body': 'Gears cannot give you extra speed AND extra strength at the same time — it is always a trade. A big slow gear turns with more twisting force, called torque. A small fast gear spins quickly but with less force.\n\nA cyclist climbing the steep hill to Nagarkot shifts to a low gear: the wheels turn slower, but with enough strength to climb. On the flat road back, a high gear trades that strength for speed.',
                    },
                    {
                        'heading': 'Gears are everywhere',
                        'body': 'Open up almost any machine and you will find gears: bicycles, clocks, egg beaters, washing machines and the small servo motors used in school robotics kits.\n\nRobot designers add gearboxes to motors because most motors naturally spin very fast but very weakly. A gearbox slows the spin down and multiplies the strength, so a small motor can lift a heavy robotic arm. No gearbox, no lifting!',
                    },
                ],
                'fun_fact': 'The ancient Greeks built a geared machine called the Antikythera mechanism more than 2,000 years ago — it used over 30 bronze gears to predict eclipses!',
                'quiz': [
                    {
                        'q': 'Two meshing gears always…',
                        'options': ['Spin the same direction', 'Spin in opposite directions', 'Spin at the same speed', 'Stop each other'],
                        'answer': 1,
                        'explain': 'Each tooth pushes its partner the opposite way, so meshing gears always counter-rotate.',
                    },
                    {
                        'q': 'A 3:1 gear ratio means the output gear turns…',
                        'options': ['3 times faster', '3 times slower', 'Backwards only', 'At random speeds'],
                        'answer': 1,
                        'explain': 'With 3:1, the driver must spin three full turns to rotate the big output gear once — slower but stronger.',
                    },
                    {
                        'q': 'When a gear slows down the rotation, what does it give you in return?',
                        'options': ['More torque (turning strength)', 'More electricity', 'Less weight', 'Nothing at all'],
                        'answer': 0,
                        'explain': 'Slowing rotation through gears multiplies torque — that is the speed-for-strength trade.',
                    },
                    {
                        'q': 'Why do robot arms use gearboxes on their motors?',
                        'options': ['To look cool', 'To make motors quieter', 'To trade fast weak spinning for slow strong turning', 'To save battery only'],
                        'answer': 2,
                        'explain': 'Motors spin fast but weakly; a gearbox converts that into the slow, strong motion an arm needs to lift things.',
                    },
                ],
            },
            {
                'slug': 'robot-senses',
                'title': 'Robot Senses',
                'icon': 'sensors',
                'minutes': 14,
                'sim': 'robotics/robot-senses',
                'sim_type': '3d',
                'summary': 'Fire ultrasonic pings at a wall, move it closer and farther, and see how robots measure distance with sound.',
                'objectives': [
                    'Describe how an ultrasonic sensor sends and hears a ping',
                    'Connect echo time to distance: longer echo means farther wall',
                    'Estimate distance from the echo-time readout',
                    'Name animals that use echoes the same way',
                ],
                'knowledge': [
                    {
                        'heading': 'Seeing with sound',
                        'body': 'An ultrasonic sensor is a robot\'s way of seeing with sound. It shouts a tiny "ping" — a sound too high for human ears — and then listens for the echo bouncing back off a wall or object.\n\nIn the simulation, watch the ring fly out, hit the wall and travel back. The robot times this whole round trip very precisely, down to millionths of a second.',
                    },
                    {
                        'heading': 'Echo time tells distance',
                        'body': 'Sound travels through air at about 343 metres every second. If the echo comes back quickly, the wall must be close. If it takes longer, the wall is far away.\n\nThe robot\'s controller does the math: distance equals speed of sound times echo time, divided by two. Why divide by two? Because the sound made a round trip — there and back — but we only want the one-way distance!',
                    },
                    {
                        'heading': 'Nature invented it first',
                        'body': 'Bats fly in total darkness and never crash, because they have used echo-location for millions of years. They squeak, listen and build a sound-picture of caves and forests. Dolphins do the same underwater.\n\nEngineers copied this trick for robots, submarines and even cars — parking sensors that beep faster as you reverse closer to a wall are ultrasonic sensors, exactly like the one in this lesson.',
                    },
                    {
                        'heading': 'Why robots need distance sensors',
                        'body': 'A robot without senses is like walking through your house blindfolded — sooner or later, bump! Distance sensors let robots stop before hitting walls, follow people at a safe distance, or map a whole room.\n\nMost student robots in Nepali school competitions use the little blue HC-SR04 ultrasonic sensor. It costs only a few hundred rupees but can measure from 2 cm to 4 metres — the exact sensor this simulation copies.',
                    },
                ],
                'fun_fact': 'A bat can hear an echo from a tiny mosquito and snatch it from the air mid-flight — its sonar is sharper than most robot sensors ever built!',
                'quiz': [
                    {
                        'q': 'How does an ultrasonic sensor measure distance?',
                        'options': ['It takes a photo', 'It times how long an echo takes to return', 'It stretches a measuring tape', 'It feels the wall with a finger'],
                        'answer': 1,
                        'explain': 'The sensor sends a ping and times the echo; longer round-trip time means the object is farther away.',
                    },
                    {
                        'q': 'If the wall moves farther away, the echo time…',
                        'options': ['Gets shorter', 'Stays the same', 'Gets longer', 'Disappears'],
                        'answer': 2,
                        'explain': 'The sound has to travel a longer round trip, so the echo takes more time to come back.',
                    },
                    {
                        'q': 'Which animal uses echoes to "see" in the dark?',
                        'options': ['A bat', 'A cow', 'A goat', 'A pigeon'],
                        'answer': 0,
                        'explain': 'Bats use echo-location, sending out high squeaks and listening to the echoes — nature\'s ultrasonic sensor.',
                    },
                    {
                        'q': 'Why does the robot divide the echo time by two?',
                        'options': ['To make the number smaller', 'Because sound travels there AND back', 'Because it has two sensors', 'It does not divide'],
                        'answer': 1,
                        'explain': 'The measured time covers the round trip; halving it gives the one-way distance to the wall.',
                    },
                ],
            },
        ],
    },
    {
        'slug': 'robotics-builder',
        'title': 'Robot Builder Workshop',
        'category': 'robotics',
        'age_range': '12-15',
        'level': 'Intermediate',
        'icon': 'build',
        'color': '#0284C7',
        'tagline': 'Drive, steer, grab and dodge — build real robot behaviors.',
        'description': 'Time to take the controls. In this workshop you will drive a two-wheel robot with differential steering, program a line follower, operate a 3-joint robotic arm and let a robot dodge obstacles on its own. Every simulation here mirrors how real competition robots actually work.',
        'skills': ['Differential drive', 'IR line sensing', 'Feedback control', 'Forward kinematics', 'Sense-think-act loops', 'Gripper mechanics'],
        'lessons': [
            {
                'slug': 'motors-and-wheels',
                'title': 'Motors & Wheels',
                'icon': 'directions_car',
                'minutes': 15,
                'sim': 'robotics/differential-drive',
                'sim_type': '3d',
                'summary': 'Control each wheel motor separately and discover how unequal speeds steer a robot — no steering wheel needed.',
                'objectives': [
                    'Drive a robot using only two motor power sliders',
                    'Predict the path from any left/right power combination',
                    'Make the robot spin in place using opposite motor powers',
                    'Explain the differential drive equations in plain words',
                ],
                'knowledge': [
                    {
                        'heading': 'Steering without a steering wheel',
                        'body': 'Most small robots have no steering wheel at all. Instead they use differential drive: two wheels, each with its own motor. Equal power on both sides drives the robot straight. Give the left wheel more power and the robot curves right; more power on the right curves it left.\n\nIt feels strange at first, but you already know this trick — it is exactly how you steer a wheelchair or row a boat with two oars.',
                    },
                    {
                        'heading': 'The math behind the motion',
                        'body': 'Engineers describe differential drive with two simple equations. Forward speed is the average of the wheel speeds: v = (vL + vR) / 2. Turning rate depends on the difference: w = (vR - vL) / L, where L is the distance between the wheels.\n\nSet both sliders to +80 and the difference is zero — no turning, pure forward motion. Set left to +50 and right to +100, and the difference makes the robot arc smoothly to the left.',
                    },
                    {
                        'heading': 'The tank turn',
                        'body': 'Here is the party trick: set the left motor to +60 and the right motor to -60. The average speed is zero, so the robot goes nowhere — but the difference is huge, so it spins on the spot like a top. This is called a tank turn or pivot turn, because tanks steer the same way.\n\nPivot turns are gold in robot competitions: they let a robot turn around in a tight maze corner without needing any extra space.',
                    },
                    {
                        'heading': 'From sliders to real robots',
                        'body': 'On real robots, those slider values become PWM signals — rapid on-off pulses that control how much power each motor receives. A value of 100 means full power; 50 means power half the time.\n\nRobots from vacuum cleaners to Mars rovers use differential steering because it is simple, cheap and precise. With only two motors and clever code, a robot can trace any path you can imagine — watch the trail line in the simulation prove it.',
                    },
                ],
                'fun_fact': 'NASA\'s Perseverance rover has six wheels, each with its own independent motor — it can do a full tank turn on Mars without moving forward a single centimetre!',
                'quiz': [
                    {
                        'q': 'Both motors at +80 power. What does the robot do?',
                        'options': ['Spins in place', 'Drives straight forward', 'Curves left', 'Stops'],
                        'answer': 1,
                        'explain': 'Equal wheel speeds mean zero difference, so there is no turning — the robot drives straight.',
                    },
                    {
                        'q': 'Left motor +100, right motor +40. The robot…',
                        'options': ['Curves toward the right', 'Curves toward the left', 'Drives straight', 'Goes backwards'],
                        'answer': 0,
                        'explain': 'The faster left wheel travels farther than the right, swinging the robot around toward the slower right side.',
                    },
                    {
                        'q': 'How do you make a differential drive robot spin in place?',
                        'options': ['Both motors at zero', 'Both motors at full power', 'Equal and opposite motor powers', 'Remove one wheel'],
                        'answer': 2,
                        'explain': 'Equal and opposite powers make the average speed zero but the difference maximal — a pure pivot turn.',
                    },
                    {
                        'q': 'In v = (vL + vR) / 2, what does v represent?',
                        'options': ['Turning rate', 'Battery voltage', 'The robot\'s forward speed', 'Wheel size'],
                        'answer': 2,
                        'explain': 'Forward speed is simply the average of the left and right wheel speeds.',
                    },
                ],
            },
            {
                'slug': 'line-follower',
                'title': 'Line Follower',
                'icon': 'route',
                'minutes': 15,
                'sim': 'robotics/line-follower',
                'sim_type': '2d',
                'summary': 'Give a robot two IR sensors and a simple rule, then watch it chase a curvy line — until you crank the speed too high.',
                'objectives': [
                    'Explain how an IR sensor tells dark line from light floor',
                    'Trace the bang-bang steering rule: left sensor on line means steer left',
                    'Find the speed limit where the robot starts losing the line',
                    'Describe why feedback makes the robot self-correcting',
                ],
                'knowledge': [
                    {
                        'heading': 'How a robot sees a line',
                        'body': 'An infrared (IR) sensor shines invisible light at the floor and measures how much bounces back. A white floor reflects lots of light; a black line swallows it. So the sensor outputs a simple message: bright means floor, dark means line.\n\nA line follower carries two of these sensors side by side near its nose, watching the ground like a pair of eyes pointed at the track.',
                    },
                    {
                        'heading': 'The bang-bang rule',
                        'body': 'The simplest line-following logic is called bang-bang control, and it fits in three lines: if the left sensor sees the line, steer left. If the right sensor sees it, steer right. If neither sees it, drive straight.\n\nThat is the whole program! The robot constantly drifts off the line a little, notices, and corrects — hundreds of times per minute. The wiggling path you see is the algorithm working, not failing.',
                    },
                    {
                        'heading': 'Feedback: the secret ingredient',
                        'body': 'This wiggle-and-correct cycle is called feedback: the robot senses its own mistake and uses it to fix itself. Feedback is everywhere in engineering — a thermostat that switches a heater on when a room gets cold, or your own hand adjusting a bicycle handlebar without you even thinking.\n\nWithout feedback the robot would be blind: even a perfect launch angle would drift off the track within seconds.',
                    },
                    {
                        'heading': 'Why speed kills (the run)',
                        'body': 'Push the speed slider high and watch what happens at a sharp curve: by the time the sensor spots the line, the robot has already shot past it. Sensors and corrections take time, and at high speed the robot travels too far between checks.\n\nLine-follower races, popular at robotics competitions in Kathmandu and around the world, are won by tuning this exact balance: as fast as possible, but never faster than the feedback can react.',
                    },
                ],
                'fun_fact': 'The fastest competition line-follower robots can complete a twisting track at over 3 metres per second — faster than most people can run!',
                'quiz': [
                    {
                        'q': 'What does an IR line sensor actually measure?',
                        'options': ['The colour of the sky', 'How much infrared light reflects off the floor', 'The robot\'s weight', 'The motor temperature'],
                        'answer': 1,
                        'explain': 'Dark lines absorb IR light while light floors reflect it, so reflection strength reveals what is underneath.',
                    },
                    {
                        'q': 'In bang-bang control, what happens when the LEFT sensor detects the line?',
                        'options': ['The robot steers left', 'The robot steers right', 'The robot stops', 'The robot reverses'],
                        'answer': 0,
                        'explain': 'The line being under the left sensor means the robot drifted right, so it must steer left to recenter.',
                    },
                    {
                        'q': 'Why does the robot lose the line at very high speed?',
                        'options': ['The sensors melt', 'The battery dies', 'It travels too far before it can react to sensor readings', 'Lines move away'],
                        'answer': 2,
                        'explain': 'Feedback needs reaction time; at high speed the robot overshoots curves before corrections can take effect.',
                    },
                    {
                        'q': 'The wiggling path of a line follower shows…',
                        'options': ['A broken robot', 'Feedback corrections happening over and over', 'Wind pushing the robot', 'Low battery'],
                        'answer': 1,
                        'explain': 'Each wiggle is one sense-and-correct cycle — the visible signature of feedback control.',
                    },
                ],
            },
            {
                'slug': 'robotic-arm',
                'title': 'The Robotic Arm',
                'icon': 'precision_manufacturing',
                'minutes': 16,
                'sim': 'robotics/robotic-arm',
                'sim_type': '3d',
                'summary': 'Operate a 3-joint arm with a gripper, grab a ball and learn what degrees of freedom really mean.',
                'objectives': [
                    'Control base, shoulder and elbow joints to position a gripper',
                    'Count the degrees of freedom of the arm',
                    'Grab and release a ball by combining joint moves',
                    'Explain forward kinematics in one sentence',
                ],
                'knowledge': [
                    {
                        'heading': 'Joints and degrees of freedom',
                        'body': 'Every independent way a robot can move is called a degree of freedom, or DOF. This arm has three: the base spins left-right, the shoulder tilts up-down, and the elbow bends. The gripper opening is a bonus mover, but it positions nothing — so we say the arm itself has 3 DOF.\n\nYour own arm has seven degrees of freedom from shoulder to wrist, which is why you can scratch your back in ways no simple robot can.',
                    },
                    {
                        'heading': 'Forward kinematics',
                        'body': 'Forward kinematics answers one question: given every joint angle, where exactly is the gripper tip? The math chains together: the base angle rotates everything, the shoulder angle tilts the upper arm, the elbow angle bends the forearm, and adding it all up gives one point in space.\n\nWhen you move the sliders, the simulation is computing forward kinematics live, every single frame, to draw the arm correctly.',
                    },
                    {
                        'heading': 'The art of grabbing',
                        'body': 'Grabbing looks easy but is famously hard in robotics. The gripper must arrive close enough to the ball, be open before contact, and close at the right moment with the right force — too soft and the ball slips, too hard and it gets crushed.\n\nIn the simulation, the rule is simple: if the gripper tip is near the ball when you close it, the grab succeeds. Real factory robots add force sensors in their fingers to feel exactly this moment.',
                    },
                    {
                        'heading': 'Arms that build our world',
                        'body': 'Industrial robotic arms weld cars, pack medicine, assemble phones and even perform surgery. A typical factory arm has six joints, repeats its motion thousands of times a day, and places parts with accuracy finer than a human hair.\n\nHospitals in Nepal have begun using surgical-assist technology too, and engineering students at universities like Pulchowk Campus build and program arms much like this one as semester projects.',
                    },
                ],
                'fun_fact': 'The robotic arm on the International Space Station, Canadarm2, is 17 metres long and can move itself end-over-end across the station like an inchworm!',
                'quiz': [
                    {
                        'q': 'A "degree of freedom" is…',
                        'options': ['A temperature unit', 'One independent way a robot can move', 'A type of battery', 'The robot\'s top speed'],
                        'answer': 1,
                        'explain': 'Each joint that moves independently adds one degree of freedom to the robot.',
                    },
                    {
                        'q': 'How many degrees of freedom position this arm\'s gripper?',
                        'options': ['One', 'Two', 'Three', 'Ten'],
                        'answer': 2,
                        'explain': 'Base rotation, shoulder tilt and elbow bend — three independent joints position the gripper tip.',
                    },
                    {
                        'q': 'Forward kinematics computes…',
                        'options': ['The gripper position from the joint angles', 'The joint angles from a target', 'Battery usage', 'The robot\'s weight'],
                        'answer': 0,
                        'explain': 'FK goes from known joint angles forward to the resulting position of the end of the arm.',
                    },
                    {
                        'q': 'Why is grabbing objects hard for real robots?',
                        'options': ['Robots dislike balls', 'Grip force and timing must be just right', 'Grippers are always too small', 'It is not hard'],
                        'answer': 1,
                        'explain': 'Too little force drops the object and too much crushes it — sensing the right grip is a real engineering challenge.',
                    },
                ],
            },
            {
                'slug': 'obstacle-avoider',
                'title': 'Obstacle Avoider',
                'icon': 'radar',
                'minutes': 15,
                'sim': 'robotics/obstacle-avoider',
                'sim_type': '3d',
                'summary': 'Switch on the autopilot and watch a robot sense, think and act its way around a field of obstacles.',
                'objectives': [
                    'Describe the sense-think-act loop with this robot as the example',
                    'Tune sensor range and speed and observe the behavior change',
                    'Explain why the robot sometimes gets trapped in corners',
                    'Connect this simple autonomy to real self-driving machines',
                ],
                'knowledge': [
                    {
                        'heading': 'Sense, think, act — repeat forever',
                        'body': 'Every autonomous robot runs the same heartbeat: SENSE the world, THINK about what it means, ACT on the decision — then loop back and do it all again, many times per second.\n\nThis robot senses with a distance cone, thinks with one rule ("is something closer than my threshold?"), and acts by either cruising forward or turning away. Watch the HUD badge flip between CRUISING and TURNING — that is the loop made visible.',
                    },
                    {
                        'heading': 'Reactive behavior',
                        'body': 'This robot has no map and no memory. It reacts purely to what its sensor reports right now — engineers call this reactive control. The beauty is its simplicity: one sensor, one rule, and the robot can wander a cluttered room indefinitely.\n\nThe weakness shows in tight corners: with no memory, the robot can turn away from one wall straight into another, jittering back and forth. Smarter robots add memory and maps to escape such traps.',
                    },
                    {
                        'heading': 'Tuning matters',
                        'body': 'Slide the sensor range down and the robot becomes near-sighted, braking late and turning sharply at the last moment. Slide speed up and its reactions arrive too late for safety, just like the line follower losing its track.\n\nThis tuning act — range versus speed versus turn rate — is exactly what engineers do with real delivery robots and warehouse bots. There is rarely one perfect setting; there are trade-offs chosen for the job.',
                    },
                    {
                        'heading': 'From toy to self-driving',
                        'body': 'A self-driving car is this same loop, scaled up enormously: cameras, radar and lidar for sensing; powerful computers running neural networks for thinking; steering, brakes and throttle for acting — dozens of times every second.\n\nThe principle never changes. Master the sense-think-act loop with one ultrasonic sensor and a toy robot, and you have understood the skeleton of every autonomous machine on Earth.',
                    },
                ],
                'fun_fact': 'Robot vacuum cleaners using simple reactive rules clean millions of homes — early models had no map at all, yet covered whole floors just by bouncing off obstacles randomly!',
                'quiz': [
                    {
                        'q': 'What are the three steps of the autonomy loop?',
                        'options': ['Sense, think, act', 'Start, stop, restart', 'Charge, drive, sleep', 'Look, jump, run'],
                        'answer': 0,
                        'explain': 'Autonomous robots repeatedly sense the world, decide what to do, and act — then loop again.',
                    },
                    {
                        'q': 'This robot turns when…',
                        'options': ['Its battery is low', 'The sensed distance drops below a threshold', 'It feels like it', 'A timer rings'],
                        'answer': 1,
                        'explain': 'The single rule compares sensor distance to a threshold; closer than that means switch to TURNING.',
                    },
                    {
                        'q': 'Why can a purely reactive robot get stuck jittering in a corner?',
                        'options': ['Its wheels break', 'It has no memory or map of where it has been', 'Corners are magnetic', 'The sensor turns off'],
                        'answer': 1,
                        'explain': 'Reacting only to the current reading, it may endlessly trade one nearby wall for another without a plan to escape.',
                    },
                    {
                        'q': 'Increasing speed while keeping sensor range short makes collisions…',
                        'options': ['Less likely', 'More likely', 'Impossible', 'Slower'],
                        'answer': 1,
                        'explain': 'Higher speed means less time to react within the same sensing distance, so crashes become more likely.',
                    },
                ],
            },
        ],
    },
]

COURSES = COURSES + _ADVANCED_COURSES
