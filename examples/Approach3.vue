<template>
    <Comparison :title="['Refinement 1', 'Targeted LOD']">
      <template v-slot:subtitle>Manipulating byte offsets to only load important details</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office, 130kb"
          src="./assets/targeted/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <Targeted :chunkSize="466 * 2" name="targeted" />
      </template>
    </Comparison>
</template>

<script>
import Comparison from "./Comparison.vue";
import ImageWithDetails from "./ImageWithDetails.vue";
import Targeted from "./techniques/Targeted.vue";
import Vue from 'vue';

export default {
  components: {
    Comparison,
    ImageWithDetails,
    Targeted,
  },
};
</script>
<style lang="scss" scoped>

</style>