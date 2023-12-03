module.exports = {
	env: {
		browser: true,
		es2021: true,
	},
	extends: [
		'eslint:recommended',
		'plugin:@typescript-eslint/recommended',
		'plugin:react/recommended',
		'plugin:typescript-sort-keys/recommended',
	],
	overrides: [
		{
			env: {
				node: true,
			},
			files: ['.eslintrc.{js,cjs}'],
			parserOptions: {
				sourceType: 'script',
			},
		},
	],
	parser: '@typescript-eslint/parser',
	parserOptions: {
		ecmaVersion: 'latest',
		sourceType: 'module',
	},
	plugins: [
		'@typescript-eslint',
		'prettier',
		'simple-import-sort',
		'import',
		'typescript-sort-keys',
		'sort-keys-fix',
		'unused-imports',
	],
	rules: {
		'import/first': 'error',
		'import/newline-after-import': [
			'error',
			{
				count: 2,
			},
		],
		'import/no-duplicates': 'error',
		indent: ['error', 'tab'],
		'linebreak-style': ['error', 'windows'],
		// 'prettier/prettier': [
		// 	'error',
		// 	{
		// 		endOfLine: 'crlf',
		// 		printWidth: 120,
		// 		singleQuote: true,
		// 		tabWidth: 4,
		// 	},
		// ],
		quotes: ['error', 'single'],
		'react/jsx-sort-props': [
			2,
			{
				callbacksLast: true,
				ignoreCase: true,
				noSortAlphabetically: false,
				shorthandFirst: false,
				shorthandLast: true,
			},
		],
		'react/react-in-jsx-scope': 'off',
		semi: ['error', 'always'],
		'simple-import-sort/imports': 'error',
		'sort-imports': [
			'error',
			{
				allowSeparatedGroups: true,
				ignoreCase: true,
				ignoreDeclarationSort: true,
				ignoreMemberSort: false,
				memberSyntaxSortOrder: ['none', 'all', 'multiple', 'single'],
			},
		],
		'sort-keys': ['error', 'asc'],
		'typescript-sort-keys/interface': 'error',
		'typescript-sort-keys/string-enum': 'error',
		'unused-imports/no-unused-imports': 'error',
	},
};
