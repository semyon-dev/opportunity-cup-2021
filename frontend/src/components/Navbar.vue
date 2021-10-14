<template lang="pug">
nav
  v-app-bar(flat, app, large)
    // Title
    v-toolbar-title.grey--text
      span {{ $t("title") }}
    v-spacer
    v-tooltip(bottom)
      template(v-slot:activator='{ on, attrs }')
        v-slider.pt-12(
          v-model='slider',
          thumb-label,
          :min='1000',
          :max='13130',
          step='500',
          color='blue',
          track-color='grey',
          v-on='on',
          v-bind='attrs',
          @change='adjustLimit'
        )
      span Регулирует, сколько записей будет отображаться. Будьте осторожны! 7000 записей требуют 1Гб оперативной памяти
    // Dark mode
    v-btn(text, icon, color='grey', @click='toggleMode')
      v-icon(small) brightness_2
    // Language picker
    //- v-menu(offset-y)
      template(v-slot:activator='{ on }')
        v-btn(text, icon, color='grey', v-on='on') {{ currentLocale.icon }}
      v-list
        v-list-item(
          v-for='locale in locales',
          @click='changeLanguage(locale.code)',
          :key='locale.code'
        )
          v-list-item-title {{ locale.icon }}
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { i18n } from '@/plugins/i18n'
import * as api from '@/utils/api'
import { namespace } from 'vuex-class'

const AppStore = namespace('AppStore')

@Component
export default class Navbar extends Vue {
  @AppStore.State dark!: boolean
  @AppStore.State limit!: number

  @AppStore.Mutation setDark!: (dark: boolean) => void
  @AppStore.Mutation setLimit!: (limit: number) => void
  @AppStore.Mutation setLanguage!: (language: string) => void

  slider = 5000

  get locales() {
    return [
      { icon: '🇺🇸', code: 'en' },
      { icon: '🇷🇺', code: 'ru' },
    ]
  }
  get currentLocale() {
    for (const locale of this.locales) {
      if (locale.code === i18n.locale) {
        return locale
      }
    }
  }

  adjustLimit() {
    this.setLimit(this.slider)
  }
  toggleMode() {
    this.setDark(!this.dark)
    ;(this.$vuetify.theme as any).dark = this.dark
  }
  changeLanguage(locale: string) {
    i18n.locale = locale
    this.setLanguage(locale)
    document.title = i18n.t('strippedTitle') as string
  }
  mounted() {
    this.slider = this.limit
  }
}
</script>

<style>
nav a:link {
  text-decoration: none;
}

nav a:visited {
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

nav a:active {
  text-decoration: underline;
}

v-input__slider {
  max-width: 350px;
}
</style>
