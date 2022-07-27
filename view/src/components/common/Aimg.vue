<template>
  <div class="aimg">
    <a href="###">
      <img
        :src="imgPath"
        alt=""
        :width="width - 6 + 'px'"
        :height="height - 10 + 'px'"
        @click="outClick()"
      />
    </a>
  </div>
</template>
 
<script>
export default {
  name: 'Aimg',
  props: {
    imgPath: String,
    width: {
      type: Number,
      default: 30,
    },
    height: {
      type: Number,
      default: 30,
    },
  },
  components: {
  },
  methods: {
    outClick () {
      this.$emit("imgClick")
    },
  },
  data () {
    return {
    }
  }
}
</script>
 
<style>
.aimg {
  display: inline-block;
}
</style>