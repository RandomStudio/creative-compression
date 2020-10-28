<template>
  <div>
    <Comparison :title="['Direction 2', 'Structured LOD']">
      <template v-slot:subtitle>Using the `Range: bytes=` content header to abort downloading of progressively encoding JPEGs early</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office, 130kb"
          src="./assets/focus_office/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <LOD :bgChunkSize="20000" :hasForeground="false" name="focus_office"></LOD>
      </template>
    </Comparison>
    <Comparison>
      <template v-slot:subtitle>By adjust range passed and concatenating returned blobs, we can control level of detail loaded programmatically. Below image loads 20kb each time a cursor hovers it.</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office, 130kb"
          src="./assets/focus_office_2/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <LOD :hasBackground="false" name="focus_office_2"></LOD>
      </template>
    </Comparison>
    <Comparison>
      <template v-slot:subtitle>Using object bounding box detection to create a 'focus/foreground' layer. Keeping background image bytes loaded to absolute minimum. Progressively loading foreground on user hover.</template>
      <template v-slot:before>
        <ImageWithDetails
          caption="JPEG of Office, 130kb"
          src="./assets/focus_office_3/normal.jpg"
        />
      </template>
      <template v-slot:after>
        <LOD name="focus_office_3"></LOD>
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