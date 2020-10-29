<template>
	<div class="container">
		<img class="image" :src="blobUrl" @click="doScan" @mouseleave="cancelInterval" />
		<p>Loaded size: {{size}}</p>
	</div>
</template>

<script>
import Vue from 'vue';

export default {
	props: {
		chunkSize: {
			type: Number,
			default: 5000,
		},
		name: {
			type: String,
			required: true,
		},
	},
	computed: {
		size() {
			return `${Math.floor((this.nextChunkOffset) / 1000)}kb`
		},
		src() {
			return `./assets/${this.name}/image.jpg`;
		},
	},
	data() {
		return {
			blobParts: [],
			blobUrl: '',
			isComplete: false,
			isLoading: false,
			interval: null,
			nextChunkOffset: 0,
			offsets: [],
			scan: 0,
		}
	},
	methods: {
		cancelInterval() {
			window.clearInterval(this.interval)
			this.interval = null;
		},
		// First scan fetches both image headers and scan data
		async doInitialScan() {
			const { start, scan, end } = this.offsets[0];
			const chunk = await this.loadChunk(start, end)
			const headers = chunk.slice(start, scan)
			const scanChunk = chunk.slice(scan)
			this.blobParts.push(headers);
			this.blobParts.push(scanChunk);

			this.blobUrl = URL.createObjectURL(new Blob(this.blobParts, { type: "text/plain" }));
			this.scan = 1;
		},
		async doScan() {
			const { start, scan, end } = this.offsets[this.scan];

			const topOffsetPercentage = 20;
			const bottomOffsetPercentage = 80;

			const scanRange = end - scan;
			const startOffset = Math.floor((scanRange / 100) * topOffsetPercentage);
			const endOffset = Math.floor((scanRange / 100) * bottomOffsetPercentage);

			const requestStart = start + startOffset;
			const requestEnd = start + endOffset;
			
			const headers = await this.loadChunk(start, scan - 1);
			const chunk = await this.loadChunk(requestStart, requestEnd);

			const startOffsetChunk = this.blobParts[1].slice(0, startOffset)
			const endOffsetChunk = this.blobParts[1].slice(endOffset)
		
			this.blobParts.push(headers);
			this.blobParts.push(startOffsetChunk);
			this.blobParts.push(chunk);
			this.blobParts.push(endOffsetChunk);

			this.blobUrl = URL.createObjectURL(new Blob(this.blobParts, { type: "text/plain" }));
			this.scan += 1;
		},
		loadChunk(start, end) {
			console.log(start, end)
			if (this.isLoading) {
				return;
			}

			this.isLoading = true;

			return new Promise((resolve) => {
				fetch(this.src, {
					headers: {
						'Range': `bytes=${start}-${end}`,
					},
				}).then(async response => {
					if (!response.ok) {
						throw Error(200);
					}
					return await response.blob();
				}).then(newBlob => {
					this.isLoading = false;
					resolve(newBlob);
				}).catch(err => {
					console.log(err)
					if (err === 200) {
						this.isComplete = true;
						return;
					}
				});
			})
		},
		loadImage () {
			if (this.interval) {
				return;
			}
			//this.interval = window.setInterval(this.loadChunk, 25);
		},
		async loadOffsets () {
			const response = await fetch(`assets/${this.name}/offsets.json`)
			this.offsets = await response.json();
		}
	},
	async mounted () {
		await this.loadOffsets()
		await this.doInitialScan()
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