<template lang="pug">
v-layout
  //- show content only if data is loaded. Unless show progress-circular
  v-layout(v-if='loaded') 
    #navigation
      pre#str
      svg(
        @mousedown='startDrag($event)',
        @mousemove='drag($event)',
        @mouseleave='endDrag($event)',
        @mouseup='endDrag($event)'
      )
        rect.draggable(
          x='18',
          y='5',
          width='20',
          height='12',
          fill='rgba(0, 0, 0, 0)',
          stroke='#000',
          stroke-width='2'
        )
    #svg-root 
    canvas#canvas
    v-dialog(v-model="dialog" width="500" transition="dialog-bottom-transition")
      template(v-slot:activator="{ on }")
      v-card()
        v-toolbar(
          color="primary"
          dark) Изменить длину задачи
        v-card-text.pa-8.text-h5 Введите количество дней, на которое нужно перенести задачу
        v-divider
        v-card-actions
          v-text-field(placeholder="Количество дней" v-model="offsetCosts" small)
          v-spacer
          v-btn(
            color="primary"
            dark
            @click="calcCosts") Рассчитать
    #contextmenu
      v-btn(dark x-small @click="dialog=true") Изменить длину задачи
  v-layout(v-else)
    v-progress-circular(indeterminate, :width='7', :size='70')
</template>
<script lang="ts" defer>
import Vue from 'vue'
import Component from 'vue-class-component'
import { namespace } from 'vuex-class'
const SnackbarStore = namespace('SnackbarStore')

import { SVGGantt, CanvasGantt, StrGantt } from 'gantt'

import { getTasks, setOffset } from '@/utils/api'

@Component({})
export default class GanttSimple extends Vue {
  @SnackbarStore.Mutation setSnackbarSuccess!: (message: string) => void

  data = [
    {
      id: 1,
      type: 'group',
      text: '1 Waterfall model',
      start: new Date('2018-10-10T09:24:24.319Z'),
      end: new Date('2018-12-12T09:32:51.245Z'),
      percent: 0.71,
      links: [],
    },
    {
      id: 11,
      parent: 1,
      text: '1.1 Requirements',
      start: new Date('2018-10-21T09:24:24.319Z'),
      end: new Date('2018-11-22T01:01:08.938Z'),
      percent: 0.29,
      links: [
        {
          target: 12,
          type: 'FS',
        },
      ],
    },
    {
      id: 12,
      parent: 1,
      text: '1.2 Design',
      start: new Date('2018-11-05T09:24:24.319Z'),
      end: new Date('2018-12-12T09:32:51.245Z'),
      percent: 0.78,
    },
  ]

  selectedElement = null
  svg = null
  svgRoot = null
  offset = { x: 0, y: 0 }
  contextMenu = null

  getMousePosition(evt: Event) {
    let CTM = this.svg.getScreenCTM()
    return {
      x: (evt.clientX - CTM.e) / CTM.a,
      y: (evt.clientY - CTM.f) / CTM.d,
    }
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
      this.offset.y -= parseFloat(
        this.selectedElement.getAttributeNS(null, 'y')
      )
    }
  }
  drag(evt: Event) {
    if (this.selectedElement) {
      evt.preventDefault()
      var coord = this.getMousePosition(evt)
      this.selectedElement.setAttributeNS(null, 'x', coord.x - this.offset.x)
      this.selectedElement.setAttributeNS(null, 'y', coord.y - this.offset.y)
      this.updateSVGPosition(coord.x - this.offset.x, coord.y - this.offset.y)
    }
  }
  endDrag(evt: Event) {
    this.selectedElement = null
  }

  tasks = []
  loaded = false
  dialog = false
  offsetCosts = ""
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
            }
          })
        task['links'] = dependOn
        // console.log(task)
        this.tasks.push(task)
        if (this.tasks.length > 1000) return false
        return true
      })
      console.log('returned')
      console.log(this.tasks)
      this.loaded = true
    } catch (err) {
      console.log(err)
    }
  }

  updateSVGPosition(x: number, y: number) {
    // console.log(this.svgRoot)
    this.svgRoot.style.position = 'absolute'
    this.svgRoot.style.left = (-x * this.svgRoot.getBBox().width) / 200
    this.svgRoot.style.top = (-y * this.svgRoot.getBBox().height) / 100
  }

  showContextMenu(e: Event) {
    this.contextMenu.style.visibility = "visible"
    this.contextMenu.style.left = e.x + "px"
    console.log(e, e.x, this.contextMenu.style.left)
    this.contextMenu.style.top = e.y + "px"
    let id: string = e.target.parentElement.children[4].children[0].attributes[1].value
    this.idCosts = parseInt(id)  }

  calcCosts() {
    setOffset(this.idCosts, this.offsetCosts).then(response => {
      this.setSnackbarSuccess("Количество сдвигов: " + response.count + " и цена: " + response.cost)
      // alert("Количество сдвигов: " + response.count + " и цена: " + response.cost)
    })
  }

  hideContextMenu(e: Event) {
    this.contextMenu.style.visibility = "hidden"

  }

  mounted() {
    document.addEventListener('contextmenu', function(event) {
      event.preventDefault();
    }, true); 
    this.processTasks().then(() => {
      let svgGantt = new SVGGantt('#svg-root', this.tasks, {
        viewMode: 'month',
      })
      // svgGantt.render()

      let canvasGantt = new CanvasGantt('#canvas', this.tasks, {
        viewMode: 'month',
      })
      // canvasGantt.render()

      let strGantt = new StrGantt(this.tasks, {
        viewMode: 'month',
      })
      let body = strGantt.render()
      this.contextMenu = document.getElementById("contextmenu")
      document.getElementById("svg-root").addEventListener('mousedown', this.hideContextMenu)
      let ganttBars = document.getElementsByClassName("gantt-bar")
      for (var i = 0; i < ganttBars.length; i++) {
        let leftDate = ganttBars[i].children[0]
        let rightDate = ganttBars[i].children[1]
        ganttBars[i].addEventListener('contextmenu', this.showContextMenu)
        
        // console.log(leftDate)
        // bar -> :active
      }
    })
  }
}
</script>
<style>
#navigation {
  position: fixed;
  background: rgba(0, 0, 0, 0.34) !important;
  right: 15px;
  bottom: 15px;
  width: 200px;
  height: 100px;
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
  width: 200px!important;
  height: 100px!important;
}
#contextmenu {
  position: fixed;
  visibility: hidden;
}
</style>