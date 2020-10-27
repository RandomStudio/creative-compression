<template>
    <Comparison>
      <template v-slot:title>Direction 1: Abstract Tesselation</template>
      <template v-slot:before>
		  <ImageWithDetails caption="JPEG of Office" src="./masks_office/normal.jpg" />
	  </template>
      <template v-slot:after>
		  <ImageWithDetails caption="JPEG of Office" src="./masks_office/normal.jpg" />
		</template>
    </Comparison>
</template>

<script>
import Comparison from "./Comparison.vue";
import ImageWithDetails from "./ImageWithDetails.vue";
import Vue from 'vue';

export default {
  components: {
	Comparison,
	ImageWithDetails,
  },
};
</script>
<style lang="scss" scoped>

</style>