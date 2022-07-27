<template>
  <div>
    <!-- 上半区域 -->
    <div id="settingView">
      <!--模式相关-->
      <div class="setMode">
        <SetTitle
          :imgPath="require('assets/icons/dataset.svg')"
          message="Data Selection"
        ></SetTitle>
        <!-- 数据集选择 -->
        <div class="select" :style="{ width: selectWidth + 'px' }">
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

      <div class="setMode">
        <SetTitle
          :imgPath="require('assets/icons/colorScale.svg')"
          message="Abstraction Color Scale"
        ></SetTitle>
        <div class="abstraction-color-scale">
          <p>Signal Strength:</p>
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
    titleHeight: {
      type: Number,
    },
  },
  components: {
    SetTitle,
  },
  data () {
    return {
      inter: 10,
      smallTitleHeight: 25,

      dataSet: 0,
      options_dataSet: [
        {
          value: 0,
          label: "Dataset 1 (2 hours)",
        },
        {
          value: 1,
          label: "Dataset 2 (6 hours)",
        },
      ],

      init: true,
    }
  },
  computed: {
    selectWidth () {
      return this.width - 40
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
  margin: 15px auto;
  line-height: 30px;
}
.setMode:nth-child(1) {
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