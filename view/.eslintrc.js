module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential',
    //'@vue/standard'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'space-before-function-paren': 0,
    'no-extra-semi': 0, // 可以多余的冒号
    semi: 0, // 语句可以不需要分号结尾
    // 'comma-dangle': ["error", "always-multiline"],
    'comma-dangle':0,
    'no-multi-spaces': 0, // 不能用多余的空格
    'no-unused-vars': [
      2,
      {
        // 允许声明未使用变量
        vars: 'local',
        // 参数不检查
        args: 'none'
      }
    ]
  },
}
