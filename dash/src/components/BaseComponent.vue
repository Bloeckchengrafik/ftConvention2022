<template>
  <h1>FT Convention 2022</h1><br />
  <video ref="live" style="backgroundColor: #333"></video><br />
  <canvas id="imageSrc" alt="No Image" @click="beginDetection()" ref="out"></canvas><br />
  <div>
    <span>Buffers</span><br />
    <button @click="showBuf(source)">Source</button>
    <button @click="showBuf(crop)">Cropped</button>
    <button @click="showBuf(bw)">BW</button>
    <button @click="showBuf(edge)">Edges</button>
    <button @click="showBuf(blur)">Blur</button>
    <button @click="showBuf(thresh)">Threshold</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import cv from "@techstark/opencv-js";
import html2canvas from "html2canvas";

export default defineComponent({
  name: 'Base',
  async setup () {
    let media = await navigator.mediaDevices.getUserMedia({
      video: true
    })

    return {
        media,
        source: null as cv.Mat | null,
        bw: null as cv.Mat | null,
        edge: null as cv.Mat | null,
        blur: null as cv.Mat | null,
        thresh: null as cv.Mat | null,
        crop: null as cv.Mat | null,
    };
  },
  mounted() {
    let video: HTMLVideoElement = this.$refs.live as HTMLVideoElement;
    video.srcObject = this.media
    video.onloadedmetadata = () => {
        video.play();
    };
  },
  methods: {
    showBuf(buf: cv.Mat | null) {
      const stepOutTarget = this.$refs.out as HTMLCanvasElement
      cv.imshow(stepOutTarget, buf!)   
    },
    async beginDetection() {
      await this.doEdge();
    },
    async doEdge() {
      const screenshotTarget = this.$refs.live as HTMLElement;
      let canvasImage = await html2canvas(screenshotTarget).then((canvas) => {
          return canvas
      });

      let ctx = canvasImage.getContext('2d')!;
      let imgData = ctx.getImageData(0, 0, canvasImage.width, canvasImage.height);
      let src = cv.matFromImageData(imgData);
      let crop = src.clone()

      

      let bw = crop.clone()
      let edge = bw.clone()
      let blur = edge.clone()
      let thresh = blur.clone()
      
      cv.cvtColor(src, bw, cv.COLOR_RGB2GRAY)

      cv.Canny(bw, edge, 60, 120)

      cv.GaussianBlur(bw, blur, { width: 5, height: 5 }, 0)

      this.source = src
      this.bw = bw
      this.edge = edge
      this.blur = blur
      this.thresh = thresh

      this.showBuf(edge)
    }
  },
  components: {
  }
});
</script>

<style lang="sass">
video, img, canvas
    width: 427px
    height: 320px

button
  display: inline
</style>
