import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repo = path.resolve(root, '..', '..');
const site = path.join(repo, 'backend_python', 'web', 'static', 'web');

export const P = {
  root,
  repo,
  site,
  stage: path.join(root, 'stage'),
  assets: path.join(root, 'assets'),
  fonts: path.join(root, 'assets', 'fonts'),
  captures: path.join(root, 'assets', 'captures'),
  spec: path.join(root, 'spec'),
  specFile: path.join(root, 'spec', 'launch.spec.json'),
  factsFile: path.join(root, 'spec', 'facts.generated.json'),
  out: path.join(root, 'out'),
  dist: path.join(root, 'dist'),
};

export const mounts = () => ({
  '/stage': P.stage,
  '/assets': P.assets,
  '/spec': P.spec,
  '/site': site,
});
