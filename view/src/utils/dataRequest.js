
import instance from './request'
export function upDataSet (dataSetNum) {
    return instance.get(`/upDataSet?dataSetNum=${dataSetNum}`)
}
export function get_brushInit (timeStep, freqStep) {
    return instance.get(`/get_brushInit?timeStep=${timeStep}&freqStep=${freqStep}`)
}
export function init (startTime, endTime, startFre, endFre) {
    return instance.get(`/init?startTime=${startTime}&endTime=${endTime}&startFre=${startFre}&endFre=${endFre}`)
}

export function getASTFData (flag = false) {
    return instance.post(`/getASTFData`)

}
