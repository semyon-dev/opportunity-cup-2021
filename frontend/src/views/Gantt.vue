<template lang="pug">
v-layout
  gantt-elastic(
    :options='options',
    :tasks='tasks',
    @tasks-changed='tasksUpdate',
    @options-changed='optionsUpdate',
    @dynamic-style-changed='styleUpdate'
  )
    gantt-header(slot='header')
</template>
<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import GanttElastic from 'gantt-elastic'
import GanttHeader from 'gantt-elastic-header'
import dayjs from 'dayjs'

import { getTasks } from '@/utils/api'

@Component({
  components: { GanttElastic, GanttHeader },
})
export default class Gantt extends Vue {
  getDate(hours: number) {
    const currentDate = new Date()
    const currentYear = currentDate.getFullYear()
    const currentMonth = currentDate.getMonth()
    const currentDay = currentDate.getDate()
    const timeStamp = new Date(
      currentYear,
      currentMonth,
      currentDay,
      0,
      0,
      0
    ).getTime()
    return new Date(timeStamp + hours * 60 * 60 * 1000).getTime()
  }

  loaded = false
  tasks = [
    {
      id: 1,
      label: 'Make some noise',
      user: '<a href="https://www.google.com/search?q=John+Doe" target="_blank" style="color:#0077c0;">John Doe</a>',
      start: this.getDate(-24 * 5),
      duration: 15 * 24 * 60 * 60 * 1000,
      percent: 85,
      type: 'project',
      //collapsed: true,
    },
  ]

  options = {
    taskMapping: {
      progress: 'percent',
    },
    maxRows: 100,
    maxHeight: 500,
    title: {
      label: 'Your project title as html (link or whatever...)',
      html: false,
    },
    row: {
      height: 24,
    },
    calendar: {
      hour: {
        display: true,
      },
    },
    chart: {
      progress: {
        bar: false,
      },
      expander: {
        display: true,
      },
    },
    taskList: {
      expander: {
        straight: false,
      },
      columns: [
        {
          id: 1,
          label: 'ID',
          value: 'id',
          width: 40,
        },
        {
          id: 2,
          label: 'Description',
          value: 'label',
          width: 200,
          expander: true,
          html: true,
          events: {
            click({ data, column }) {
              alert('description clicked!\n' + data.label)
            },
          },
        },
        {
          id: 3,
          label: 'Assigned to',
          value: 'user',
          width: 130,
          html: true,
        },
        {
          id: 3,
          label: 'Start',
          value: (task) => dayjs(task.start).format('YYYY-MM-DD'),
          width: 78,
        },
        {
          id: 4,
          label: 'Type',
          value: 'type',
          width: 68,
        },
        {
          id: 5,
          label: '%',
          value: 'progress',
          width: 35,
          style: {
            'task-list-header-label': {
              'text-align': 'center',
              width: '100%',
            },
            'task-list-item-value-container': {
              'text-align': 'center',
              width: '100%',
            },
          },
        },
      ],
    },
    locale: {
      name: 'en',
      Now: 'Now',
      'X-Scale': 'Zoom-X',
      'Y-Scale': 'Zoom-Y',
      'Task list width': 'Task list',
      'Before/After': 'Expand',
      'Display task list': 'Task list',
    },
  }
  dynamicStyle = {}
  lastId = 16

  addTask() {
    this.tasks.push({
      id: this.lastId++,
      label:
        '<a href="https://images.pexels.com/photos/423364/pexels-photo-423364.jpeg?auto=compress&cs=tinysrgb&h=650&w=940" target="_blank" style="color:#0077c0;">Yeaahh! you have added a task bro!</a>',
      user: '<a href="https://images.pexels.com/photos/423364/pexels-photo-423364.jpeg?auto=compress&cs=tinysrgb&h=650&w=940" target="_blank" style="color:#0077c0;">Awesome!</a>',
      start: this.getDate(24 * 3),
      duration: 1 * 24 * 60 * 60 * 1000,
      percent: 50,
      type: 'project',
    })
  }
  tasksUpdate(tasks: any) {
    this.tasks = tasks
  }
  optionsUpdate(options: any) {
    this.options = options
  }
  styleUpdate(style: any) {
    this.dynamicStyle = style
  }

  async processTasks() {
    try {
      const tasks = await getTasks()
      interface taskInterface {
        id: number
        start: number
        duration: number
        type: string
        dependentOn: number[]
        percent: number
        user: string
        style: Object
        label: string
        parentId: number
      }
      console.log(tasks)
      tasks.every(element => {
        // console.log(element, Object.keys(element))
        let task: taskInterface = {}

        task["label"] = "task from the table"
        task["user"] = "origin dev"
        task["percent"] = 100

        if (Object.keys(element).includes('_id')) task['id'] = element['_id']

        if (Object.keys(element).includes('start'))
          task['start'] = Date.parse(element['start'])

        if (Object.keys(element).includes('duration'))
          task['duration'] = element['duration']

        if (!task['duration']) {
          task['type'] = 'milestone'
          task['duration'] = 100
        } else task['type'] = 'task'

        let dependOn: number[] = []

        if (Object.keys(element).includes('predecessors'))
          element['predecessors'].forEach((predecessor) => {
            dependOn.push(predecessor['n'])
          })
        task['dependentOn'] = dependOn
        // console.log(task)
        this.tasks.push(task)
        if (this.tasks.length > 50) return false
        return true
      })
      console.log('returned')
      console.log(this.tasks)
      this.loaded = true
    } catch (err) {
      console.log(err)
    }
  }

  mounted() {
    this.tasks.push({
      id: 2,
      label: 'Make some noise',
      user: '<a href="https://www.google.com/search?q=John+Doe" target="_blank" style="color:#0077c0;">John Doe</a>',
      start: this.getDate(-24 * 5),
      duration: 15 * 24 * 60 * 60 * 1000,
      percent: 85,
      type: 'milestone',
      //collapsed: true,
    },
    {
      label: "task from the table",
      user: "origin dev",
      percent: 100,
      id: 3,
      start: 1569139200000,
      duration: 100,
      type: "milestone",
      dependentOn: [1703,1657]
    })
    this.processTasks()
  }
}
</script>