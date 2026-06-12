import { setupMazeLesson } from './maze-lesson.js';

export default function init(stage) {
  return setupMazeLesson(stage, {
    palette: ['move-forward', 'turn-left', 'turn-right'],
    intro: 'Hi, I\'m Neby! A program is a list of step-by-step instructions. Stack blocks in order, press Run, and watch the robot follow them to the star!',
    winLines: [
      'Woohoo! The robot followed your instructions perfectly!',
      'Star collected! Your program worked!',
      'Yes! Step by step, just like a real programmer!',
    ],
    crashLines: [
      'Bonk! The robot bumped a wall. Computers follow instructions exactly — check each step!',
      'Ouch! A wall! Try changing the order or direction of your blocks.',
    ],
    missLines: [
      'The robot stopped before the star. Maybe it needs a few more blocks?',
      'So close! Count the squares to the star and check your steps.',
    ],
    allDoneLine: 'You completed First Steps! You just wrote your first programs!',
    levels: [
      {
        grid: [
          '#####',
          '#S G#',
          '#####',
        ],
        dir: 1,
        hint: 'The star is 2 squares ahead. Add two Move forward blocks and press Run!',
      },
      {
        grid: [
          '######',
          '#S  ##',
          '## ###',
          '## G##',
          '######',
        ],
        dir: 1,
        hint: 'This path bends! Move forward, then Turn right, then keep moving.',
      },
      {
        grid: [
          '#######',
          '#### G#',
          '####  #',
          '#S    #',
          '####  #',
          '#######',
        ],
        dir: 1,
        hint: 'Two turns this time. Plan the whole route before you press Run!',
      },
    ],
  });
}
