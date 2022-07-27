<template>
  <div :class="classSelect()">
    <img :src="imgPath" alt="" />
    <span>{{ message }}</span>
  </div>
</template>
 
<script>
export default {
  name: 'setTitle',
  props: {
    imgPath: String,
    message: String,
    type: {
      type: Number,
      default: 0,
    }
  },
  components: {
  },
  methods: {
    classSelect () {
      if (this.type == 0) {
        return 'setTitle'
      } else {
        return 'mainTitle'
      }
    }
  },
  data () {
    return {
      imga: require("assets/icons/test.png")
    }
  }
}
</script>
 
<style>
.setTitle {
  /*background-color: #fbfbfb;*/
  box-shadow: 0px 0.8px 0.2px 0.2px rgba(0, 0, 0, 0.1);
  font-size: 16px;
  height: 25px;
  line-height: 25px;
  color: #000000;
  font-weight: 300;
}
.setTitle img {
  width: 19px;
  height: 15px;
}
.mainTitle {
  line-height: 30px;
}
.mainTitle img {
  width: 24px;
  height: 20px;
}
</style>