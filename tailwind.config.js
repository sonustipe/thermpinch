/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./thermpinch/pages/**/*.py", // scans all Python files in the pages directory
    "./thermpinch/components/**/*.py", // scans all Python files in the components directory
    "./thermpinch/app/**/*.py", // scans all Python files in the app directory
    "./thermpinch/app.py", // scans all Python files in the lib directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
