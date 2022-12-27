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
    state.dependencies.items.find((dep) => dep.id === data.id).minimum_version = data.version
  },

  updateOutdated(state, data) {
    state.dependencies.items.find((dep) => dep.id === data.id).versions.forEach((version) => {
      if(version.version <= data.version) {
        version.outdated = true
      } else {
        version.outdated = false
      }
    })
  }
}

const actions = {
  async getDependencies({commit}, {page, perPage, filter}) {
    const url = urlBuilder(page, perPage, filter)
    await this.$axios.get(url).then((response) => {
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

const urlBuilder = (page, perPage, filter) => {
  let url = `/api/packages?page=${page}&per_page=${perPage}`
  if(filter) {
    Object.entries(filter).forEach(([key, value]) => {
      if(value) {
        url += `&${key}=${value}`
      }
    })
  }  
  return url
}

export default {
  state,
  mutations,
  actions
}
