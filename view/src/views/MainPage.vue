
<template>
  <div>
    <div
      id="riverMainPage"
      :style="{ width: width + 'px', height: height + 'px' }"
    >
      <div>
        <SetTitle
          :type="1"
          :imgPath="require('assets/icons/brush.svg')"
          :message="$lan.view1[$sw]"
        />

        <BrushView :width="width" :height="brushViewHeight" :margin="margin">
        </BrushView>
      </div>
      <div class="viewInter" :style="{ height: inter + 'px' }"></div>
      <div class="abstraction">
        <div
          class="mainTitle"
          :style="{
            lineHeight: titleHeight + 'px',
            width: width + 'px',
            height: titleHeight + 'px',
          }"
        >
          <img
            src="~assets/icons/overView.svg"
            alt=""
            :width="titleHeight - 6 + 'px'"
            :height="titleHeight - 10 + 'px'"
          />
          <span>{{ $lan.view2[$sw] }}</span>
          <div
            v-show="$store.state.selectSignals.length != 0"
            :style="{
              width: '10px',
              height: titleHeight + 'px',
              display: 'inline-block',
              verticalAlign: 'top',
              marginRight: '25px',
              float: 'right',
            }"
          >
            <a
              href="###"
              class="el-icon-close"
              style="text-decoration: none; color: white"
              @click="closeSelectSignals()"
            ></a>
          </div>
          <div
            v-show="$store.state.selectSignals.length != 0"
            :style="{
              width: '10px',
              height: titleHeight + 'px',
              display: 'inline-block',
              verticalAlign: 'top',
              marginRight: '25px',
              float: 'right',
            }"
          >
            <a
              href="###"
              class="el-icon-check"
              style="text-decoration: none; color: white"
              @click="upSelectSignals()"
            ></a>
          </div>

          <div
            v-show="selectMode && $store.state.selectSignals.length == 0"
            :style="{
              width: '10px',
              height: titleHeight + 'px',
              display: 'inline-block',
              verticalAlign: 'top',
              marginRight: '25px',
              float: 'right',
            }"
          >
            <a
              href="###"
              class="el-icon-refresh-left"
              style="text-decoration: none; color: white"
              @click="upRefresh()"
            ></a>
          </div>
        </div>
        <ASTF
          :width="width"
          :height="viewHeight"
          :margin="margin"
          :mode="viewMode"
          :freqDisNum="freqDisNum"
          :equidistantIdScale="equidistantIdScale"
          :smartIdScale="smartIdScale"
          :selectMode="selectMode"
          :nbigUp="nbigUp"
          :refreshFlag="refreshFlag"
        >
        </ASTF>
      </div>
      <div class="viewInter" :style="{ height: inter + 'px' }"></div>
    </div>
  </div>
</template>

