import { spawn } from 'node:child_process';

export function run(command, args, { input = null, capture = true } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { stdio: [input ? 'pipe' : 'ignore', capture ? 'pipe' : 'inherit', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout?.on('data', (d) => {
      stdout += d;
    });
    child.stderr.on('data', (d) => {
      stderr = (stderr + d).slice(-20000);
    });
    child.once('error', (error) => reject(new Error(`${command} could not start: ${error.message}`)));
    child.once('close', (code) => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`${command} exited with ${code}\n${stderr.slice(-3000)}`));
    });
    if (input) child.stdin.end(input);
  });
}

export const ffmpeg = (args, options) => run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], options);

export async function probe(file) {
  const { stdout } = await run('ffprobe', ['-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', file]);
  return JSON.parse(stdout);
}

export async function hasEncoder(name) {
  const { stdout } = await run('ffmpeg', ['-hide_banner', '-encoders']);
  return stdout.split('\n').some((line) => new RegExp(`\\s${name}\\s`).test(line));
}

export async function version(command) {
  const { stdout } = await run(command, ['-version']);
  return stdout.split('\n')[0];
}
