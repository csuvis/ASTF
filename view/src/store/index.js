
import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'
import config from 'api/config'
Vue.use(Vuex)
const state = {
  selectMode: false,
  /* 刷选时间和刷选频率 */
  maxTime: 0,
  minTime: 0,
  maxFre: 0,
  minFre: 0,
  minBand: 0,
  maxBand: 0,
  /* 数据集极致频率和极致频率 */
  extentMaxTime: config.extentTimeRange[1],
  extentMinTime: config.extentTimeRange[0],
  extentMaxFre: config.extentFreRange[1],
  extentMinFre: config.extentFreRange[0],
  /* 刷选时间下id的平均值 */
  avgInit: [],

  dataSet: -1,  //数据集 第几套数据
  overStop: false,
  /* 等比例 非等比例等模式的切换 */
  mode: 1,
  /* 存储选中的信号 {id,avgFre,avgBand} */
  selectSignals: [],  //临时存储选中的信号
  mapSelectId: {},
  disSelectSignals: [],  //点击确认后拷贝选中的信号
  /*一屏最多Mhz*/
  freqMaxDis: 0,

  timeStep: 60,
  freqStep: 0.5,
}
export default new Vuex.Store({
  state,
  mutations,
  actions,
  modules: {
  }
})