<script>
import config from 'api/config'
import ASTF from 'views/ASTF'
import BrushView from 'views/BrushView'
import SetTitle from "components/common/SetTitle"
export default {
  name: "MainPage",
  props: {
    width: {
      type: Number
    },
    height: {
      type: Number
    },
    titleHeight: {
      type: Number
    },
  },
  components: {
    ASTF,
    BrushView,
    SetTitle,
  },
  data () {
    return {
      /* 信号四个维度异常相关参数 */
      refreshFlag: false,
      switchRiverSpec: true,
      meanstdData: {},
      /**/
      wangEnable: false,
      isNonScaling: true,
      showRectInfo: {},
      showRectEnable: false,
      inter: config.viewInter, //每个视图之间的留白
      brushViewHeight: this.$viewPx[this.$viewSW][4],
      riverData: [],
      riverFreRange: [],
      /* 非等比例所需变量 */
      extentFront: [0.5, 4],
      bandFront: [0.1, 2],
      bandScale: d3.scalePow().exponent(1),
      idFreq_array: [],
      frontId_array: [],
      smartIdScale: {},
      /* 平铺所需变量 */
      equidistantBandScale: d3.scaleLinear(),
      equidistantBandFront: [0.1, 2],
      equidistantFront: 0.5,
      equidistantIdScale: {},
      /* */
      testRectInfo: [],
      xScale: d3.scaleLinear(),
      margin: { left: 52, right: 35, top: 25, bottom: 20 },
      upLoading: false,
      selectMode: false,
      //更新间隔river
      upRiverStep: false,
      nbigUp: false,
      abstractData: [],
      overRiverTimeRange: [],
      switchAvgMax: 'MaxBand'
    }
  },
  created () {
  },
  computed: {
    timeStep () {
      return this.$store.state.timeStep
    },
    freqStep () {
      return this.$store.state.freqStep
    },
    smartStep () {
      return { 'extentFront': this.extentFront, 'bandFront': this.bandFront }
    },
    fixedStep () {
      return { 'equidistantFront': this.equidistantFront, 'equidistantBandFront': this.equidistantBandFront }
    },
    //计算需要多少个屏幕来显示Mhz
    freqDisNum () {
      if (this.$store.state.freqMaxDis == 0) {
        return 1
      } else {
        let freqRange = this.$store.state.maxFre - this.$store.state.minFre
        return Math.ceil(freqRange / this.$store.state.freqMaxDis)
      }
    },
    viewHeight () {
      return this.height - this.brushViewHeight - this.titleHeight - this.inter * 2
    },
    extentTimeRange () {  //一重时间
      return [this.$store.state.minTime, this.$store.state.maxTime]
    },
    extentFreRange () {
      return [this.$store.state.minFre, this.$store.state.maxFre]
    },
    dataSet () {
      return this.$store.state.dataSet
    },
    viewMode () {
      return this.$store.state.mode
    },
  },
  methods: {
    /* 不可删 */
    upSelectMode () {
      //全选模式
      if (this.selectMode == false) {
        this.upSmartScale(false)
        this.upEquidistantScale(false)
      } else {
        this.$store.state.disSelectSignals.sort((e1, e2) => e1.avgFre - e2.avgFre)
        this.upSmartScale(true)
        this.upEquidistantScale(true)
        this.nbigUp = !this.nbigUp
      }
    },
    /* 不可删 */
    upSelectSignals () {
      if (this.$store.state.selectSignals.length != 0) {
        this.selectMode = true
        //this.selectShow = false
        this.$store.commit("copyDisSelectSignals")
        this.$store.commit("removeSelectSignals")
        this.$store.commit("upSelectMode", this.selectMode)
        this.upSelectMode()
      }
    },
    /* 不可删 多重选择 */
    closeSelectSignals () {
      this.$store.commit("removeSelectSignals")
    },
    /* 不可删  多重选择 */
    upRefresh () {
      this.$store.commit("removeSelectSignals")
      this.selectMode = false
      this.nbigUp = !this.nbigUp
      this.$store.commit("upSelectMode", this.selectMode)
      this.upSelectMode()
    },
    /* 不可删 */
    upTimeFre () {
      this.upLoading = !this.upLoading
      //setTimeout(()=>{
      this.$store.dispatch('actionUpExtreme', [new Date(this.extentTimeRange[0]).getTime() / 1000
        , new Date(this.extentTimeRange[1]).getTime() / 1000, this.$store.state.minFre, this.$store.state.maxFre]).then(() => {
          this.upSmartScale(this.selectMode)
          this.upEquidistantScale(this.selectMode)
        })
      //},200)  
    },
    /* Smart distribution  */
    upSmartScale (kind, dong = true) {
      let avgInit
      if (kind == false) {
        avgInit = this.$store.state.avgInit
      } else {
        avgInit = this.$store.state.selectSignals
      }
      if (avgInit.length == 0 || avgInit == undefined) {
        return
      }

      let gaps = []
      //动态调整比例 根据数量
      if (dong == true) {
        let signalLength = avgInit.length
        if (signalLength < 40) {
          this.extentFront = [8, 10]
          this.bandFront = [1, 2]
        } else if (signalLength < 60) {
          this.extentFront = [0.1, 0.2]
          this.bandFront = [0.5, 2]
        } else if (signalLength < 80) {
          this.extentFront = [0.1, 0.2]
          this.bandFront = [0.5, 2]
        } else if (signalLength < 100) {
          this.extentFront = [0.1, 0.2]
          this.bandFront = [0.25, 1]
        } else {
          this.extentFront = [0.05, 0.1]
          this.bandFront = [0.1, 0.2]
        }
      }
      this.$emit("upSmartStep", { 'extentFront': this.extentFront, 'bandFront': this.bandFront })
      this.bandScale.domain([this.$store.state.minBand / 2, this.$store.state.maxBand / 2])
        .range(this.bandFront)
      for (let i = 0; i < avgInit.length; ++i) {
        if (i == 0) {
          gaps.push((avgInit[i].avgFre - avgInit[i].MaxBand / 2 - this.extentFreRange[0]))
        } else {
          gaps.push(avgInit[i].avgFre - avgInit[i].MaxBand / 2 - avgInit[i - 1].avgFre - avgInit[i - 1].MaxBand / 2)
        }
      }
      let lastGap = this.extentFreRange[1] - avgInit[avgInit.length - 1].avgFre - avgInit[avgInit.length - 1].MaxBand / 2
      let lastGapFlag = lastGap > 0 ? true : false
      if (lastGapFlag) {
        gaps.push(this.extentFreRange[1] - avgInit[avgInit.length - 1].avgFre - avgInit[avgInit.length - 1].MaxBand / 2)
      }
      let gapScale = d3.scaleLinear().range(this.extentFront)
        .domain(d3.extent(gaps))
      let medium = 0
      let left = 0
      let right = 0
      // id, sum , left , right
      this.idFreq_array = []
      this.smartIdScale = {}
      this.frontId_array = []
      avgInit.forEach((ele, i) => {
        let halfBand = this.bandScale(ele.MaxBand / 2)
        let left_freq = ele.avgFre - ele.MaxBand / 2
        let right_freq = ele.avgFre + ele.MaxBand / 2

        left += gapScale(gaps[i])
        medium = left + halfBand
        right = medium + halfBand
        let tempScale = d3.scaleLinear().domain([left_freq, right_freq])
          .range([left, right])
        this.idFreq_array.push([ele.id, { medium, left, right, left_freq, right_freq, tempScale }])
        this.smartIdScale[ele.id] = tempScale
        this.frontId_array.push([medium, ele])
        left = right
      })
      if (lastGapFlag)
        right += gapScale(gaps[gaps.length - 1])
      //console.log(this.idFreq_array)
      this.xScale.domain([0, right])
        .range([0, this.width - this.margin.left - this.margin.right])
      this.smartIdScale['sum'] = right
    },
    /* Equidistant distribution */
    upEquidistantScale (kind, dong = true) {
      let avgInit
      if (kind == false) {
        avgInit = this.$store.state.avgInit
      } else {
        avgInit = this.$store.state.disSelectSignals
      }
      if (avgInit.length == 0 || avgInit == undefined) {
        return
      }
      if (dong == true) {
        let signalLength = avgInit.length
        if (signalLength < 40) {
          this.equidistantFront = 8  //间隔
          this.equidistantBandFront = [1, 2]  //最小宽度 最大宽度
        } else if (signalLength < 60) {
          this.equidistantFront = 0.1
          this.equidistantBandFront = [0.5, 2]
        } else if (signalLength < 80) {
          this.equidistantFront = 0.1
          this.equidistantBandFront = [0.5, 2]
        } else if (signalLength < 100) {
          this.equidistantFront = 0.1
          this.equidistantBandFront = [0.25, 1]
        } else {
          this.equidistantFront = 0.05
          this.equidistantBandFront = [0.1, 0.2]
        }
      }
      this.$emit("upEquidistantScaleStep", { 'equidistantFront': this.equidistantFront, 'equidistantBandFront': this.equidistantBandFront })
      this.equidistantBandScale.domain([this.$store.state.minBand / 2, this.$store.state.maxBand / 2]).range(this.equidistantBandFront)
      let medium = 0
      let left = 0
      let right = 0
      this.equidistantIdScale = {}
      avgInit.forEach((ele, i) => {
        let halfBand = this.equidistantBandScale(ele[this.switchAvgMax] / 2)
        let left_freq = ele.avgFre - ele[this.switchAvgMax] / 2
        let right_freq = ele.avgFre + ele[this.switchAvgMax] / 2
        left += this.equidistantFront
        medium = left + halfBand
        right = medium + halfBand
        let tempScale = d3.scaleLinear().domain([left_freq, right_freq])
          .range([left, right])
        this.equidistantIdScale[ele.id] = tempScale
        left = right
      })
      this.equidistantIdScale['sum'] = right + this.equidistantFront
    },
  },
  watch: {
    dataSet (val) {
      this.riverData = []
    },
    extentTimeRange () {
      if ((this.extentFreRange[0] == 0 && this.extentFreRange[1] == 0) ||
        (this.extentTimeRange[0] == 0 && this.extentTimeRange[1] == 0)
      ) return
      this.upTimeFre()
    },
    extentFreRange (newVal, oldVal) {
      if (newVal[1] >= oldVal[1] && newVal[0] <= oldVal[0]) { }
      else {
        for (let i = this.$store.state.disSelectSignals.length - 1; i >= 0; --i) {
          let item = this.$store.state.disSelectSignals[i]
          if (item.avgFre < newVal[0] || item.avgFre > newVal[1]) {
            this.$store.state.disSelectSignals.splice(i, 1)
            delete this.$store.state.mapSelectId[item.id]
          }
        }
        this.$store.commit("refreshSelectSignals")
      }
      //判断范围是增大还是减小
      if ((this.extentFreRange[0] == 0 && this.extentFreRange[1] == 0) ||
        (this.extentTimeRange[0] == 0 && this.extentTimeRange[1] == 0)
      ) return
      this.upTimeFre()
    },
  }
}
</script>

