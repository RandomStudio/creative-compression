<template>
  <div class="page">
    <div class="header">
      <SplitText class="title" tag="h1">Random Studio</SplitText>
      <SplitText class="subtitle" tag="p">Creative Compression</SplitText>
    </div>
    <Approach1></Approach1>
    <Approach2></Approach2>
  </div>
</template>

<script>
import Approach1 from "./Approach1.vue";
import Approach2 from "./Approach2.vue";
import Approach3 from "./Approach3.vue";
import SplitText from "./techniques/SplitText.vue";
import Vue from "vue";

export default Vue.extend({
  components: {
    Approach1,
    Approach2,
    Approach3,
    SplitText,
  },
  data() {
    return {
      bundler: "Parcel",
    };
  },
});
</script>

<style lang="scss" scoped>
.header {
  color: white;
  background-color: black;
  width: 100vw;
  height: 95vh;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  place-content: center;
  place-items: center;
}

// Page styles
.title {
  margin: 0;
  font-size: 8vw;
}
.subtitle {
  margin: 0;
  font-size: 6vw;
}
</style>