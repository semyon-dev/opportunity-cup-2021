<template lang="pug">
v-layout
  //- show content only if data is loaded. Unless show progress-circular
  v-layout(v-if='loaded') 
    #navigation()
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
    canvas#canvas-root(style='visibility: hidden')
    pre#str
  v-layout(v-else)
    v-progress-circular(indeterminate, :width='7', :size='70')
</template>
<script lang="ts" defer>
import Vue from 'vue'
import Component from 'vue-class-component'
import { SVGGantt, CanvasGantt, StrGantt } from 'gantt'

import { getTasks } from '@/utils/api'

@Component({})
export default class GanttSimple extends Vue {
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

  getMousePosition(evt: Event) {
    let CTM = this.svg.getScreenCTM()
    return {
      x: (evt.clientX - CTM.e) / CTM.a,
      y: (evt.clientY - CTM.f) / CTM.d,
    }
  }

  startDrag(evt: Event) {
    if (this.svg === null)
      this.svg = evt.target
    if (this.svgRoot === null)
      this.svgRoot = (document.getElementById("svg-root") as HTMLElement).children[0]

    if (evt.target.classList.contains('draggable')) {
      this.selectedElement = evt.target;
      this.offset = this.getMousePosition(evt);
      this.offset.x -= parseFloat(this.selectedElement.getAttributeNS(null, "x"));
      this.offset.y -= parseFloat(this.selectedElement.getAttributeNS(null, "y"));
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
        task['parentId'] = 4

        if (Object.keys(element).includes('_id')) task['id'] = element['_id']
        task['text'] = task.id.toString()

        if (Object.keys(element).includes('start'))
          task['start'] = new Date(element['start'])

        if (Object.keys(element).includes('duration'))
          task['end'] = new Date(
            Date.parse(element['start']) + element['duration'] * 3600*1000
          )
        console.log(task["id"], task['start'], task['end'], element['duration'])

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

  updateSVGPosition(x: number, y:number) {
    // console.log(this.svgRoot)
    this.svgRoot.style.position = "absolute";
    this.svgRoot.style.left = -x * this.svgRoot.getBBox().width / 200;
    this.svgRoot.style.top = -y * this.svgRoot.getBBox().height / 100;
  }

  mounted() {
    this.processTasks().then(() => {
      let svgGantt = new SVGGantt('#svg-root', this.tasks, {
        viewMode: 'month',
      })

      let canvasGantt = new CanvasGantt('#canvas-root', this.tasks, {
        viewMode: 'month',
      })

      let strGantt = new StrGantt(this.tasks, {
        viewMode: 'month',
      })
      let body = strGantt.render()
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
  position: absolute!important;
}
</style>