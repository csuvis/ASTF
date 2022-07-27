
import { init } from 'utils/dataRequest'
export default {
    actionUpExtreme (context, set) {
        return new Promise(resolve => {
            init(set[0], set[1], set[2], set[3]).then(response => {
                let avgInit = response.data.avg
                let extentBand = [response.data.extent.MinBand, response.data.extent.MaxBand]
                //upExtremeBand
                context.commit('upAvgInit', avgInit)
                context.commit('upExtremeBand', extentBand)
                resolve("over")
            })
        })
    }
}