<template lang="pug">
.v-container.pa-4
  canvas#container
  // Main content
  v-layout(col)
    //- v-data-table
    //- c-grid.demo-grid(:data='records' :options="{parentElement: document.getElemenById('container')}")
    //-   // define checkbox
    //-   c-grid-check-column(field='check', width='50', height='25')
    //-     c-grid-column(field='personid', width='85', height='25') ID
    //-     // multiple header
    //-   c-grid-column-group(caption='Name')
    //-     c-grid-input-column(field='fname', width='20%', min-width='150', height='25')
    //-       | First Name
    //-     c-grid-input-column(field='lname', width='20%', min-width='150', height='25')
    //-       | Last Name
    //-     // button
    //-   c-grid-button-column(
    //-     caption='SHOW REC',
    //-     width='120',
    //-     @click='onClickRecord'
    //-   )
    //-     .grid-sample

    v-stage#container(
      ref='stage',
      :config='configKonva',
      @mousedown='handleStageMouseDown',
      @touchstart='handleStageMouseDown',
      @wheel='onWheel($event)'
    )
      v-layer(ref='layer')
        v-rect(
          v-for='item in rectangles',
          :key='item.id',
          :config='item',
          @transformend='handleTransformEnd',
          @dragstart='dragstartRect',
          @dragmove='dragmoveRect',
          @dragend='dragendRect',
          :ref='item.name'
        )
        v-transformer(ref='transformer')
  v-layout.text-center(column, justify-center, align-center)
    v-flex.pt-4
      .caption
        router-link(to='/gantt') {{ $t("home.privacy") }}
    v-progress-linear(color='light-blue', height='10', value='10', striped)
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import Component from 'vue-class-component'
import { i18n } from '@/plugins/i18n'
import { namespace } from 'vuex-class'

import Konva from 'konva'
import VueKonva from 'vue-konva'
Vue.use(VueKonva)

import vueCheetahGrid from 'vue-cheetah-grid'
Vue.use(vueCheetahGrid)

const AppStore = namespace('AppStore')
const SnackbarStore = namespace('SnackbarStore')

@Component({
  components: {},
})
export default class Home extends Vue {
  @SnackbarStore.Mutation setSnackbarError!: (error: string) => void

