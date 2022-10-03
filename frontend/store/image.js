const state = () => ({
  images: []
})

const mutations = {
  setImage(state, data) {
    state.images = data
  }
}

const actions = {
  async getImages({commit}) {
    await this.$axios.get('/api/images').then((response) => {
      commit('setImage', response.data)
    })
  }
}

export default {
  state,
  mutations,
  actions
}

