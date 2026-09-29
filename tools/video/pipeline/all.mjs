export async function run({ flags }) {
  const steps = ['doctor', 'render', 'audio', 'mux', 'qa'];
  for (const step of steps) {
    console.log(`\n=== ${step} ===`);
    const module = await import(`./${step}.mjs`);
    await module.run({ positional: [], flags });
  }
}
