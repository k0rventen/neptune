const state = () => ({
  images: [],
  currentImage: undefined,
  tags: undefined
})

const mutations = {
  setImage(state, data) {
    state.images = data
  },
  addImage(state, data) {
    state.images.push(data)
  },
  currentImage(state, data) {
    state.currentImage = data
  },
  setTags(state, data) {
    state.tags = data
  }
}

const actions = {
  async getImages({commit}) {
    await this.$axios.get('/api/images').then((response) => {
      commit('setImage', response.data)
    })
  },

  async deleteImage({commit}, data) {
    await this.$axios.delete(`/api/tags/${data}`).then(async () => {
      await this.$axios.get('/api/images').then((response) => {
        commit('setImage', response.data)
      })
    })
  },

  async scanImages({commit}, image) {
    await this.$axios.post('/api/scan', image).then((response) => {
      commit('addImage', response.data)
    })
  },

  async getCurrentImage({commit}, image) {
    await this.$axios.get(`/api/tags/${image}`).then((response) => {
      commit('currentImage', response.data)
    })
  },

  async getTags({commit}) {
    await this.$axios.get('/api/tags').then(({data}) => {
      commit('setTags', data)
    })
  }
}

export default {
  state,
  mutations,
  actions
}

