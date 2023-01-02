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
    state.tags.items.push(data)
  },
  currentImage(state, data) {
    state.currentImage = data
  },
  setTags(state, data) {
    state.tags = data
  },
  unsetImage(state, sha) {
    state.tags.items = state.tags.items.filter((image) => image.sha !== sha)
  },
  changeVulnState(state, {active , id}) {
    let backup
    if(state.currentImage) {
      if(active) {
        state.currentImage.vulnerabilities = state.currentImage.vulnerabilities.filter((vuln) => {
          if(vuln.id === id) {
            backup = vuln
            return false
          }
          return true
        })
        backup.active = active
        state.currentImage.active_vulnerabilities.push(backup)
      } else {
        state.currentImage.active_vulnerabilities = state.currentImage.active_vulnerabilities.filter((vuln) => {
          if(vuln.id === id) {
            backup = vuln
            return false
          }
          return true
        })
        backup.active = active
        state.currentImage.vulnerabilities.push(backup)
      }
    }
  }
}

const actions = {

  async deleteImage({commit}, data) {
    await this.$axios.delete(`/api/tags/${data}`).then(async () => {
      await this.$axios.get('/api/images').then((response) => {
        commit('setImage', response.data)
      })
    })
  },

  async setAckState({commit}, {id, notes, active}) {
    await this.$axios.put(`api/vulnerabilities/${id}`, {
      notes,
      active
    }).then(() => {
      commit('changeVulnState', {active, id})
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

  async getTags({commit}, {page, perPage, filter}) {
    const url = urlBuilder(page, perPage, filter)
    await this.$axios.get(url).then(({data}) => {
      commit('setTags', data)
    })
  },

  async removeImg({ commit }, sha) {
    await this.$axios.delete(`/api/tags/${sha}`)
    commit('unsetImage', sha)
  }
}

const urlBuilder = (page, perPage, filter) => {
  let url = `/api/tags?page=${page}&per_page=${perPage}`
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

