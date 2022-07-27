<template>
  <div>
    <!-- 上半区域 -->
    <div id="settingView" v-show="switchView == 0">
      <!--模式相关-->
      <div class="setMode">
        <SetTitle
          :imgPath="require('assets/icons/viewManager.svg')"
          :message="$lan.set1[$sw]"
        ></SetTitle>
        <!-- 数据集选择 -->
        <div
          class="select"
          :style="{ width: selectWidth + 'px', marginTop: '8px' }"
        >
          <el-select v-model="dataSet" size="small" placeholder="请选择">
            <el-option
              v-for="item in options_dataSet"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
      </div>
      <!--模式相关-->
      <div class="setMode">
        <SetTitle
          :imgPath="require('assets/icons/viewManager.svg')"
          :message="$lan.set1[$sw]"
        ></SetTitle>
        <div :class="'checkbox-paper'">
          <el-radio v-model="view_mode" :label="1">{{
            $lan.set2[$sw]
          }}</el-radio>
          <el-radio v-model="view_mode" :label="4">{{
            $lan.set3[$sw]
          }}</el-radio>
          <el-radio v-model="view_mode" :label="3">{{
            $lan.set4[$sw]
          }}</el-radio>
        </div>
        <!-- 一屏最大频率 -->
        <div
          class="select"
          :style="{ width: selectWidth + 'px', marginTop: '8px' }"
        >
          <el-select
            v-model="freqMaxDis"
            :disabled="view_mode != 3"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in options_freqMaxDis"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
      </div>
      <div class="setMode">
        <SetTitle
          :imgPath="require('assets/icons/colorScale.svg')"
          message="Abstraction Color Scale"
        ></SetTitle>
        <div class="abstraction-color-scale">
          <p>{{ $lan.set8[$sw] }}:</p>
          <div style="background-color: #8cd6eb">1</div>
          <div style="background-color: #52c1e2">2</div>
          <div style="background-color: #23a6cd">3</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SetTitle from "components/common/SetTitle"
export default {
  name: "Setting",
  props: {
    width: {
      type: Number,
    },
    height: {
      type: Number,
    },
    switchView: {
      type: Number,
    },
    signalSelection: {
      type: Array,
    },
    titleHeight: {
      type: Number,
    },
    tileIdFrontMap: {
      type: Object
    },

    smartStep: {
      type: Object
    },
    fixedStep: {
      type: Object
    },
    riverMouseId: {
      type: String
    }
  },
  components: {
    SetTitle,
  },
  data () {
    return {
      /*异常 离群 阈值切换*/
      autoAbPulse: true,
      signalStep: undefined,
      signalBand: undefined,
      inter: 10,
      smallTitleHeight: 25,
      /* 别删 */
      view_mode: 1,
      freqMaxDis: 0,
      options_freqMaxDis: [
        {
          value: 0,
          label: this.$lan.set5[this.$sw],
        },
        {
          value: 8,
          label: this.$lan.set6[this.$sw] + "8Mhz",
        },
        {
          value: 15,
          label: this.$lan.set6[this.$sw] + "15Mhz",
        },
        {
          value: 20,
          label: this.$lan.set6[this.$sw] + "20Mhz",
        }
      ],
      dataSet: 0,
      options_dataSet: [
        {
          value: 0,
          label: "data 1",
        },
        {
          value: 1,
          label: "data 2",
        },
      ],

      init: true,
      dbmStdNum: 3,
      dbmRatioNum: 0,
      snrStdNum: 3,
      snrRatioNum: 0,
      mapInfo: {},
      freqStdNum: 3,
      bandStdNum: 3,
      freqRatioNum: 12,
      bandRatioNum: 12,
    }
  },
  computed: {
    extentFreRange () {
      return [this.$store.state.minFre, this.$store.state.maxFre]
    },
    selectWidth () {
      return this.width - 40
    },
    buttonEnable () {
      return this.$store.state.selectSignals.length == 0 ? true : false
    },
    viewMode () {
      return this.$store.state.mode
    },
    loading () {
      return this.$store.state.overStop
    },
    storeDataSet () {
      return this.$store.state.dataSet
    },
  },
  mounted () {
  },
  watch: {
    storeDataSet () {
      if (this.dataSet == this.storeDataSet) this.init = false
      this.dataSet = this.storeDataSet
    },
    dataSet (val) {
      this.$store.commit("upDataSet", val)
    },
    view_mode (val) {
      this.$store.commit("upMode", val)
      if (val != 3 && this.freqMaxDis != 0) {
        this.freqMaxDis = 0
      }
      if (val == 3) {
        this.freqMaxDis = 15
      }
    },
    freqMaxDis (val) {
      this.$store.commit("upFreqMaxDis", val)
    },
  },
  methods: {

  },
};
</script>

<style>
#settingView {
  height: 590.5px;
}
.colorSwitch,
.select {
  height: 40px;
  margin: 0px auto;
  margin-top: 7px;
  line-height: 30px;
}
.setMode {
  margin-bottom: 0px;
  padding-top: 10px;
}

.checkbox {
  margin-left: 18px;
  line-height: 30px;
  margin-top: 5px;
  margin-bottom: 5px;
}
.checkbox-paper {
  margin-left: 18px;
  line-height: 30px;
  margin-top: 5px;
  margin-bottom: 5px;
}
.li-common {
  list-style-type: none;
  margin: 0 3px;
}
.ui-common {
  padding: 0px;
}
li:hover {
  color: orange;
}

.colorRect {
  margin-top: 10px;
}

#list .fileButton {
  margin-left: 12px;
  padding: 5px 7px;
  vertical-align: top;
  margin-top: 3px;
}
.center-set-pos {
  padding-top: 33px;
  padding-left: 0px;
}
.abstraction-color-scale {
  margin: 0 auto;
  margin-top: 20px;
  width: 200px;
  height: 20px;
  font-size: 12px;
  line-height: 20px;
  color: #eee;
}
.abstraction-color-scale p {
  float: left;
  margin: 0px;
  padding: 0px;
  padding-right: 10px;
  color: black;
  font-weight: 400;
}
.abstraction-color-scale div {
  float: left;
  width: 30px;
  height: 20px;
  text-align: center;
}
</style>