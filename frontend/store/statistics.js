const state = () => ({
  stats: undefined,
  historicalStats: undefined,
  fiveLast: undefined
})

const mutations = {
  setStats(state, data) {
    state.stats = data
  },

  setHistoricalStats(state, data) {
    state.historicalStats = data
  },

  setFiveLast(state, data) {
    state.fiveLast = data
  }
}

const actions = {
  async getStats({commit}) {
    await this.$axios.get('/api/statistics').then((response) => {
      commit('setStats', response.data)
    })
  },

  async getHistoricalStats({commit}) {
    await this.$axios.get('/api/historicalstatistics').then((response) => {
      commit('setHistoricalStats', response.data)
    })
  },

  async getFiveLast({commit}) {
    await this.$axios.get('/api/tags?offset=0&limit=5').then((response) => {
      commit('setFiveLast', response.data)
    })
  }
}

export default {
  state,
  mutations,
  actions
}

