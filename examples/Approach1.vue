<template>
  <div>
    <Comparison :title="['Direction 1', 'Object aware simplification']">
      <template v-slot:subtitle>Extracting key objects using Object Detection model, simplifying background with White Box Cartoonization ML model trained on anime dataset</template>
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
    <Comparison>
      <template v-slot:subtitle>Further processing the background layer, limiting it to 7 user defined colours</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office"
          src="./assets/vectorize_office_2/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <Vectorized name="vectorize_office_2"></Vectorized>
      </template>
    </Comparison>
    <Comparison>
      <template v-slot:subtitle>Applying heavy denoise filtering before tracing and limiting it to a palette of dominant colours extracted from image itself</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office"
          src="./assets/vectorize_office_3/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <Vectorized name="vectorize_office_3"></Vectorized>
      </template>
    </Comparison>
  </div>
</template>

<script>
import Comparison from "./Comparison.vue";
import ImageWithDetails from "./ImageWithDetails.vue";
import Vectorized from "./techniques/Vectorized.vue";
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