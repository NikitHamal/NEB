import { setupMazeLesson } from './maze-lesson.js';

export default function init(stage) {
  return setupMazeLesson(stage, {
    palette: ['move-forward', 'turn-left', 'turn-right', 'repeat', 'if-path'],
    intro: 'New super-block: IF path ahead! Blocks inside it only run when the way is clear. It\'s like the robot looking before it leaps!',
    winLines: [
      'Brilliant! The robot made smart choices all by itself!',
      'That\'s real thinking code — the robot checked before moving!',
      'Genius! If-blocks + loops = a robot that adapts!',
    ],
    crashLines: [
      'Bonk! Remember: Move inside an IF block never crashes. A bare Move can!',
      'Crash! Try wrapping your Move blocks in the IF path ahead block.',
    ],
    missLines: [
      'Hmm, not at the star yet. Does your loop repeat enough times?',
      'Almost! Walk until a wall, then turn — does your program do that?',
    ],
    allDoneLine: 'Smart Choices complete! Sequences, loops AND conditionals — you know the three building blocks of every program ever written!',
    levels: [
      {
        grid: [
          '########',
          '#S   G##',
          '########',
        ],
        dir: 1,
        maxBlocks: 3,
        hint: 'Try Repeat 6 with IF path ahead and a Move inside. The robot walks to the star and the IF stops it crashing into the wall!',
      },
      {
        grid: [
          '########',
          '#S     #',
          '###### #',
          '###### #',
          '######G#',
          '########',
        ],
        dir: 1,
        maxBlocks: 6,
        hint: 'Walk until the wall, turn right, walk again. Try: Repeat 2 of [Repeat 6 of [IF path: Move], Turn right].',
      },
      {
        grid: [
          '#########',
          '#S      #',
          '####### #',
          '#    G# #',
          '# ##### #',
          '#       #',
          '#########',
        ],
        dir: 1,
        maxBlocks: 6,
        stepDelay: 180,
        hint: 'A giant spiral! One smart pattern solves it: keep moving while the path is clear, turn right at every wall. Loop that 5 times!',
      },
    ],
  });
}
