
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
          message="Statistical View"
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
          <span>Abstract Signal Time-Frequency View</span>
        </div>
        <ASTF
          :width="width"
          :height="viewHeight"
          :margin="margin"
          :ASTFUpFlag="ASTFUpFlag"
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
      ASTFUpFlag: false,
      inter: config.viewInter, //每个视图之间的留白
      brushViewHeight: this.$viewPx[this.$viewSW][4],
      xScale: d3.scaleLinear(),
      margin: { left: 52, right: 35, top: 25, bottom: 40 },
      upLoading: false,
    }
  },
  created () {
  },
  computed: {
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
    upTimeFre () {
      this.upLoading = !this.upLoading
      this.$store.dispatch('actionUpExtreme', [new Date(this.extentTimeRange[0]).getTime() / 1000
        , new Date(this.extentTimeRange[1]).getTime() / 1000, this.$store.state.minFre, this.$store.state.maxFre]).then(() => {
          this.ASTFUpFlag = !this.ASTFUpFlag
        })
    },
  },
  watch: {
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