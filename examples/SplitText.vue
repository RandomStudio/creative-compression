<template>
    <component :is="tag" :content="content" class="split-text" ref="text">
      <slot></slot>
    </component>
</template>

<script>
import Vue from 'vue';

export default {
  props: ['tag'],
  data() {
    return {
      content: '',
      value: 'yes'
    }
  },
  mounted() {
    this.content = this.$el.textContent;
  }
};
</script>
<style lang="scss" scoped>

// Handles the effect itself
.split-text {
  --line-height: 1.4;
  --line: (1em * var(--line-height));
  line-height: var(--line-height);
  font-family: 'Times New Roman', Times, serif;
  position: relative;
  background: repeating-linear-gradient(to bottom, currentColor 0, currentColor calc(0.55 * var(--line)), transparent calc(0.551 * var(--line)), transparent calc(1 * var(--line)));
  background-clip: text;
  -webkit-text-fill-color: transparent;

  &::after {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    font-family: Palatino Linotype, Comic Sans;
    background: repeating-linear-gradient(to bottom, transparent 0, transparent calc(0.55 * var(--line)), currentColor calc(0.551 * var(--line)), currentColor calc(1 * var(--line)));
    background-clip: text;
    content: attr(content);
  }
}
</style>