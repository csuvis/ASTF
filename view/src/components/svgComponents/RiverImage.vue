<!--
 * @Description: 
 * @Version: 2.0
 * @Autor: 葛璐豪
 * @Date: 2021-01-15 21:46:02
 * @LastEditors: Seven
 * @LastEditTime: 2021-01-17 12:03:58
-->
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    version="1.1"
    :width="width + 'px'"
    :height="height + 'px'"
    viewBox="0 0 10 10"
    preserveAspectRatio="none slice"
    :class="{ activeShow: enableWindows }"
  >
    <rect
      width="10"
      height="10"
      fill="transparent"
      :stroke="wangEnable ? '#888' : 'transparent'"
    ></rect>
    <!-- type==0为底层样式 -->
    <g>
      <!-- 空白 -->
      <g v-if="baseType == 1" class="vanish"></g>
      <!-- 矩形 -->
      <g v-else-if="baseType == 2" class="often">
        <rect
          x="0"
          y="0"
          width="10"
          height="10"
          :fill="color"
          stroke-width="2"
        />
      </g>
      <!-- 半矩形+下半三角 -->
      <g v-else-if="baseType == 4" class="more">
        <polygon
          points="0,0 0,5 5,9.9 10,5 10,0"
          :fill="color"
          stroke-width="2"
        ></polygon>
      </g>
      <!-- 半矩形+下半三角+短联线 -->
      <g v-else-if="baseType == 8" class="more">
        <polygon
          points="0,0 0,5 5,9.9 10,5 10,0"
          :fill="color"
          stroke-width="2"
        ></polygon>
        <rect
          x="-0.15"
          y="9.16"
          width="5.2"
          height="0.8"
          :fill="color"
          transform="translate(0,0)rotate(23,5 10)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="4.95"
          y="9.16"
          width="5.2"
          height="0.8"
          :fill="color"
          rx="0.4"
          ry="0.4"
          transform="rotate(-23,5 10)"
        ></rect>
      </g>
      <!-- 上半三角+半矩形 -->
      <g v-if="baseType == 3" class="less">
        <polygon
          points="5,0.1 0,5 0,10 10,10 10,5"
          :fill="color"
          stroke-width="2"
        ></polygon>
      </g>
      <!-- 上半三角+半矩形+短联线 -->
      <g v-if="baseType == 7" class="less">
        <rect
          x="0"
          y="0.2"
          width="5.30"
          height="0.8"
          :fill="color"
          transform="translate(5.5,0.9)rotate(-204)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="0"
          y="0.2"
          width="5.30"
          height="0.8"
          :fill="color"
          transform="translate(5.0,-0.2)rotate(24)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <polygon
          points="5,0.1 0,5 0,10 10,10 10,5"
          :fill="color"
          stroke-width="2"
        ></polygon>
      </g>

      <!-- 菱形 -->
      <g v-else-if="baseType == 5" class="over">
        <polygon
          points="5,0.2 0,5 5,9.8 10,5"
          :fill="color"
          stroke-width="2"
        ></polygon>
      </g>
      <!-- 菱形＋短联线 -->
      <g v-else-if="baseType == 9" class="over">
        <polygon
          points="5,0.2 0,5 5,9.8 10,5"
          :fill="color"
          stroke-width="2"
        ></polygon>
        <!-- 95%+圆角 -->
        <rect
          x="0"
          y="0.4"
          width="5.30"
          height="0.8"
          :fill="color"
          transform="translate(5.5,1.2)rotate(-202)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="0"
          y="0.0"
          width="5.30"
          height="0.8"
          :fill="color"
          transform="translate(4.9,0.1)rotate(20)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="-0.15"
          y="9.1"
          width="5.2"
          height="0.8"
          :fill="color"
          transform="translate(0,0)rotate(23,5 10)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="4.95"
          y="9.1"
          width="5.2"
          height="0.8"
          :fill="color"
          rx="0.4"
          ry="0.4"
          transform="rotate(-23,5 10)"
        ></rect>
      </g>
      <!-- 对三角形 -->
      <g v-else-if="baseType == 6" class="over">
        <polygon points="0,0.4 5,5 10,0.4" :fill="color"></polygon>
        <polygon points="0,9.6 5,5 10,9.6" :fill="color"></polygon>
      </g>
      <!-- 对三角形＋短联线 -->
      <g v-else-if="baseType == 10" class="over">
        <polygon
          points="5,5 0,0.4 10,0.4"
          :fill="color"
          stroke-width="2"
        ></polygon>
        <polygon
          points="5,5 0,9.6 10,9.6"
          :fill="color"
          stroke-width="2"
        ></polygon>
        <rect
          x="6.9"
          y="4.7"
          width="5.2"
          height="0.8"
          :fill="color"
          rx="0.4"
          ry="0.4"
          transform="rotate(-23,5 10)"
        ></rect>
        <rect
          x="-2.1"
          y="4.7"
          width="5.2"
          height="0.8"
          :fill="color"
          transform="rotate(23,5 10)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="2.9"
          y="5.3"
          width="5.2"
          height="0.8"
          :fill="color"
          transform="rotate(23,5 10)"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          x="1.9"
          y="5.3"
          width="5.2"
          height="0.8"
          :fill="color"
          rx="0.4"
          ry="0.4"
          transform="rotate(-23,5 10)"
        ></rect>
      </g>
    </g>

    <g>
      <g v-if="topType == 0" class="vanish"></g>
      <!-- 有脉冲异常事件 -->
      <g v-if="topType == 3" class="lowgap">
        <rect
          v-if="baseType == 3 || baseType == 7"
          x="2"
          y="5.6"
          width="6"
          height="0.8"
          fill="#DA273D"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          v-else-if="baseType == 4 || baseType == 8"
          x="2"
          y="3.6"
          width="6"
          height="0.8"
          fill="#DA273D"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          v-else-if="baseType == 6 || baseType == 10"
          x="2"
          y="0"
          width="6"
          height="0.8"
          fill="#DA273D"
          rx="0.4"
          ry="0.4"
        ></rect>
        <rect
          v-else
          x="2"
          y="5"
          width="6"
          height="0.8"
          fill="#DA273D"
          rx="0.4"
          ry="0.4"
        ></rect>
      </g>
    </g>
    <g>
      <!-- 无干扰异常 -->
      <g v-if="mediumType == false" class="vanish"></g>
      <!-- 若是干扰异常信号 -->
      <g v-else-if="(mediumType == true) & (baseType != 1)" class="interrupt">
        <rect
          :x="(10 - k * 0.8) / 2"
          y="2"
          height="6"
          :width="k * 0.8"
          fill="#DA273D"
          :rx="(k * 0.8) / 2"
          :ry="0.6"
        ></rect>
      </g>
    </g>

    <rect
      v-if="enableWindows"
      @mouseenter="showInfo($event)"
      @mouseleave="hideInfo($event)"
      x="0"
      y="0"
      width="10"
      height="10"
      fill="transparent"
      :stroke="strokeColor"
      stroke-width="0.5"
    ></rect>
  </svg>
