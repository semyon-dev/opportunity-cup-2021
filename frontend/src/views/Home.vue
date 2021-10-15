<template lang="pug">
v-layout
  //- show content only if data is loaded. Unless show progress-circular
  v-layout(v-if='loaded') 
    #navigation
      svg#navigation-svg(
        @mousedown='startDrag($event)',
        @mousemove='drag($event)',
        @mouseleave='endDrag($event)',
        @mouseup='endDrag($event)',
        width='400'
      )
        g(transform='translate(0, 0)')
          rect.draggable(
            x='5',
            y='0',
            width='40',
            height='50',
            fill='rgba(0, 0, 0, 0.1)',
            stroke='rgba(0, 0, 0, 0.5)',
            stroke-width='2'
          )
    #svg-root 
    pre#str
    canvas#canvas
    v-dialog(
      v-model='dialog',
      width='500',
      transition='dialog-bottom-transition'
    )
      template(v-slot:activator='{ on }')
      v-card
        v-toolbar(color='primary', dark) Изменить длину задачи
        v-card-text.pa-8.text-h5 Введите количество дней, на которое нужно перенести задачу
        v-divider
        v-card-actions
          v-text-field(
            placeholder='Количество дней',
            v-model='offsetCosts',
            small
          )
          v-spacer
          v-btn(color='primary', dark, @click='calcCosts') Рассчитать
    #contextmenu
      v-btn(dark, x-small, @click='dialog = true') Изменить длину задачи
  v-layout(v-else)
    v-progress-circular(indeterminate, :width='7', :size='70')
</template>
<script lang="ts" defer>
import Vue from 'vue'
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
const AppStore = namespace('AppStore')
const SnackbarStore = namespace('SnackbarStore')

import { SVGGantt, CanvasGantt, StrGantt } from 'gantt'

import { getTasks, setOffset } from '@/utils/api'

@Component({})
export default class GanttSimple extends Vue {
  @AppStore.State limit!: number
  @SnackbarStore.Mutation setSnackbarSuccess!: (message: string) => void

  selectedElement = null
  svg = null
  svgRoot = null
  offset = { x: 0, y: 0 }
  contextMenu = null

  // Navigation methods section

  getMousePosition(evt: Event) {
    let CTM = this.svg.getScreenCTM()
    return {
      x: (evt.clientX - CTM.e) / CTM.a,
      y: (evt.clientY - CTM.f) / CTM.d,
    }
  }

  updateSVGPosition(x: number, y: number) {
    // updates #svg-root position based on naviagtion rectangle position
    this.svgRoot.style.position = 'absolute'
    this.svgRoot.style.left = (-x * this.svgRoot.getBBox().width) / 450
    // this.svgRoot.style.top = (-y * this.svgRoot.getBBox().height) / 150
  }

  startDrag(evt: Event) {
    if (this.svg === null) this.svg = evt.target
    if (this.svgRoot === null)
      this.svgRoot = (
        document.getElementById('svg-root') as HTMLElement
      ).children[0]

    if (evt.target.classList.contains('draggable')) {
      this.selectedElement = evt.target
      this.offset = this.getMousePosition(evt)
      this.offset.x -= parseFloat(
        this.selectedElement.getAttributeNS(null, 'x')
      )
      // this.offset.y -= parseFloat(this.selectedElement.getAttributeNS(null, 'y'))
    }
  }
  drag(evt: Event) {
    if (this.selectedElement) {
      evt.preventDefault()
      var coord = this.getMousePosition(evt)
      this.selectedElement.setAttributeNS(null, 'x', coord.x - this.offset.x)
      // this.selectedElement.setAttributeNS(null, 'y', coord.y - this.offset.y)
      this.updateSVGPosition(coord.x - this.offset.x, coord.y - this.offset.y)
    }
  }
  endDrag(evt: Event) {
    this.selectedElement = null
  }

  // Tasks processing section

  responseTasks = []
  tasks = []
  loaded = false
  dialog = false
  offsetCosts = ''
  idCosts = 0

