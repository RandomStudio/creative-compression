<template>
    <div class="comparison">
      <SplitText class="title" tag="h2">
        <slot name="title"></slot>
      </SplitText>
      <div class="left"><slot name="before"></slot></div>
      <div class="right"><slot name="after"></slot></div>
    </div>
</template>

<script>
import SplitText from "./SplitText.vue";
import Vue from 'vue';

export default {
  components: {
    SplitText,
  },
  data() {
    return {
      content: '',
      value: 'yes'
    }
  },
  mounted() {
    this.content = this.$el.textContent;
  }
};
</script>
<style lang="scss" scoped>
.comparison {
  display: flex;
  flex-direction: row;
  max-width: 1140px;
  margin: 0 auto;
  padding: 40px 20px 60px;
  justify-content: center;
  flex-wrap: wrap;
}
.title {
  text-align: center;
  margin: 0 auto;
  width: 70%;
} 
.left,
.right {
  width: calc(50% - 24px);
  margin: 12px;
}
</style>