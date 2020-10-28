<template>
	<div class="container">
		<div class="image" ref="image" @mouseover="loadForeground" @mouseleave="cancelForeground">
			<img class="background" v-if="background.nextChunkOffset > 0" :src="background.src" />
			<img class="foreground" v-if="foreground.nextChunkOffset > 0 && layout" :src="foreground.src" :style="layout" />
		</div>
		<p>Loaded size: {{Math.floor((background.nextChunkOffset + foreground.nextChunkOffset) / 1000)}}kb</p>
	</div>
</template>

<script>
import Vue from 'vue';

export default {
	props: ['name'],
	data() {
		return {
			background: {
				blobParts: [],
				nextChunkOffset: 0,
				src: '',
			},
			foreground: {
				blobParts: [],
				nextChunkOffset: 0,
				src: '',
			},
			interval: null,
			layout: {}
		}
	},
	methods: {
		cancelForeground() {
			window.clearInterval(this.interval)
		},
		loadChunk(fileSrc, target, chunkSize = 5000) {
			const { blobParts, nextChunkOffset, } = this[target]
			const endChunk = nextChunkOffset + chunkSize;
			fetch(fileSrc, {
				headers: {
					'Range': `bytes=${nextChunkOffset}-${endChunk}`,
				},
			}).then(async response => {
				if (!response.ok) {
					throw Error('File complete');
				}
				return await response.blob();
			}).then(newBlob => {
				this[target].blobParts.push(newBlob);
				this[target].nextChunkOffset = endChunk + 1
				this[target].src = URL.createObjectURL(new Blob(blobParts, { type: "text/plain" }));
			}).catch(err => {
				console.log(err)
			});
		},
		loadBackgroundChunk () {
			this.loadChunk(`./assets/${this.name}/background.jpg`, 'background')
		},
		loadForeground() {
			this.interval = window.setInterval(() => {
				this.loadChunk(`./assets/${this.name}/crop.jpg`, 'foreground', 6000)
			}, 500)
		}
	},
	mounted () {
		fetch(`assets/${this.name}/coords.json`)
			.then(async response => await response.json())
			.then(({ top, left, width, height }) => {
				this.layout = `
					top: ${top}%;
					left: ${left}%;
					width: ${width}%;
					height: ${height}%;
				`;
			})
			this.loadBackgroundChunk();
	},
};
</script>
<style lang="scss" scoped>
.image,
.background {
	position: relative;
	width: 100%;
}
.foreground {
	position: absolute;
}
.has-borders {
	border: 1px solid white;
}
.is-hidden {
	opacity: 0;
}
</style>