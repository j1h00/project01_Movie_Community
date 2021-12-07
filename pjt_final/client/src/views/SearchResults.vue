<template>
  <div>
    <!-- Header -->
    <div class="h-80 flex flex-col justify-center">
      <h3 class="text-2xl tracking-widest text-gray-900 text-center">Movie</h3>
      <h1 class="mt-8 text-center text-5xl text-gray-900 font-bold">" {{ this.searchInput }} " 의 검색 결과</h1>
    </div>


    <section class="bg-gray-100">
      <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">영화 검색 결과</h1>
      <div v-if="movies && movies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-y-hidden overflow-x-scroll wrapper-box ml-3">
        <div v-for="(movie, idx) in this.movies" :key="idx" class="movie-card border py-4 px-4 bg-whit w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
          <movie-card :movie="movie"></movie-card>
        </div>
      </div>

      <div v-else>
        <h1 class="ml-7 text-lg">검색 결과가 없습니다.</h1>
      </div>

      <h1 class="border-t-2 ml-3 mt-5 -mb-2 p-3 text-xl font-bold">배우/감독 검색 결과</h1>
      <div v-if="crews && crews.length" class="crew-section">
        <div class="h-full flex flex-wrap flex-col overflow-x-scroll wrapper-box ml-3">
          <div v-for="(crew, idx) in crews" :key="idx" class="profile-box my-3 mx-2">
            <crew-card :crew="crew"></crew-card>
          </div>
        </div>
      </div>
      <div v-else class="crew-section">
        <h1 class="ml-7 text-lg">검색 결과가 없습니다.</h1>
      </div>
    </section>
  </div>
</template>

<script>
import CrewCard from '@/components/CrewCard.vue'
import MovieCard from '@/components/MovieCard.vue'
import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'SearchResults',
  components: {
    CrewCard, MovieCard
  },
  data: function(){
    return {
      movies: null,
      crews: null,
    }
  },
  computed: {
    ...mapState(['searchInput'])
  },
  methods:{
    ...mapActions(['changeSearchInput']),
    getSeachResult() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/search/',
        params: {
          searchInput: this.searchInput,
        },
      })
        .then(res => {
          this.movies = res.data.movie_data
          this.crews = res.data.crew_data
        })
        .catch(err => console.error(err))
    },
  },
  created: function(){
    this.changeSearchInput(this.$route.params.searchInput)
    this.getSeachResult()
  },
  watch: {
    searchInput: function () {
      this.getSeachResult()
    }
  }
}
</script>

<style scoped>
.movie-section  {
  height: 570px;
}

.movie-card {
  height: 510px;
  cursor: pointer;
}

.crew-section {
  height: 320px;
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

