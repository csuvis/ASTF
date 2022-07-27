/*
 * @Description: 
 * @Version: 2.0
 * @Autor: 葛璐豪
 * @Date: 2020-10-27 18:25:57
 * @LastEditors: Seven
 * @LastEditTime: 2020-10-27 18:55:07
 */
const path = require('path');

function resolve(dir) {
  return path.join(__dirname, dir);
}
module.exports = {
  configureWebpack: {
    externals: {
     d3: "window.d3",
     sw: "window.sw",
     lan: "window.lan",
     THREE: "window.THREE",
    }
   },
  chainWebpack: (config) => {
    config.resolve.alias
      .set('@', resolve('src'))
      .set('assets',resolve('src/assets'))
      .set('utils',resolve('src/utils'))
      .set('api',resolve('src/api'))
      .set('views',resolve('src/views'))
      .set('components',resolve('src/components'))
  }
};
