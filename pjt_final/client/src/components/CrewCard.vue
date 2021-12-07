<template>
    <div class="w-full h-full bg-white border border-gray-200 rounded shadow-lg">
      <div
        v-if="crew.profile_path"
        class="bg-cover bg-center profile-image" 
        :style="{ 'background-image': 'url(' + getProfileImgUrl + ')' }">
      </div>
      <div v-else>
        <img src="../assets/unknown.png" alt="">
      </div>
      <div class="w-full">
        <div class="p-4">
          <p class="font-bold">
            {{ crew.name }}
          </p>
          <p class="mb-2 text-sm text-gray-600">{{ crew.role }}</p>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'CrewCard',
  props: {
    crew: Object,
  },
  computed: {
    getProfileImgUrl: function(){
      if (this.crew.profile_path) {
        return `https://image.tmdb.org/t/p/original/${this.crew.profile_path}`
      } else {
        return '../assets/unknown.png'
      } 
    },
  }
}
</script>

<style>
.profile-image {
  width: 138px;
  height: 175px;
}
</style>