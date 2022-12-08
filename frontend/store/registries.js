const state = () => ({
  registries: [],
})

const mutations = {
    addRegistries(state, data) {
        data.password = '**********'
        state.registries.push(data)
    },

    setRegistries (state, data) {
        state.registries = data
    }
}

const actions = {
    async sendRegistry({commit}, data) {
        await this.$axios.post('/api/registries', data).then(() => {
            commit('addRegistries', data)
        })
    },

    async getRegistries({commit}) {
        await this.$axios.get('/api/registries').then(({ data }) => {
            commit('setRegistries', data)
        })
    }
}

export default {
  state,
  mutations,
  actions,
}