  async processTasks() {
    try {
      const tasks = await getTasks()
      interface link {
        target: number
        type: 'FS' | 'FF' | 'SS' | 'SF'
      }
      interface taskInterface {
        id: number
        text: string
        start: string
        end: string
        duration: number
        type: string
        dependentOn: number[]
        percent: number
        user: string
        style: Object
        label: string
        parentId: number
        links: link[]
      }
      console.log(tasks)
      this.responseTasks = tasks
      tasks.every((element) => {
        // console.log(element, Object.keys(element))
        let task: taskInterface = {}

        task['label'] = 'task from the table'
        task['user'] = 'origin dev'
        task['percent'] = 1
        task['parentId'] = element['_id']

        if (Object.keys(element).includes('_id')) task['id'] = element['_id']
        task['text'] = task.id.toString()

        if (Object.keys(element).includes('start'))
          task['start'] = new Date(element['start'])

        if (Object.keys(element).includes('duration'))
          task['end'] = new Date(
            Date.parse(element['start']) + element['duration'] * 3600 * 1000
          )

        if (!element['duration']) {
          task['type'] = 'milestone'
          task['duration'] = 100
        } else task['type'] = 'task'

        let dependOn: link[] = []

        if (Object.keys(element).includes('predecessors'))
          element['predecessors'].forEach((predecessor) => {
            let type = ''
            if (Object.keys(predecessor).includes('X')) {
              type += predecessor['X'] == 'Н' ? 'S' : 'F'
              type += predecessor['Y'] == 'Н' ? 'S' : 'F'
              dependOn.push({
                target: predecessor['n'],
                type: type,
              })
              if (
                Object.keys(predecessor).includes('m') &&
                parseInt(predecessor['m']) > 0
              ) {
                task['end'] = new Date(
                  Date.parse(element['start']) +
                    element['duration'] * 3600 * 1000 +
                    parseInt(predecessor['m']) * 3600 * 1000
                )
                task['percent'] = 1 - predecessor['m'] / element['duration']
              }
            }
          })
        task['links'] = dependOn
        // console.log(task)
        this.tasks.push(task)
        if (this.tasks.length > this.limit) return false
        return true
      })
      console.log('returned')
      console.log(this.tasks)
      this.loaded = true
    } catch (err) {
      console.log(err)
    }
  }

  showContextMenu(e: Event) {
    this.contextMenu.style.visibility = 'visible'
    this.contextMenu.style.left = e.x + 'px'
    console.log(e, e.x, this.contextMenu.style.left)
    this.contextMenu.style.top = e.y + 'px'
    let id: string = ''
    if (e.target.tagName === 'polygon')
      id = e.target.parentElement.children[1].attributes[1].value
    else id = e.target.parentElement.children[4].children[0].attributes[1].value
    this.idCosts = parseInt(id)
  }

  calcCosts() {
    setOffset(this.idCosts, this.offsetCosts).then((response) => {
      this.setSnackbarSuccess(
        'Количество сдвигов: ' + response.count + ' и цена: ' + response.cost
      )
    })
  }

  hideContextMenu(e: Event) {
    this.contextMenu.style.visibility = 'hidden'
  }

  colorGradient(fadeFraction, rgbColor1, rgbColor2, rgbColor3) {
    interface rgb {
      red: number
      green: number
      blue: number
    }
    let color1: rgb = rgbColor1
    let color2: rgb = rgbColor2
    let fade = fadeFraction * 2

    // Find which interval to use and adjust the fade percentage
    if (fade >= 1) {
      fade -= 1
      color1 = rgbColor2
      color2 = rgbColor3
    }

    let diffRed: number = color2.red - color1.red
    let diffGreen: number = color2.green - color1.green
    let diffBlue: number = color2.blue - color1.blue

    let gradient = {
      red: parseInt(Math.floor(color1.red + diffRed * fade), 10),
      green: parseInt(Math.floor(color1.green + diffGreen * fade), 10),
      blue: parseInt(Math.floor(color1.blue + diffBlue * fade), 10),
    }
    return (
      'rgb(' + gradient.red + ',' + gradient.green + ',' + gradient.blue + ')'
    )
  }

  mounted() {
    document.addEventListener(
      'contextmenu',
      function (event) {
        event.preventDefault()
      },
      true
    )
    this.processTasks().then(() => {
      let svgGantt = new SVGGantt('#svg-root', this.tasks, {
        viewMode: 'month',
      })

      let canvasGantt = new CanvasGantt('#canvas', this.tasks, {
        viewMode: 'month',
      })

      let strGantt = new StrGantt(this.tasks, {
        viewMode: 'month',
      })
      let body = strGantt.render()
      this.contextMenu = document.getElementById('contextmenu')
      document
        .getElementById('svg-root')
        .addEventListener('mousedown', this.hideContextMenu)
      let c1 = { red: 19, green: 233, blue: 200 }
      let c2 = { red: 255, green: 235, blue: 20 }
      let c3 = { red: 255, green: 0, blue: 0 }
      let ganttBars = document.getElementsByClassName('gantt-bar')
      for (let i = 0; i < ganttBars.length; i++) {
        ganttBars[i].addEventListener('contextmenu', this.showContextMenu)
        if (ganttBars[i].children.length > 2)
          ganttBars[i].children[2].style.fill = 'rgba(0, 0, 0, .1)'
        if (ganttBars[i].children.length > 3)
          ganttBars[i].children[3].style.fill = this.colorGradient(
            Math.random(),
            c3,
            c2,
            c1
          )
      }
    })
  }

  @Watch('limit')
  onLimitChange() {
    this.loaded = false
    if (this.tasks.length > this.limit) this.tasks = []
    this.$router.go(this.$router.currentRoute)
  }
}
</script>
<style>
#navigation {
  position: fixed;
  background: rgba(0, 0, 0, 0.27) !important;
  right: 15px;
  bottom: 15px;
  width: 400px;
  height: 50px;
  border-radius: 3px;
  z-index: 999999;
}
.static {
  cursor: not-allowed;
}
.draggable {
  cursor: move;
}
#svg-root {
  position: absolute !important;
}
#canvas {
  width: 200px !important;
  height: 100px !important;
}
#contextmenu {
  position: fixed;
  visibility: hidden;
}
</style>