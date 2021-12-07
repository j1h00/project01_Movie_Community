<template>
  <div class=" flex item-center">
    <input 
      type="text" 
      class="w-full px-4 py-3 mx-4 leading-tight text-sm text-gray-900 bg-gray-200 rounded placeholder-gray-900 focus:outline-none focus:shadow-outline" 
      placeholder="search"
      v-model="searchInput"
      @keyup.enter="goSearch"
    >
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'SearchBar',
  data: function () {
    return {
      searchInput: '',
      movies : [],
    }
  },
  methods: {
    ...mapActions(['changeSearchInput']),
    goSearch() {
      this.changeSearchInput(this.searchInput)
      this.$router.push({
        name: 'SearchResults',
        params : {searchInput : this.searchInput},
      })
    }
  },
}
</script>

<style>

</style>