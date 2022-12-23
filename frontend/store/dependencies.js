const state = () => ({
  dependencies: [],
  min_version: [],
  notes: [],
})

const mutations = {
  setDependencies(state, data) {
    state.dependencies = data
    data.items.forEach((dep) => {
      state.min_version[dep.name] = dep.minimum_version;
      state.notes[dep.name] = dep.notes;
    })
  },

  setVersion(state, data) {
    state.dependencies.find((dep) => dep.id === data.id).minimum_version = data.version
  }
}

const actions = {
  async getDependencies({commit}, {page, perPage}) {
    await this.$axios.get(`/api/packages?page=${page}&per_page=${perPage}`).then((response) => {
      commit('setDependencies', response.data)
    })
  },

  async setVersion({commit}, { id, version, notes }) {
    await this.$axios.put(`/api/packages/${id}`, { minimum_version: version , notes })
    commit('setVersion', { id, version })
  },

  async setNotes({commit}, { id, version, notes }) {
    await this.$axios.put(`/api/packages/${id}`, { minimum_version: version , notes })
  }
}

export default {
  state,
  mutations,
  actions
}
