
<template>
  <div :style="{ height: height + 'px', width: width + 'px' }">
    <svg :width="width + 'px'" :height="height + 'px'">
      <g id="brushTime" :transform="`translate(${margin.left},${margin.top})`">
        <g id="brushTimeXAxis" :transform="`translate(0,${innerHeight})`">
          <text
            :x="innerWidth"
            y="9"
            dy="0.71em"
            fill="currentColor"
            text-anchor="middle"
          >
            Time
          </text>
        </g>
        <g id="brushTimeYAxis">
          <text x="-9" dy="-0.3em" fill="currentColor">Signal</text>
          <text x="-9" dy="0.7em" fill="currentColor">Counts</text>
        </g>
        <path
          id="brushTimePath"
          :d="timeNumberArea(timeData)"
          fill="noe"
        ></path>
      </g>

      <g
        id="brushFre"
        :transform="`translate(${halfWidth + margin.left + inter},${
          margin.top
        })`"
      >
        <g id="brushFreXAxis" :transform="`translate(0,${innerHeight})`">
          <text
            :x="innerWidth - 10"
            y="9"
            dy="0.71em"
            fill="currentColor"
            text-anchor="middle"
          >
            Freq/MHz
          </text>
        </g>
        <g id="brushFreYAxis">
          <text x="-9" dy="-0.3em" fill="currentColor">Signal</text>
          <text x="-9" dy="0.7em" fill="currentColor">Counts</text>
        </g>
        <path
          id="brushFreqPath"
          :d="freqNumberArea(freqData)"
          fill="noe"
        ></path>
      </g>
    </svg>
  </div>
</template>

<script>
import $ from 'jquery'
import { format } from 'utils/base'
import { get_brushInit, upDataSet } from 'utils/dataRequest'
import config from 'api/config'
export default {
  name: 'BrushView',
  props: {
    width: {
      type: Number
    },
    height: {
      type: Number,
    },
    margin: {
      type: Object
    },
  },
  computed: {
    halfWidth () {
      return (this.width - this.margin.left - this.margin.right - this.inter) / 2
    },
    innerWidth () {
      return this.halfWidth
    },
    innerHeight () {
      return this.height - this.margin.top - this.margin.bottom
    },
    dataSet () {
      return this.$store.state.dataSet
    },
    timeStep () {
      return this.$store.state.timeStep
    },
    freqStep () {
      return this.$store.state.freqStep
    },
  },
  data () {
    return {
      webmenuEnable: false,
      isUpProc: false,
      inter: 100,
      scaleTime: d3.scaleTime()
        .domain([new Date(config.extentTimeRange[0]), new Date(config.extentTimeRange[1])]).nice(),
      fScaleTime: d3.scaleTime()
        .domain([new Date(config.extentTimeRange[0]), new Date(config.extentTimeRange[1])]).nice(),
      scaleFre: d3.scaleLinear().domain(config.extentFreRange),
      timeBrush: d3.brushX(),
      freBrush: d3.brushX(),
      timeNumberScale: d3.scaleLinear(),
      freqNumberScale: d3.scaleLinear(),
      timeData: [],
      timeNumberArea: d3.line(),
      freqNumberArea: d3.line(),
      freqData: [], //右上所需数据
      timeBottom: undefined,
      FreBottom: undefined,
      numberLeft: undefined,
      freqNumberLeft: undefined,
      timeGroup: undefined,
      freGroup: undefined,
      init: true,
      allTimeRange: [],
      allFreRange: [],
    }
  },
  watch: {
    dataSet () {
      if (this.isUpProc == false) {
        this.isUpProc = true
        this.refresh()
        this.isUpProc = false
      }
    },
    timeStep () {
      if (this.isUpProc == false) {
        this.isUpProc = true
        this.upData()
        this.isUpProc = false
      }
    },
    freqStep () {
      if (this.isUpProc == false) {
        this.isUpProc = true
        this.upData()
        this.isUpProc = false
      }
    },
  },
  mounted () {
    this.scaleTime.range([0, this.innerWidth])
    this.scaleFre.range([0, this.innerWidth])
    this.fScaleTime.range([this.innerHeight, 0])
    this.timeGroup = d3.select("#brushTime")
    this.freGroup = d3.select("#brushFre")
    this.timeNumberScale.range([this.innerHeight, 0])
    this.freqNumberScale.range([this.innerHeight, 0])
    this.timeBottom = d3.axisBottom(this.scaleTime).tickFormat((d, i) => format(d, 2)).ticks(5)
    this.numberLeft = d3.axisLeft(this.timeNumberScale).ticks(5).tickFormat((d, i) => i == 0 ? "" : d)

    this.FreBottom = d3.axisBottom(this.scaleFre).tickFormat((d, i) => `${d}MHz`)
    this.freqNumberLeft = d3.axisLeft(this.freqNumberScale).ticks(5).tickFormat((d, i) => i == 0 ? "" : d)
    //this.timeLeft = d3.axisLeft(this.fScaleTime).tickFormat((d,i)=>i==0?"":format(d,2)).ticks(5)

    this.timeBrush.extent([[0, 0], [this.innerWidth, this.innerHeight]])
    this.freBrush.extent([[0, 0], [this.innerWidth, this.innerHeight]])
    this.timeBrush.on("brush end", () => {
      if (d3.event.type != "end") return
      if (d3.event.selection == undefined) return
      let timeRange = d3.event.selection.map(this.scaleTime.invert).reverse()
      this.$store.commit("upExtremeTime", [timeRange[1], timeRange[0]])
    })
    this.freBrush.on("brush end", () => {
      if (d3.event.type != "end") return
      if (d3.event.selection == undefined) return
      let freRange = d3.event.selection.map(this.scaleFre.invert).reverse()
      this.$store.commit("upExtremeFre", [freRange[1], freRange[0]])
    })
    this.timeGroup.call(this.timeBrush)
    this.freGroup.call(this.freBrush)
    this.upData()
  },
  methods: {
    openLXB (event) {
      let menu = $("#webmenu")
      menu.css({
        "top": event.clientY,
        "left": event.clientX,
        "height": '25px'
      })
      this.webmenuEnable = true
    },
    enterWeb () {
      this.webmenuEnable = false
      if ((this.$store.state.maxtime == 0 && this.$store.state.minTime == 0)
        || (this.$store.state.maxFre == 0 && this.$store.state.minFre == 0)) {
        this.$message("尚未刷选,请刷选时频")
        return
      }
      window.open('http://127.0.0.1:4888', 'target', '')
    },
    closeMenu () {
      this.webmenuEnable = false
    },
    upData () {
      this.timeData = []
      this.freqData = []
      get_brushInit(this.timeStep, this.freqStep).then(response => {
        this.$store.commit("upDataSet", response.data.dataSet)

        //this.timeBrush
        //this.freBrush
        //console.log("upDataSet",response.data.dataSet)
        let extentDate = [new Date(response.data.minTime * 1000), new Date(response.data.maxTime * 1000)]
        // console.log(extentDate)
        this.allTimeRange = extentDate
        this.scaleTime.domain(extentDate).nice()
        this.fScaleTime.domain(extentDate).nice()
        //console.log(response.data.minFre,response.data.maxFre)
        this.scaleFre.domain([response.data.minFre, response.data.maxFre])
        this.allFreRange = [response.data.minFre, response.data.maxFre]
        let data = response.data.timeBrush
        this.freqData = response.data.freqBrush
        let freqNumberMaxCnt = response.data.freqNumberMaxCnt
        let maxCnt = 0
        for (let i = 0; i < data.length; ++i) {
          maxCnt = Math.max(maxCnt, data[i].cnt)
          this.timeData.push({ 'time': new Date(data[i].time * 1000), 'cnt': data[i].cnt })
        }
        this.timeNumberScale.domain([0, maxCnt]).nice()
        this.freqNumberScale.domain([0, freqNumberMaxCnt]).nice()
        this.timeNumberArea.x(d => this.scaleTime(d.time))
          .y(d => this.timeNumberScale(d.cnt))
        this.freqNumberArea.x(d => this.scaleFre(d.freq))
          .y(d => this.freqNumberScale(d.cnt))
        this.timeGroup.select("#brushTimeYAxis").call(this.numberLeft)
        this.timeGroup.select("#brushTimeXAxis").call(this.timeBottom)
        this.freGroup.select("#brushFreXAxis").call(this.FreBottom)
        this.freGroup.select("#brushFreYAxis").call(this.freqNumberLeft)
        let bruYG = document.querySelectorAll("#brushTimeYAxis text")
        let bruXG = document.querySelectorAll("#brushTimeXAxis text")
        let FruXg = document.querySelectorAll("#brushFreXAxis text")
        let FruYg = document.querySelectorAll("#brushFreYAxis text")
        bruYG[bruYG.length - 1].innerHTML = ""
        bruXG[bruXG.length - 1].innerHTML = ""
        FruXg[FruXg.length - 1].innerHTML = ""
        FruYg[FruYg.length - 1].innerHTML = ""
        bruYG = document.querySelectorAll("#brushTimeYAxis line")
        bruXG = document.querySelectorAll("#brushTimeXAxis line")
        FruXg = document.querySelectorAll("#brushFreXAxis line")
        FruYg = document.querySelectorAll("#brushFreYAxis line")
        bruYG[bruYG.length - 1].style.stroke = "white"
        bruXG[bruXG.length - 1].style.stroke = "white"
        FruXg[FruXg.length - 1].style.stroke = "white"
        FruYg[FruYg.length - 1].style.stroke = "white"
        //console.log(document.querySelectorAll("#brushTimeYAxis text"))
        //let l1 = this.timeGroup.selectAll("#brushTimeYAxis text")._groups[0].length-1
        // let l2 = this.timeGroup.selectAll("#brushTimeXAxis text")._groups[0].length-1
        //console.log(this.timeGroup.selectAll("#brushTimeYAxis text")._groups[0])
        const { freqRange, timeRange } = config.dataInitBrushRange[response.data.dataSet]
        const timeRangeX = [
          this.scaleTime(timeRange[0]), this.scaleTime(timeRange[1])
        ]
        const freqRangeX = [
          this.scaleFre(freqRange[0]),
          this.scaleFre(freqRange[1])
        ]
        setTimeout(() => {
          this.timeBrush.move(this.timeGroup, timeRangeX)
          this.freBrush.move(this.freGroup, freqRangeX)
        }, 500)

      })
    },
    refresh () {
      //console.log("**************refresh************")
      if (this.init == false) {
        this.$store.commit("upExtremeTime", [0, 0])
        this.$store.commit("upExtremeFre", [0, 0])
        this.timeBrush.move(d3.select("#brushTime"), null)
        this.freBrush.move(d3.select("#brushFre"), null)
        this.$store.commit("upOverStop", true)
        this.timeData = []
        this.freqData = []
        upDataSet(this.dataSet).then(response => {
          if (response.data == "success") {
            this.$store.commit("removeSelectSignals")
            this.upData()
            this.$store.commit("upOverStop", false)
          }
        })
      } else {
        this.init = false
      }
    },
  },
}
</script>

<style>
#brushTimePath,
#brushFreqPath {
  stroke: black;
}
#webmenu {
  border: 0.1px solid #eee;
  margin: 10px 10px;
  position: absolute;
  width: 332px;
  height: 50px;
  background-color: #fff;
  box-shadow: 0.5px 0.5px 1px #222;
}
#webmenu ul {
  list-style: none;
  margin: 0px 0px;
  margin-top: 3px;
  padding: 0px 0px;
}
</style>