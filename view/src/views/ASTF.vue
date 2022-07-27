
<template>
  <div v-loading="loading" element-loading-text="loading...">
    <div
      id="overRiverContanier"
      ref="overRiverContanier"
      :style="{ width: width + 'px', height: height + 'px' }"
    >
      <Gradual />
      <div
        class="chart-body"
        id="overRiverChart"
        ref="overRiverChart"
        :style="{
          width: width - margin.left - margin.right + 'px',
          height: height - margin.top - margin.bottom + 'px',
          top: margin.top + 'px',
          left: margin.left + 'px',
        }"
      >
        <svg
          id="OverRiverSvg"
          :width="svgWidth + 'px'"
          :height="svgHeight + 'px'"
        >
          <g id="main_group">
            <!--第一层全频刷选图-->
            <g id="allGroup">
              <g
                class="allImg"
                v-for="item in selectMode
                  ? freKind.filter((ele) => ele.id in equidistantIdScale)
                  : freKind"
                :key="'img' + item.id"
                :transform="`translate(${getImgPos(
                  item.id,
                  item.avgFre - item[switchAvgMax] / 2
                )},0)`"
              >
                <g
                  class="yAllImg"
                  v-for="(ceil, index) in item.segs"
                  :key="item.id + ':' + index"
                  :transform="`translate(0,${yScale(
                    new Date(item.baseTimeLines[index] * 1000)
                  )})`"
                  @click="addSignal(item)"
                >
                  <RiverImage
                    :width="
                      getImgPos(item.id, item.avgFre + item[switchAvgMax] / 2) -
                      getImgPos(item.id, item.avgFre - item[switchAvgMax] / 2)
                    "
                    :height="
                      Math.ceil(
                        yScale(new Date(item.baseTimeLines[index + 1] * 1000)) -
                          yScale(new Date(item.baseTimeLines[index] * 1000))
                      ) + 0.5
                    "
                    :color="
                      isSelectId(item.id) && false
                        ? '#2c7f97'
                        : ceil.baseKind == 1
                        ? ''
                        : getColor(index, item.segs)
                    "
                    :baseType="ceil.baseKind"
                    :mediumType="isAbFre(ceil, item.id, index)"
                    :topType="isAbPulse(ceil, item.id, index)"
                    :data="{ info: item, index: index }"
                    :range="{
                      x:
                        getImgPos(
                          item.id,
                          item.avgFre - item[switchAvgMax] / 2
                        ) + margin.left,
                      y:
                        yScale(new Date(item.baseTimeLines[index + 1] * 1000)) +
                        margin.top,
                    }"
                    :enableWindows="true"
                    @showRect="showRect"
                    @hideRect="hideRect"
                  />
                </g>
              </g>
              <g>
                <g
                  v-for="item in $store.state.selectSignals"
                  :key="'selectSignal' + item.id"
                  :transform="`translate(${getImgPos(
                    item.id,
                    item.avgFre - item[switchAvgMax] / 2
                  )},0)`"
                  @click="addSignal(item)"
                >
                  <rect
                    :width="
                      getImgPos(item.id, item.avgFre + item[switchAvgMax] / 2) -
                      getImgPos(item.id, item.avgFre - item[switchAvgMax] / 2)
                    "
                    :height="innerHeight"
                    fill="#8ba0a0"
                    opacity="0.2"
                  ></rect>
                </g>
              </g>
            </g>
          </g>
        </svg>
      </div>
      <!--美化水平轴-->
      <div
        class="fixed-beau"
        :style="{ width: width + 'px', height: margin.top + 5 + 'px' }"
      >
        <svg
          v-show="freKind.length != 0"
          :width="width + 'px'"
          :height="margin.top + 5 + 'px'"
        >
          <g :transform="`translate(${margin.left},${margin.top})`">
            <line x1="-6" x2="0" y1="0" y2="0" stroke="currentColor"></line>
            <line x1="0.5" x2="0.5" y1="-6" y2="0" stroke="currentColor"></line>
            <text
              y="-8"
              :x="width - 100"
              fill="black"
              text-anchor="middle"
              :font-size="'10px'"
              font-family="sans-serif"
            >
              Freq/MHz
            </text>
          </g>
        </svg>
      </div>
      <!--美化纵轴-->
      <div
        class="fixed-beau"
        :style="{ width: margin.left + 5 + 'px', height: height + 'px' }"
      >
        <svg
          v-show="freKind.length != 0"
          :width="margin.left + 5 + 'px'"
          :height="height + 'px'"
        >
          <g :transform="`translate(${margin.left},${margin.top})`">
            <text
              x="-8"
              :y="height - 40"
              dy="0.3em"
              fill="black"
              text-anchor="end"
              :font-size="'10px'"
              font-family="sans-serif"
            >
              Time
            </text>
          </g>
        </svg>
      </div>
      <!--纵轴-->
      <div
        class="fixed-left-axis"
        ref="overRiverLeftAxis"
        :style="{
          width: margin.left + 5 + 'px',
          height: height + 'px',
          top: 0 + 'px',
          left: '0px',
        }"
      >
        <svg
          v-show="freKind.length != 0"
          :width="margin.left + 5 + 'px'"
          :height="svgHeight + margin.top + margin.bottom + 'px'"
        >
          <g
            :transform="`translate(${margin.left},${margin.top})`"
            id="line-YAxis"
          ></g>
        </svg>
      </div>
      <!--水平轴-->
      <div
        class="fixed-top-axis"
        ref="overRiverTopAxis"
        :style="{
          width: width - margin.left - margin.right + 'px',
          height: margin.top + 5 + 'px',
          top: '0px',
          left: margin.left + 'px',
        }"
      >
        <svg
          v-show="freKind.length != 0"
          :width="svgWidth + 'px'"
          :height="margin.top + 5 + 'px'"
        >
          <g :transform="`translate(0,${margin.top})`">
            <line
              x1="-6"
              y1="0"
              :x2="innerWidth"
              y2="0"
              stroke="currentColor"
            ></line>

            <g v-show="mode == 1">
              <line
                v-for="(item, index) in freKind.filter(
                  (ele) => ele.id in equidistantIdScale
                )"
                :key="'line' + item.id"
                :y2="write_line(item, index)"
                stroke="currentColor"
                :x1="getImgPos(item.id, item.avgFre)"
                :x2="getImgPos(item.id, item.avgFre)"
              ></line>
              <text
                v-for="(item, index) in freKind.filter(
                  (ele) => ele.id in equidistantIdScale
                )"
                :key="'text' + item.id"
                y="-8"
                :x="getImgPos(item.id, item.avgFre)"
                fill="black"
                text-anchor="middle"
                font-size="10px"
                font-family="sans-serif"
              >
                {{ write_text(item, index) }}
              </text>
            </g>
            <g v-show="mode == 4">
              <g
                v-for="(item, index) in freKind.filter(
                  (ele) => ele.id in equidistantIdScale
                )"
                :key="'tilex' + item.id"
                :transform="`translate(${getImgPos(item.id, item.avgFre)},0)`"
              >
                <line
                  v-if="index % idAxisInter == 0"
                  y2="-6"
                  stroke="currentColor"
                  x1="0"
                  x2="0"
                ></line>
                <text
                  v-if="index % idAxisInter == 0"
                  y="-8"
                  fill="black"
                  text-anchor="middle"
                  font-size="10px"
                  font-family="sans-serif"
                >
                  {{ id_init.get(item.id).avgFre.toFixed(2) + "Mhz" }}
                </text>
              </g>
            </g>
            <g
              v-show="mode == 2 || mode == 3"
              id="line-XAxis"
              ref="lineXAxis"
            ></g>
          </g>
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import RiverImage from "components/svgComponents/RiverImage"
import Gradual from "components/svgComponents/Gradual"
import { getASTFData } from 'utils/dataRequest'
import { format } from 'utils/base'
export default {
  name: "ASTF",
  props: {
    /* View Attributeew  */
    width: {
      type: Number
    },
    height: {
      type: Number
    },
    margin: {
      type: Object
    },
    /* Three distribution models 1:Smart 4:equildistant 2/3:origin*/
    mode: {
      type: Number,
      default: 1,
    },
    /* if signal were selected:true */
    selectMode: {
      type: Boolean,
    },
    /* pages */
    freqDisNum: {
      type: Number,
      default: 1,
    },
    /* smartIdScale */
    smartIdScale: {
      type: Object
    },
    /* equidistantIdScale */
    equidistantIdScale: {
      type: Object
    },
    nbigUp: {
      type: Boolean
    }
  },
  computed: {
    svgWidth () {
      if (this.mode == 1 || this.mode == 2 || this.mode == 4) {
        return this.width - this.margin.left - this.margin.right - 5
      } else {
        return this.width * this.freqDisNum - this.margin.left - this.margin.right
      }
    },
    svgHeight () {
      return this.height - this.margin.top - this.margin.bottom - 5
    },
    innerWidth () {
      return this.svgWidth
    },
    innerHeight () {
      return this.svgHeight
    },
    dataSet () {
      return this.$store.state.dataSet
    },
    id_init () {
      return new Map(this.$store.state.avgInit.map(d => [d.id, d]))
    },
    /* 通过信号数量 计算轴显示间隔 */
    idAxisInter () {
      let length = Object.keys(this.equidistantIdScale).length
      if (length < 15) {
        return 2
      } else {
        return Math.round(length / 10)
      }
    },
    startTime () {
      return new Date(this.$store.state.minTime)
    },
    endTime () {
      return new Date(this.$store.state.maxTime)
    },
    timeInter () {  //时间间隔 单位s
      return (this.endTime.getTime() - this.startTime.getTime()) / 8
    },
    axisHeight () {
      return this.innerHeight / 8
    },
    extentFreRange () {
      return [this.$store.state.minFre, this.$store.state.maxFre]
    },
  },
  data () {
    return {
      /* 是否大更新 */
      isbigUp: false,
      upDataing: false,
      menuEnable: false,
      isNonScaling: true,
      freRange: [],
      DrawOverRiver: {},
      freKind: [],
      partFreKind: [],
      loading: false,
      weightValue: 1,
      extentDbmSnr: [],
      yScale: undefined,
      haveImport: false,
      /* 等比例所用*/
      freScale: undefined,
      freAxis: undefined,
      /* 平铺所用 */
      equidistantScale: d3.scaleLinear(),
      /* 智能分布所用 */
      smartScale: d3.scaleLinear(),
      testEnable: true,
      timeKe: [],
      switchAvgMax: 'MaxBand'
    }
  },
  mounted () {
    this.freScale = d3.scaleLinear().range([0, this.innerWidth])
    this.equidistantScale.range([0, this.innerWidth])
    this.smartScale.range([0, this.innerWidth])
    this.freAxis = d3.axisTop(this.freScale).tickFormat((d, i) => {
      return d + 'MHz'
    }).ticks(10)
    this.yScale = d3.scaleTime().range([this.innerHeight, 0])
  },
  watch: {
    selectMode (val) {
      this.isbigUp = val
    },
    nbigUp () {
      this.isbigUp = true
    },
    innerWidth () {
      this.freScale.range([0, this.innerWidth])
      d3.select("#line-XAxis").call(this.freAxis).selectAll("text")
        .attr("font-size", () => {
          return '10'
        })
      let temp = this.$refs.lineXAxis.getElementsByTagName('text')
      let temp_line = this.$refs.lineXAxis.getElementsByTagName('line')
      temp[temp.length - 1].innerHTML = ""
      temp_line[temp_line.length - 1].style.stroke = 'white'
    },
    innerHeight () {
      this.yScale.range([this.innerHeight, 0])
      let leftAxis = d3.axisLeft(this.yScale).ticks(5)
      let textTemp = d3.select("#line-YAxis").call(leftAxis).selectAll("text").attr("y", "-15").attr("x", "12").attr("transform", "rotate(-45)")
      //let textL = textTemp._groups[0].length
      textTemp.text((d, i) => {
        return format(d, 0)

      })
    },
    dataSet () {
      this.freKind = []
    },
    /* 等间隔 */
    equidistantIdScale () {
      this.equidistantScale.domain([0, this.equidistantIdScale['sum']])
    },
    smartIdScale () {
      this.smartScale.domain([0, this.smartIdScale['sum']])
      this.loading = true
      this.freScale.domain([this.extentFreRange[0], this.extentFreRange[1] + 0.028985507246376812])
      d3.select("#line-XAxis").call(this.freAxis).selectAll("text")
        .attr("font-size", () => {
          return '10'
        })
      let temp = this.$refs.lineXAxis.getElementsByTagName('text')
      let temp_line = this.$refs.lineXAxis.getElementsByTagName('line')
      temp[temp.length - 1].innerHTML = ""
      temp_line[temp_line.length - 1].style.stroke = 'white'
      if (this.isbigUp === true) {
        this.isbigUp = false
        this.loading = false
        return
      }
      getASTFData().then(response => {
        this.yScale.domain([this.endTime, this.startTime])
        let leftAxis = d3.axisLeft(this.yScale).ticks(5)
        let textTemp = d3.select("#line-YAxis").call(leftAxis).selectAll("text").attr("y", "-15").attr("x", "12").attr("transform", "rotate(-45)")
          .attr("font-size", () => {

            return '10'
          })

        textTemp.text((d, i) => {
          this.timeKe.push(d)
          return format(d, 0)

        })
        this.freKind = response.data.data
        this.$emit('testRect', this.freKind)
        this.loading = false
      })
    },
  },
  components: {
    RiverImage,
    Gradual,
  },
  methods: {
    isSelectId (id) {
      let index = this.$store.state.selectSignals.find(d => d.id == id)
      if (index == undefined) return false
      else return true
    },
    addSignal (item) {
      this.$store.commit("addSelectSignals", this.id_init.get(item.id))
    },
    /* 频率或带宽异常 */
    isAbFre (ceil, id, index) {
      return (ceil.baseKind == 1) ? false : (ceil.abFreq || ceil.abBand)
    },
    /* dmb或snr异常 */
    isAbPulse (ceil, id, index) {
      if (ceil.baseKind == 0 || ceil.baseKind == 1) {
        return 0
      } else {
        let dbmAb = ceil.abDbm
        /* 再判断snr是否有强度异常 */
        let snrAb = ceil.abSnr
        let isAb = dbmAb || snrAb
        if (isAb) {
          return 3
        } else {
          return 0
        }
      }
    },
    /* color */
    getColor (index, data) {
      let current = this.getGrade(data[index])
      let upCurrent = 0
      let downCurrent = 0
      //先判断upCurrent
      if (index == 0 || data[index - 1].baseKind == 1) {
        upCurrent = current
      } else {
        upCurrent = this.getGrade(data[index - 1])
      }
      //判断downCurrent
      if (index == data.length - 1 || data[index + 1].baseKind == 1) {
        downCurrent = current
      } else {
        downCurrent = this.getGrade(data[index + 1])
      }
      let sum = upCurrent * 9 + current * 3 + downCurrent
      return `url(#grad${sum})`
    },
    //版本
    getGrade (data) {
      let current
      if (data.avgDbm > -50) current = 2
      else if (data.avgDbm > -70) current = 1
      else current = 0

      return current
    },
    showRect (temp) {
      this.$emit("showRect", temp)
    },
    hideRect () {
      this.$emit("hideRect")
    },

    write_text (item, index) {
      let curr_freq = item.avgFre.toFixed(2)
      let reult = (curr_freq + 'MHz')
      if (index % this.idAxisInter == 0 && index != this.freKind.length - 1) {
        return reult
      } else {
        return ""
      }
    },
    write_line (item, index) {
      if (index % this.idAxisInter == 0 && index != this.freKind.length - 1) {
        return -6
      } else {
        return 0
      }
    },
    getImgPos (id, freq) {
      if (!(id in this.equidistantIdScale)) {
        return
      }
      if (this.mode == 1) {
        let scale = this.smartIdScale[id]
        return this.smartScale(scale(freq))
      } else if (this.mode == 4) {
        let scale = this.equidistantIdScale[id]
        return this.equidistantScale(scale(freq))
      } else if (this.mode == 2 || this.mode == 3) {
        return this.freScale(freq)
      }
    },
  }
}
</script>

<style>
#OverRiver .selection {
  fill: black;
  fill-opacity: 0.5;
  z-index: 2;
}
#overRiverContanier {
  position: relative;
}
.chart-body {
  position: absolute;
  overflow: auto;
}
#overRiverChart {
  overflow-y: hidden;
}
.fixed-beau {
  position: absolute;
  top: 0px;
  left: 0px;
}
.fixed-top-axis {
  position: absolute;
  overflow: hidden;
}
.fixed-left-axis {
  position: absolute;
  overflow: hidden;
}
.fixed-axis {
  display: inline-block;
  position: fixed;
}
.test {
  fill: green;
}
.yAllImg,
.allImg {
  pointer-events: none;
}
.yDie {
  pointer-events: none;
}

#menu {
  border: 0.1px solid #eee;
  margin: 10px 10px;
  position: absolute;
  width: 200px;
  height: 50px;
  background-color: #fff;
  box-shadow: 0.5px 0.5px 1px #222;
}
#menu ul {
  list-style: none;
  margin: 0px 0px;
  margin-top: 3px;
  padding: 0px 0px;
}
#menu ul li {
}
</style>