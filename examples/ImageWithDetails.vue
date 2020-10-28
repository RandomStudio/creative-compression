<template>
	<div class="container">
		<div class="image">
			<img ref="image" :src="src" />
			<slot></slot>
		</div>
		<p class="caption">{{caption}}</p>
	</div>
</template>

<script>
import SplitText from "./techniques/SplitText.vue";
import Vue from 'vue';

export default {
  props: ['src', 'caption'],
};
</script>
<style lang="scss" scoped>
.container,
.image {
	width: 100%;
}
img {
	width: 100%;
	margin: 0;
	display: block;
}
.caption {
	color: #333;
	margin: 0.5em 0;
	font-size: 14px;
}
</style>