  records = [
    {
      personid: 1,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 2,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 3,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 4,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 5,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 6,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 7,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 8,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
    {
      personid: 9,
      fname: 'Charlotte',
      lname: 'Foster',
      email: 'abc@def.gh',
      birthday: '2001-01-12T21:00.00.000Z',
    },
  ]
  onClickRecord(rec: any) {
    alert(JSON.stringify(rec))
  }

  rectangles = [
    {
      rotation: 0,
      x: 25,
      y: 25,
      width: 225,
      height: 25,
      scaleX: 1,
      scaleY: 1,
      name: 'rect1',
      fill: 'white',
      stroke: '#ddd',
      strokeWidth: 1,
      shadowColor: 'black',
      shadowBlur: 2,
      shadowOffset: { x: 1, y: 1 },
      shadowOpacity: 0.4,
      draggable: true,
    },
    {
      rotation: 0,
      x: 150,
      y: 150,
      width: 225,
      height: 25,
      scaleX: 1,
      scaleY: 1,
      fill: 'green',
      name: 'rect2',
      stroke: '#ddd',
      strokeWidth: 1,
      shadowColor: 'black',
      shadowBlur: 2,
      shadowOffset: { x: 1, y: 1 },
      shadowOpacity: 0.4,
      draggable: true,
    },
  ]
  selectedShapeName = ''

  handleTransformEnd(e: any) {
    // shape is transformed, let us save new attrs back to the node
    // find element in our state
    // const rect = (this.$refs['rect2'] as any)[0].getNode()

    // update the state
    console.log(e.target)
    e.target.width(
      Math.round((e.target.width() * e.target.scale().x) / this.blockSnapSize) *
        this.blockSnapSize
    )
    e.target.x(
      Math.round(e.target.x() / this.blockSnapSize) * this.blockSnapSize
    )
    this.shadowRectangle.width(e.target.width())
    // set scale to normal value
    e.target.scaleX(1)

    // Disable scale by y axis
    e.target.scaleY(1)
    e.target.height(this.blockSnapSize)

    // Disable rotation
    e.target.rotation(0)
  }
  handleStageMouseDown(e: any) {
    // clicked on stage - clear selection
    if (e.target === e.target.getStage()) {
      this.selectedShapeName = ''
      this.updateTransformer()
      return
    }

    // clicked on transformer - do nothing
    const clickedOnTransformer =
      e.target.getParent().className === 'Transformer'
    if (clickedOnTransformer) {
      return
    }

    // find clicked rect by its name
    const name = e.target.name()
    const rect = this.rectangles.find((r) => r.name === name)
    if (rect) {
      this.selectedShapeName = name
    } else {
      this.selectedShapeName = ''
    }
    this.updateTransformer()
  }

  updateTransformer() {
    // here we need to manually attach or detach Transformer node
    const transformerNode = (this.$refs.transformer as any).getNode()
    console.log(this.selectedShapeName)

    const stage = transformerNode.getStage()
    const { selectedShapeName } = this

    const selectedNode = stage.findOne('.' + selectedShapeName)
    // do nothing if selected node is already attached
    if (selectedNode === transformerNode.node()) {
      return
    }

    if (selectedNode) {
      // attach to another node
      transformerNode.nodes([selectedNode])
    } else {
      // remove transformer
      transformerNode.nodes([])
    }
  }

  configKonva = {
    width: 900,
    height: 800,
    draggable: true,
    container: 'container',
    zoomable: true,
  }

  width = window.innerWidth
  height = window.innerHeight
  shadowOffset = 20
  tween = null
  blockSnapSize = 25

  shadowRectangle: any
  leftRectangle: any
  rightRectangle: any
  stage: any
  layer: any
  scaleBy = 2.5

  dragstartRect(e: any) {
    this.shadowRectangle.width(e.target.width())
    this.shadowRectangle.show()
    this.shadowRectangle.moveToTop()
    e.target.moveToTop()
  }

  dragmoveRect(e: any) {
    // console.log(rectangle.attrs())
    this.shadowRectangle.position({
      x: Math.round(e.target.x() / this.blockSnapSize) * this.blockSnapSize,
      y: Math.round(e.target.y() / this.blockSnapSize) * this.blockSnapSize,
    })
    this.stage.batchDraw()
  }

  dragendRect(e: any) {
    e.target.position({
      x: Math.round(e.target.x() / this.blockSnapSize) * this.blockSnapSize,
      y: Math.round(e.target.y() / this.blockSnapSize) * this.blockSnapSize,
    })
    this.stage.batchDraw()
    this.shadowRectangle.hide()
  }

  newRectangle(x: number, y: number, layer: Konva.Layer, stage: Konva.Stage) {
    let rectangle = new Konva.Rect({
      x: x,
      y: y,
      width: this.blockSnapSize * 6,
      height: this.blockSnapSize * 3,
      fill: '#fff',
      stroke: '#ddd',
      strokeWidth: 1,
      shadowColor: 'black',
      shadowBlur: 2,
      shadowOffset: { x: 1, y: 1 },
      shadowOpacity: 0.4,
      draggable: true,
    })
    layer.add(rectangle)
  }

  animationDuration = 300 //in miliseconds
  startScale = 0
  startTime = 0
  endScale = 100
  startPosX = 0
  endPosX = 0
  startPosY = 0
  endPosY = 0

  onWheelAnimate(currentTime: number) {
    if (!this.startTime) this.startTime = Date.now()
    var elapsedTime = currentTime - this.startTime + 0.1
    if (elapsedTime < this.animationDuration) {
      let currentValue =
        this.startScale +
        (elapsedTime / this.animationDuration) *
          (this.endScale - this.stage.scaleX())
      //set your field value to currentValue here with something like document.getElemenById...
      //call the next animation frame
      // console.log(currentValue);
      this.stage.scale({ x: currentValue, y: currentValue })
      // let pointer = this.stage.getPointerPosition()

      // let mousePointTo = {
      //   x: (pointer.x - this.stage.x()) / this.stage.scaleX(),
      //   y: (pointer.y - this.stage.y()) / this.stage.scaleY(),
      // }
      // // console.log(mousePointTo, pointer);
      // var newPos = {
      //   x: pointer.x - mousePointTo.x * currentValue,
      //   y: pointer.y - mousePointTo.y * currentValue,
      // }
      // this.newRectangle(mousePointTo.x * currentValue, mousePointTo.y * currentValue , this.layer, this.stage);

      // console.log("newPos", newPos);
      this.stage.position({
        x:
          (elapsedTime / this.animationDuration) *
          (this.endPosX - this.stage.x()),
        y:
          (elapsedTime / this.animationDuration) *
          (this.endPosY - this.stage.y()),
      })
      setTimeout(() => this.onWheelAnimate(Date.now()), 1)
    }
  }

  onWheel(e: WheelEvent) {
    console.log(Date.now())
    this.startTime = 0
    this.startScale = this.stage.scaleX()
    console.log(this.startScale)
    let pointer = this.stage.getPointerPosition()
    this.endScale =
      e.deltaY < 0
        ? this.startScale * this.scaleBy
        : this.startScale / this.scaleBy
    this.startPosX = pointer.x - this.stage.x()
    this.endPosX = this.stage.width() / 2
    this.startPosY = pointer.y - this.stage.y()
    this.endPosY = this.stage.height() / 2
    console.log(this.startPosX, this.startPosY)
    console.log(this.endPosX, this.endPosY)
    this.newRectangle(this.startPosX, this.startPosY, this.layer, this.stage)
    this.newRectangle(this.endPosX, this.endPosY, this.layer, this.stage)

    // this.stage.scale({x: this.endScale, y: this.endScale});

    console.log('->', this.endScale)
    this.onWheelAnimate(Date.now())

    this.stage.position({
      x: this.stage.x(),
      y: this.stage.y(),
    })
    this.stage.scale({ x: this.endScale, y: this.endScale })
    this.stage.position({
      x: -this.stage.x(),
      y: -this.stage.y(),
    })
  }

  mounted() {
    this.shadowRectangle = new Konva.Rect({
      x: 0,
      y: 0,
      width: this.blockSnapSize * 9,
      height: this.blockSnapSize,
      fill: '#FF7B17',
      opacity: 0.6,
      stroke: '#CF6412',
      strokeWidth: 3,
      dash: [20, 2],
    })

    this.stage = (this.$refs.stage as any).getNode()

    this.stage.on('click tap', (e: Event) => {
      if (e.target === this.stage) {
        document.body.style.cursor = 'cursorurl'
        this.stage.batchDraw()
      }
    })

    var gridLayer = new Konva.Layer()
    var padding = this.blockSnapSize
    console.log(this.width, padding, this.width / padding)
    for (var i = 0; i < this.width / padding; i++) {
      gridLayer.add(
        new Konva.Line({
          points: [
            Math.round(i * padding) + 0.5,
            0,
            Math.round(i * padding) + 0.5,
            this.height,
          ],
          stroke: '#999',
          strokeWidth: 1,
        })
      )
    }

    gridLayer.add(new Konva.Line({ points: [0, 0, 10, 10] }))
    for (var j = 0; j < this.height / padding; j++) {
      gridLayer.add(
        new Konva.Line({
          points: [
            0,
            Math.round(j * padding),
            this.width,
            Math.round(j * padding),
          ],
          stroke: j % 4 == 0 ? '#cecece' : '#fff',
          strokeWidth: 1,
        })
      )
    }

    this.layer = (this.$refs.layer as any).getNode()
    this.shadowRectangle.hide()
    this.layer.add(this.shadowRectangle)
    this.newRectangle(
      this.blockSnapSize * 3,
      this.blockSnapSize * 3,
      this.layer,
      this.stage
    )
    this.newRectangle(
      this.blockSnapSize * 10,
      this.blockSnapSize * 3,
      this.layer,
      this.stage
    )
    this.newRectangle(
      this.blockSnapSize * 10,
      this.blockSnapSize * 3,
      this.layer,
      this.stage
    )

    this.stage.add(gridLayer)
    this.stage.add(this.layer)
  }
}
</script>

<style scoped>
html {
  height: 100%;
}
body {
  height: calc(100% - 100px);
}
.contents {
  padding: 30px;
  box-sizing: border-box;
}
.demo-grid {
  width: 500px;
  height: 300px;
  box-sizing: border-box;
  border: solid 1px #ddd;
}
.demo-grid.large {
  height: 500px;
}
.demo-grid.middle {
  height: 300px;
}
.demo-grid.small {
  height: 240px;
}
.log {
  /* width: 100%; */
  height: 80px;
  background-color: #f5f5f5;
}
.hljs {
  tab-size: 4;
}
</style>
