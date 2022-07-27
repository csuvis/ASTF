
export default {
    /* 刷选时间和刷选频率更新 */
    upExtremeTime (state, ExtremeTime) {
        state.maxTime = ExtremeTime[1]
        state.minTime = ExtremeTime[0]
    },
    upExtremeFre (state, ExtremeFre) {
        state.maxFre = ExtremeFre[1]
        state.minFre = ExtremeFre[0]
    },
    /* 最大带宽和最小带宽 */
    upExtremeBand (state, ExtremeBand) {
        state.maxBand = ExtremeBand[1]
        state.minBand = ExtremeBand[0]
    },
    /* 更新平均频率和带宽 */
    upAvgInit (state, avgInit) {
        state.avgInit = avgInit
    },

    /* 等比例 非等比例等模式的切换 */
    upMode (state, temp) {
        state.mode = temp
    },
    /*一屏最多Mhz 以及 一屏最多时间*/
    upFreqMaxDis (state, temp) {
        state.freqMaxDis = temp
    },
    /* 增加选中的信号 */
    addSelectSignals (state, temp) {
        if (temp.id in state.mapSelectId && state.mapSelectId[temp.id] != undefined) {
            state.mapSelectId[temp.id] = undefined
            let pos = state.selectSignals.findIndex(ele => ele.id == temp.id)
            state.selectSignals.splice(pos, 1)
        } else {
            state.mapSelectId[temp.id] = true
            state.selectSignals.push(temp)
            console.log(state.selectSignals)
        }
    },
    copyDisSelectSignals (state) {
        state.disSelectSignals = JSON.parse(JSON.stringify(state.selectSignals))
    },
    refreshSelectSignals (state) {
        state.selectSignals = Object.assign([], state.selectSignals)
        state.mapSelectId = Object.assign({}, state.mapSelectId)
    },
    /* 消除所有信号 */
    removeSelectSignals (state) {
        state.mapSelectId = {}
        state.selectSignals = []
    },
    /* 数据集更新 */
    upDataSet (state, temp) {
        state.dataSet = temp
    },
    upDataStep (state, temp) {
        state.timeStep = temp.timeStep
        state.freqStep = temp.freqStep
    },
    upOverStop (state, temp) {
        state.overStop = temp
    },
    /* */
    upSelectMode (state, temp) {
        state.selectMode = temp
    },

}