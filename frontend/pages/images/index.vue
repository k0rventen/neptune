<template>
  <div class="w-full">
    <div class="mt-3 px-3 w-full">
      <label class="relative">
        <svg class="absolute top-1 left-1 fill-black" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
        <input v-model="search" type="text" class="focus:outline-none rounded-md w-full px-5 py-1 bg-[#FEFBF6] placeholder-black" :placeholder="$t('images.search')">
      </label>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
        <template v-for="image in value">
          <card-image v-for="tags in image.tags" :key="tags.image_id" :header="tags.image.concat(':', tags.tag)" :color="selectColor(tags.vulnerabilities, tags.outdated_packages)">
            <ul>
              <li>{{ $t('images.added_date') }} : {{ convertDate(tags.date_added) }}</li>
              <li>{{ $t('images.size') }} : {{ calcSize(tags.size) }}</li>
              <li>{{ $tc('images.package', tags.packages) }} : {{ tags.packages }}</li>
              <li>{{ $tc('images.vulnerability', tags.vulnerabilities )}} : {{ tags.vulnerabilities }} </li>
              <li>{{ $tc('images.outdated_package', tags.outdated_packages )}} : {{ tags.outdated_packages }} </li>
            </ul>
          </card-image>
        </template>

      </div>
    </div>


  </div>
</template>

<script>
import {api} from "static/data";

export default {
  name: "ImagesPage",
  data() {
    return {
      value: api,
      search: undefined
    }
  },
  watch: {
    search(newValue) {
      if(newValue === '') {
        this.value = api
      } else {
        this.value = api.filter((el) => el.name.includes(newValue) )
      }
    }
  },
  methods: {
    convertDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString('fr-FR', options)
    },
    calcSize(size) {
      if (size / 1024 >= 1) {
        if (size / 1024 / 1024 >= 1) {
          if (size / 1024 / 1024 / 1024 >= 1) {
            return (size / 1024 / 1024 / 1024).toFixed(2) + " Go";
          } else {
            return (size / 1024 / 1024).toFixed(2) + " Mo";
          }
        } else {
          return (size / 1024).toFixed(2) + " Ko";
        }
      } else {
        return size + " o";
      }
    },
    selectColor(vuln, outdated){
      if(vuln > 0) {
        return 'bg-red-400'
      }
      if(outdated > 0) {
        return 'bg-yellow-400'
      }
      return 'bg-green-400'
    }

  }
}
</script>

