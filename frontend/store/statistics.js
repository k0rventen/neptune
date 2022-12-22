const state = () => ({
  stats: undefined,
  historicalStats: undefined,
  fiveImg: undefined
})

const mutations = {
  setStats(state, data) {
    state.stats = data
  },

  setHistoricalStats(state, data) {
    state.historicalStats = data
  },

  setFiveImg(state, data) {
    state.fiveImg = data
  }
}

const actions = {
  async getStats({commit}) {
    await this.$axios.get('/api/statistics?current=true').then(({ data }) => {
      commit('setStats', data)
    })
  },

  async getHistoricalStats({commit}) {
    await this.$axios.get('/api/statistics?current=false').then((response) => {
      commit('setHistoricalStats', response.data)
    })
  },

  async getFiveImg({commit}) {
    await this.$axios.get('/api/tags/featured').then(({ data }) => {
      commit('setFiveImg', data)
    })
  }
}

export default {
  state,
  mutations,
  actions
}

