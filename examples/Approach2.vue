<template>
  <div>
    <Comparison :title="['Direction 2', 'Structured LOD']">
      <template v-slot:subtitle></template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office"
          src="./assets/vectorize_office/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <Vectorized name="vectorize_office"></Vectorized>
      </template>
    </Comparison>
  </div>
</template>

<script>
import Comparison from "./Comparison.vue";
import ImageWithDetails from "./ImageWithDetails.vue";
import Vectorized from "./Vectorized.vue";
import Vue from "vue";

export default {
  components: {
    Comparison,
    ImageWithDetails,
    Vectorized
  },
};
</script>
<style lang="scss" scoped>
</style>