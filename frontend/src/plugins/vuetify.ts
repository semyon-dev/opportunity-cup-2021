import Vue from 'vue'
import Vuetify, {
  VApp,
  VAppBar,
  VToolbarTitle,
  VSpacer,
  VBtn,
  VIcon,
  VMenu,
  VList,
  VListItem,
  VListItemTitle,
  VFlex,
  VLayout,
  VSnackbar,
  VMain,
  VProgressLinear,
  VDataTable,
  VProgressCircular,
  VDialog,
  VTextField,
  VCard,
  VCardActions,
  VCardText,
  VCardTitle,
  VDivider,
  VToolbar,
  VSlider,
  VTooltip
} from 'vuetify/lib'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify, {
  components: {
    VApp,
    VAppBar,
    VToolbarTitle,
    VSpacer,
    VBtn,
    VIcon,
    VMenu,
    VList,
    VListItem,
    VListItemTitle,
    VFlex,
    VLayout,
    VSnackbar,
    VMain,
    VProgressLinear,
    VDataTable,
    VProgressCircular,
    VDialog,
    VTextField,
    VCard,
    VCardActions,
    VCardText,
    VCardTitle,
    VDivider,
    VToolbar,
    VSlider,
    VTooltip
  },
})

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
})
