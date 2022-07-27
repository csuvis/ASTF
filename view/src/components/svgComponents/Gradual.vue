<template>
    <svg width="0px" height="0px">
    <!-- 每个矩形 的前后有2种颜色 加上自己本身 因此用一个三进制编码-->
    <!-- 前 中 后 浅:0 中:1 深:2 -->
    <!-- '#8cd6eb',"#52c1e2",'#23a6cd' -->
    <!--       #6fcbe6     #35b6dd -->
    <!-- 222 = 2*9+2*3+2 = 26 -->
        <!-- 上中下 -->
        <!--浅深浅:020  
        <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :style="`stop-color:${gradColor[2]};stop-opacity:1`" />
            <stop :offset="startGrad" :style="`stop-color:${gradColor[4]};stop-opacity:1`" />
            <stop :offset="endGrad" :style="`stop-color:${gradColor[4]};stop-opacity:1`" />
            <stop offset="100%" :style="`stop-color:${gradColor[2]};stop-opacity:1`" />
        </linearGradient>
        -->
        <defs>
        <linearGradient v-for="(_,index) in (new Array(27))" :key="'Gradient'+index" :id="`grad${index}`" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :style="`stop-color:${gradColor[getFirst(index)]};stop-opacity:1`" />
            <stop :offset="startGrad" :style="`stop-color:${gradColor[getMedium(index)]};stop-opacity:1`" />
            <stop :offset="endGrad" :style="`stop-color:${gradColor[getMedium(index)]};stop-opacity:1`" />
            <stop offset="100%" :style="`stop-color:${gradColor[getLast(index)]};stop-opacity:1`" />
        </linearGradient>
        </defs>
    </svg>

</template>
 
<script>
import config from 'api/config'
export default {
 name: 'Gradual',
 props: {
 },
 computed: {
     startGrad() {
         return `${this.gradLine}%`
     },
     endGrad() {
         return `${100-this.gradLine}%`
     }
 },
 methods: {
     getFirst(index) { //5
         let medium = parseInt(index/3)%3 //1
         let start = parseInt(index/9)%3  //0
         return medium+start
     },
     getMedium(index) {
         let medium = parseInt(index/3)%3 //
         return medium*2
     },
     getLast(index) {
         let medium = parseInt(index/3)%3
         let last = index%3 //1
         return medium+last
     }
 },
 data () {
 return {
     gradLine: 25,
     gradColor: config.gradColor
  }
 },
}
</script>
 
<style>
 
</style>