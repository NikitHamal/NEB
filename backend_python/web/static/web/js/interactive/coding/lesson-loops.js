import { setupMazeLesson } from './maze-lesson.js';

export default function init(stage) {
  return setupMazeLesson(stage, {
    palette: ['move-forward', 'turn-left', 'turn-right', 'repeat'],
    intro: 'Welcome back! Today we learn the Repeat block. Put blocks inside it and the robot does them again and again — loops save tons of work!',
    winLines: [
      'Looping legend! That was so much shorter than writing every step!',
      'Repeat for the win! Programmers love loops!',
      'Amazing! One loop did all that work for you!',
    ],
    crashLines: [
      'Bonk! Check how many times your loop repeats — maybe one too many?',
      'Crash! Count the squares again and adjust your repeat number.',
    ],
    missLines: [
      'Not quite there. Try changing the repeat number with the + and − buttons!',
      'Close! Maybe your loop needs one more turn inside it?',
    ],
    allDoneLine: 'Loop the Loop complete! You now wield the mighty power of loops!',
    levels: [
      {
        grid: [
          '#########',
          '#S     G#',
          '#########',
        ],
        dir: 1,
        maxBlocks: 3,
        hint: 'The star is 6 squares away. You could add 6 Move blocks... or put ONE Move inside a Repeat set to 6!',
      },
      {
        grid: [
          '######',
          '#S####',
          '#  ###',
          '##  ##',
          '###  #',
          '####G#',
          '######',
        ],
        dir: 2,
        maxBlocks: 6,
        hint: 'A staircase! The same dance repeats: move, turn left, move, turn right. Put that pattern inside a Repeat!',
      },
      {
        grid: [
          '######',
          '#S   #',
          '#### #',
          '#### #',
          '#G   #',
          '######',
        ],
        dir: 1,
        maxBlocks: 5,
        hint: 'Three long walls to walk. Each side is: move 3 times, then turn right. Can you loop that whole pattern?',
      },
    ],
  });
}
