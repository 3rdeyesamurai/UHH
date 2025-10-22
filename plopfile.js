module.exports = function (plop) {
  const defaultAuthor = process.env.GIT_AUTHOR_NAME || process.env.GIT_COMMITTER_NAME || '';

  plop.setGenerator('app-node', {
    description: 'Generate a Node + TypeScript application scaffold',
    prompts: [
      { type: 'input', name: 'name', message: 'App name (e.g., api-server):' },
      { type: 'input', name: 'description', message: 'Description:' },
      { type: 'input', name: 'author', message: 'Author:', default: defaultAuthor },
      { type: 'confirm', name: 'useEsm', message: 'Use ESM (type: module)?', default: true },
      { type: 'list', name: 'license', message: 'License:', choices: ['MIT', 'Apache-2.0', 'ISC', 'UNLICENSED'], default: 'MIT' }
    ],
    actions: [
      {
        type: 'addMany',
        destination: 'apps/{{dashCase name}}',
        base: 'generators/app-node',
        templateFiles: 'generators/app-node/**/*',
        globOptions: { dot: true }
      }
    ]
  });

  plop.setGenerator('lib-ts', {
    description: 'Generate a reusable TypeScript library',
    prompts: [
      { type: 'input', name: 'name', message: 'Library name (e.g., utils):' },
      { type: 'input', name: 'description', message: 'Description:' },
      { type: 'input', name: 'author', message: 'Author:', default: defaultAuthor },
      { type: 'confirm', name: 'useEsm', message: 'Use ESM (type: module)?', default: true },
      { type: 'list', name: 'license', message: 'License:', choices: ['MIT', 'Apache-2.0', 'ISC', 'UNLICENSED'], default: 'MIT' },
      { type: 'confirm', name: 'publish', message: 'Prepare for npm publish?', default: true }
    ],
    actions: [
      {
        type: 'addMany',
        destination: 'packages/{{dashCase name}}',
        base: 'generators/lib-ts',
        templateFiles: 'generators/lib-ts/**/*',
        globOptions: { dot: true }
      }
    ]
  });
};
