<template>
  <div v-if="movies && movies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-y-hidden overflow-x-scroll wrapper-box ml-3">
    <div v-for="(movie, idx) in movies" :key="idx" class="movie-card py-4 px-4 w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
      <movie-card :movie="movie.target" :similarity="Math.round(movie.similarity * alpha)"></movie-card>
    </div>
  </div>
  <div v-else>
    <h1 class="ml-3 mt-1 p-3 text-xl">아직 작성된 리뷰가 없습니다.</h1>
  </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
import _ from 'lodash'

export default {
  name: 'MovieRecommend',
  components: {
    MovieCard
  },
  data() {
    return {
      movies: _.sortBy(this.similarMovies, 'similarity').reverse()
    }
  },
  computed: {
    alpha() {
      return 99 / this.movies[0].similarity
    }
  },
  props: {
    similarMovies: Object
  }
}
</script>

<style scoped>
.movie-section  {
  height: 550px;
}

.movie-card {
  height: 510px;
  cursor: pointer;
}

.wrapper-box {
  scroll-behavior: smooth
}

.wrapper-box::-webkit-scrollbar {
  width: 2px;
  cursor: pointer;
  /* background-color: rgba(229, 231, 235, var(--bg-opacity)); */
}

.wrapper-box::-webkit-scrollbar-track {
  background-color: transparent;
  cursor: pointer;
  /*background: red;*/
}

.wrapper-box::-webkit-scrollbar-thumb {
  cursor: pointer;
  border-radius: 20px;
  background-color: lightgrey;
  border: 6px solid transparent;
  background-clip: content-box;
  /*outline: 1px solid slategrey;*/
}
</style>