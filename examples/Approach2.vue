<template>
  <div>
    <Comparison :title="['Direction 2', 'Structured LOD']">
      <template v-slot:subtitle></template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office"
          src="./assets/focus_office/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <LOD name="focus_office"></LOD>
      </template>
    </Comparison>
  </div>
</template>

<script>
import Comparison from "./Comparison.vue";
import ImageWithDetails from "./ImageWithDetails.vue";
import LOD from "./techniques/LOD.vue";
import Vue from "vue";

export default {
  components: {
    Comparison,
    ImageWithDetails,
    LOD
  },
};
</script>
<style lang="scss" scoped>
</style>