<style>
/* 当视图处于两侧选项时,会为地图与河流图增加边框 美化 */
.mapBorder,
.rightBorder {
  border: 2px solid #9a9a9a;
  border-left: none;
  border-radius: 3px;
}
.riveBorder {
  border: 2px solid #9a9a9a;
  border-radius: 3px;
}
img {
  display: inline-block;
  margin: 3px 3px;
  vertical-align: top;
}
#riverImg,
#controllerImg {
  margin: 5px 3px;
}
span {
  vertical-align: top;
}
.mapRefresh {
  display: inline-block;
  text-decoration: none;
  margin-left: 15px;
  vertical-align: 50%;
}
/* 主体 方便放缩时 始终位于中间 */
#view-app {
  width: 1901px;
  margin: 0 auto;
}
/* left为地图+河流 right为id信号选择 */
#view-left {
  display: inline-block;
  vertical-align: top;
}
#view-right {
  display: inline-block;
  vertical-align: top;
}
/* 当视图为两侧时 会调用以下css */
#mainAPP {
  position: relative;
}
#mainMap,
#mainRiver {
  display: inline-block;
  font-size: 0px;
  vertical-align: top;
}
/* 当视图为左上方时 会调用该css */
.mapAb {
  position: absolute;
  top: 32px;
  left: 4px;
  border: 2px solid #9a9a9a;
  border-radius: 3px;
}
.abstraction {
}
#LXBbutton {
  position: absolute;
  right: 7px;
  top: 580px;
}
</style>