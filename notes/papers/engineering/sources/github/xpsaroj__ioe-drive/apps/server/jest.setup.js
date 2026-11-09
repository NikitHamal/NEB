// class-validator/class-transformer decorators need this polyfilled globally before any
// decorated class is used - main.ts does this for the real app, tests need it too.
require("reflect-metadata");
