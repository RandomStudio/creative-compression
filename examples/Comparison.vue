<template>
    <div class="comparison">
      <SplitText class="title" tag="h2" v-for="line in title" :key="line">{{line}}</SplitText>
      <p class="subtitle"><slot name="subtitle"></slot></p>
      <div class="left"><slot name="before"></slot></div>
      <div class="right"><slot name="after"></slot></div>
    </div>
</template>

<script>
import SplitText from "./SplitText.vue";
import Vue from 'vue';

export default {
  props: ['title'],
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
  padding: 0 20px 60px;
  justify-content: center;
  flex-wrap: wrap;
}
.title {
  text-align: center;
  margin: 0 auto;
  width: 75%;
  font-size: 32px;
} 
.title:first-of-type {
  margin-top: 12px;
}
.title + .subtitle {
  margin-top: 12px;
}
.subtitle {
  text-align: center;
  width: 50%;
  margin: 0 25% 12px;
}
.left,
.right {
  width: calc(50% - 24px);
  margin: 12px;
}
</style>