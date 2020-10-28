<template>
	<div class="container">
		<div :class="`image ${hasBackground ? '' : 'no-background'}`" ref="image" @mouseover="loadForeground" @mouseleave="cancelForeground">
			<img class="background" v-if="background.nextChunkOffset > 0" :src="background.src" />
			<img class="foreground" v-if="foreground.nextChunkOffset > 0 && layout" :src="foreground.src" :style="layout" />
		</div>
		<p>Loaded size: {{Math.floor((background.nextChunkOffset + foreground.nextChunkOffset) / 1000)}}kb</p>
	</div>
</template>

<script>
import Vue from 'vue';

export default {
	props: {
		bgChunkSize: {
			type: Number,
			default: 5000,
		},
		hasBackground: {
			type: Boolean,
			default: true,
		},
		hasForeground: {
			type: Boolean,
			default: true,
		},
		name: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			background: {
				blobParts: [],
				isLoading: false,
				nextChunkOffset: 0,
				src: '',
			},
			foreground: {
				blobParts: [],
				isLoading: false,
				nextChunkOffset: 0,
				src: '',
			},
			interval: null,
			layout: {}
		}
	},
	methods: {
		cancelForeground() {
			console.log(this.interval)
			window.clearInterval(this.interval)
		},
		loadChunk(fileSrc, target, chunkSize) {
			const { blobParts, nextChunkOffset, } = this[target]
			const endChunk = nextChunkOffset + chunkSize;
			this[target].isLoading = true;
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
				this[target].isLoading = false;
			}).catch(err => {
				console.log(err)
			});
		},
		loadBackgroundChunk () {
			if (!this.hasBackground) {
				return;
			}
			this.loadChunk(`./assets/${this.name}/background.jpg`, 'background', this.bgChunkSize)
		},
		loadForeground() {
			if (!this.hasForeground || this.interval) {
				return;
			}
			this.interval = window.setInterval(() => {
				this.loadChunk(`./assets/${this.name}/crop.jpg`, 'foreground', 6000)
			}, 500)
		},
		loadLayout() {
			if (!this.hasForeground) {
				return;
			}
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
		}
	},
	mounted () {
		this.loadLayout();
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
.no-background {
	border: 1px solid #333;
	height: 45vw;
	max-height: 550px;
}
</style>