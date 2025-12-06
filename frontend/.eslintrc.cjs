module.exports = {
  env: { browser: true, es2020: true },
  extends: ["eslint:recommended", "plugin:react-hooks/recommended"],
  parserOptions: { sourceType: "module", ecmaVersion: "latest" },
  settings: { react: { version: "detect" } },
  rules: {},
};
