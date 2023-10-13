module.exports = {
    content: ['./index.html', './kitchen-sink.html', "./node_modules/flowbite/**/*.js"],
    theme: {
      extend: {
        //
      },
    },
    plugins: [require('./src'), require('flowbite/plugin')]
  }