<template>
  <Suspense>
    <BaseComponent></BaseComponent>
  </Suspense>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import BaseComponent from "@/components/BaseComponent.vue";


export default defineComponent({
  name: 'App',
  components: {
    BaseComponent
  }
});
</script>

<style lang="css">
#app {
  color: #fff;
  font-family: 'Courier New', Courier, monospace;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>