</template>

<script>
import { showToolTip, hideToolTip, format } from 'utils/base'
export default {
  name: 'RiverImage',
  props: {
    width: {
      type: Number,
    },
    height: {
      type: Number,
    },
    wangEnable: {
      type: Boolean,
      default: false,
    },
    /*
    top: {
        type: Boolean,
        default: true,
    },
    */
    /* 0为底层普通 1为特殊叠加 */
    type: {
      type: Number,
      default: 0,
    },
    baseType: {
      type: Number,
    },
    mediumType: {
      type: Boolean,
      default: false,
    },
    topType: {
      type: Number,
      default: 0,
    },
    color: {
      type: String
    },
    data: {
      type: Object
    },
    enableWindows: {
      type: Boolean,
      default: false
    },
    range: {
      type: Object
    }
  },
  computed: {
    k () {
      if (this.height <= this.width)
        return this.height / this.width
      else
        return 1
    }
  },
  data () {
    return {
      strokeColor: 'transparent'
    }
  },
  methods: {
    showInfo (event) {
      let index = this.data.index
      let info = this.data.info

      let ceil = info.segs[index]
      this.strokeColor = "black"

      this.$emit("showRect", {
        'id': info.id, 'avgFre': info.avgFre, 'avgBand': info.avgBand,
        'startTime': ceil.sTime, 'endTime': ceil.eTime
      })
      //console.log(ceil,(ceil.endTime-ceil.startTime)/1000)
      showToolTip({ x: event.x + 10, y: event.y - 20 }, `
                        <p>SignalID: ${info.id}</p>
                        <p>Center Frequency: ${info.avgFre.toFixed(2)}Mhz</p>
                        <p>BandWidth: ${info.avgBand.toFixed(2)}Mhz</p>
                        <p>----------------------------------</p>
                        <p>Avg dbm: ${ceil.avgDbm.toFixed(2)}</p>
                        <p>Avg snr: ${ceil.avgSnr.toFixed(2)}</p>
                        <p>Time: ${format(new Date(ceil.sTime * 1000), 0)}-${format(new Date(ceil.eTime * 1000), 0)}</p>
                    `, 7)
    },
    hideInfo (event) {
      this.$emit("hideRect")
      this.strokeColor = "transparent"
      hideToolTip()
    },
  }
}
</script>

<style>
.activeShow {
  pointer-events: auto;
}
</style>
