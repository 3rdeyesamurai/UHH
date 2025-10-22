export function main(): void {
  console.log('Hello from demo-app');
}

// Support both ESM and CJS run styles
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
const isMain = typeof require !== 'undefined' && require.main === module;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
const isEsmMain = typeof import.meta !== 'undefined' && import.meta.url === `file://${process.argv[1]}`;

if (isMain || isEsmMain) {
  main();
}
