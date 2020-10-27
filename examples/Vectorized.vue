<template>
<div class="container">
	<div class="image" ref="image">
		<img class="background" :src="`./assets/${name}/background.${bgFormat ? bgFormat : 'jpg'}`" />
		<img
			v-for="overlay in overlays"
			:class="`overlay ${hasHiddenLayers ? 'is-hidden' : ''} ${hasBorders ? 'has-borders' : ''}`"
			:key="overlay.src"
			:src="overlay.src"
			:style="overlay.style"
		/>
	</div>
	<button @click="toggleLayers">Toggle layers</button>
	<button @click="toggleBorders">Toggle borders</button>
	</div>
</template>

<script>
import SplitText from "./SplitText.vue";
import Vue from 'vue';

export default {
  props: ['bgFormat', 'name'],
  data() {
	  return {
		  hasBorders: true,
		  hasHiddenLayers: false,
		  overlays: [],
	  }
  },
  methods: {
	  toggleBorders() {
		  this.hasBorders = !this.hasBorders
	  },
	  toggleLayers() {
		  this.hasHiddenLayers = !this.hasHiddenLayers
	  }
  },
  mounted () {
	fetch(`/assets/${this.name}/coords.json`)
		.then(async response => await response.json())
		.then(coords => {
			this.overlays = coords.map((coords, index) => {
				const [top, left, width, height] = coords;
				return {
					src: `/assets/${this.name}/crop${index}.jpg`,
					style: `
						top: ${top * 100}%;
						left: ${left * 100}%;
						width: ${width}%;
						height: ${height}%;
					`
				}
			})
		})	
  },
};
</script>
<style lang="scss" scoped>
.image,
.background {
	position: relative;
	width: 100%;
}
.overlay {
	position: absolute;
}
.has-borders {
	border: 1px solid white;
}
.is-hidden {
	opacity: 0;
}
</style>