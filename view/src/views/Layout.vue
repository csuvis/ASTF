<template>
  <!-- 1920 * 850 -->
  <div v-loading="loading" element-loading-text="后端切换数据集中,请稍等...">
    <div>
      <!-- 全局提示框 -->
      <div id="tooltip"></div>
      <!-- 最外层容器 -->
      <div
        id="home"
        :style="{ width: appWidth + 'px', height: appHeight + 'px' }"
      >
        <!-- MainPage -->
        <div
          id="leftContainer"
          :style="{ width: leftWidth + 'px', height: appHeight + 'px' }"
        >
          <MainPage
            :width="leftWidth"
            :height="leftHeight"
            :lightItem="lightItem"
            :stopItem="stopItem"
            :titleHeight="titleHeight"
            :colorSwitch="colorSwitch"
            @upTileIdFrontMap="upTileIdFrontMap"
            @overRiverSignalId="overRiverSignalId"
            @leaveRiverSignalId="leaveRiverSignalId"
          >
          </MainPage>
        </div>
        <div
          id="midleInter"
          class="viewInter"
          :style="{ width: marin_middle + 'px', height: appHeight + 'px' }"
        ></div>
        <!-- 右侧Controller -->
        <div
          id="rightContainer"
          :style="{ width: rightWidth + 'px', height: appHeight + 'px' }"
        >
          <div
            class="mainTitle"
            :style="{
              width: rightWidth + 'px',
              height: titleHeight + 'px',
              lineHeight: titleHeight + 'px',
            }"
          >
            <a
              href="###"
              style="text-decoration: none; color: #f7fafb"
              @click="switchSetMap(0)"
            >
              <img
                id="controllerImg"
                src="~assets/icons/controller.svg"
                alt=""
                :width="titleHeight - 6 + 'px'"
                :height="titleHeight - 10 + 'px'"
              />
              <span>{{ $lan.view5[$sw] }}</span>
            </a>
          </div>
          <Setting
            :width="rightWidth"
            :height="leftHeight"
            :switchView="switchView"
            @HightLight="HightLight"
            @stopLight="stopLight"
            :titleHeight="titleHeight"
            :tileIdFrontMap="tileIdFrontMap"
            :smartStep="smartStep"
            :fixedStep="fixedStep"
            :riverMouseId="riverMouseId"
          ></Setting>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import config from 'api/config'
import MainPage from "views/MainPage"
import Setting from "views/Setting"

export default {
  name: "Layout",
  data () {
    return {
      appWidth: this.$viewPx[this.$viewSW][0],
      appHeight: this.$viewPx[this.$viewSW][1],
      leftWidth: this.$viewPx[this.$viewSW][2],
      marin_middle: config.viewInter,
      titleHeight: this.$viewPx[this.$viewSW][3],
      lightItem: {},
      stopItem: {},
      colorSwitch: 0,
      switchView: 0,
      tileIdFrontMap: {},

      //智能
      smartStep: {},
      fixedStep: {},
      //river
      riverMouseId: '',
    }
  },
  computed: {
    leftHeight () {
      return this.appHeight
    },
    rightWidth () {
      return this.appWidth - this.leftWidth - this.marin_middle
    },
    rightHeight () {
      return this.appHeight - this.titleHeight
    },
    loading () {
      return this.$store.state.overStop
    },
    dataSetStore () {
      return this.$store.state.dataSetStore
    },
    mode () {
      return this.$store.state.mode
    },
  },
  components: {
    MainPage,
    Setting,
  },
  created () { },
  methods: {
    overRiverSignalId (id) {
      this.riverMouseId = id
    },
    leaveRiverSignalId (id) {
      this.riverMouseId = id
    },
    /*
    setImportSignal(temp) {
      this.importSignal = temp
    },
    */
    upTileIdFrontMap (temp) {
      this.tileIdFrontMap = temp
    },
    switchSetMap (temp) {
      this.switchView = temp
    },

    HightLight (temp) {
      this.lightItem = temp
    },
    stopLight (temp) {
      this.stopItem = temp
    },
  }
};
</script>
<style>
body {
  font-family: sans-serif;
  font-size: 18px;
  padding: 0px;
  background-color: #efefef;
}
#home {
  box-sizing: border-box;
  position: relative;
  height: 100%;
  margin: 0 auto;
  margin-top: 3px;
}
/*background-color: #eaeff5; */
#leftContainer,
#rightContainer,
#midleInter {
  display: inline-block;
  vertical-align: top;
  background-color: #ffffff;
  /*background: rgb(62, 170, 62,0.);*/
  overflow-x: hidden;
  overflow-y: hidden;
}
#home .viewInter {
  background-color: #efefef;
  /*   background-color: #A94CAF;   
  background-color: #a862ad; 
  background-color: #a782aa;  */
}
#rightContainer {
  overflow-y: auto;
}
/* 标题 */
.mainTitle {
  /*颜色备用rgba(128,128,135,1)  #313131  #bababa #263733 33, 48, 48 */
  /* (33, 48, 48,0.85)  rgba(33, 75, 48,0.85) 
  236, 223, 47*/
  /* 绿色系列 */
  /*  background-color: rgba(33, 75, 48,0.85);  */
  /* 黑色系列 */
  background-color: rgba(33, 48, 48, 0.85);
  /* 紫色系列  A94CAF*/
  /* background-color: #A94CAF ; */
  /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/

  font-family: "Avenir";
  font-size: 18px;
  color: #f7fafb;
  font-weight: 600;
  box-shadow: 0px 0.8px 0.2px 0.2px rgba(0, 0, 0, 0.1);
}
#controllerImg,
#mapImg {
  margin-bottom: 10px;
}

img {
  display: inline-block;
  margin: 5px 3px;
}
span {
  vertical-align: top;
}
/* 提示窗口 */
#tooltip {
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 4px;
  font-size: 16px;
  line-height: 20px;
  color: #fff;
  position: absolute;
  z-index: 99;
  display: none;
}
#tooltip > p {
  margin: 0px;
  padding: 0px;
}
.center-nset-pos {
  position: absolute;
  bottom: 600px;
  right: 10px;
}
</style>
