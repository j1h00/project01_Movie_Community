<template>
  <div>
    <!-- Header -->
    <div 
      class="header-box bg-cover bg-center" 
      :style="{ 'background-image': 'url(' + getRandomImgUrl + ')' }">
      <div class="h-80 pt-20 text-white flex flex-col justify-center">
        <h3 class="text-2xl tracking-widest text-center">Movie</h3>
        <h1 class="mt-8 text-center text-5xl font-bold">Now Playing & Popular Movies</h1>
      </div>
    </div>

    <div class="home-section bg-white">
      <!-- 최신 영화 10 -->
      <h1 class="border-t-2 ml-3 mt-5 p-3 text-3xl font-bold">최신 영화</h1>
      <div v-if="movies && movies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-x-scroll wrapper-box ml-3">
        <div v-for="(movie, idx) in movies.slice(0,10)" :key="idx" class="movie-card border py-4 px-4 bg-whit w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
          <movie-card :movie="movie"></movie-card>
        </div>
      </div>

      <!-- 평점순 영화 20 -->
      <h1 class="border-t-2 ml-3 mt-5 p-3 text-3xl font-bold">평점순</h1>
      <div v-if="movies && movies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-x-scroll wrapper-box ml-3">
        <div v-for="(movie, idx) in highRateMovies" :key="idx" class="movie-card border py-4 px-4 bg-whit w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
          <movie-card :movie="movie" :avgRating="movie.avgRating"></movie-card>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
// import HomeHeader from '@/components/HomeHeader.vue'

import _ from 'lodash'
import axios from 'axios'
import { mapActions, mapState } from 'vuex'

export default {
  name : 'Home',
  components : {
    MovieCard, // HomeHeader
  },
  data: function(){
    return {
      movies: null,
      highRateMovies: null,
      backgroudImageURL: "https://cdn.pixabay.com/photo/2019/11/07/20/48/cinema-4609877_960_720.jpg",
    }
  },
  computed: {
    ...mapState(['userInfo']),
    getRandomImgUrl: function(){
      if (this.movies) {
        const url = _.sample(this.movies).backdrop_path
        const imgUrl = `https://image.tmdb.org/t/p/original/${url}`
        return imgUrl
      } else {
        return false
      }
    },
  },
  methods: {
    ...mapActions(['saveMovieDetail']),
    // 영화 전체 정보를 가져온다.
    getMovies() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/'
      })
        .then(res =>{
          this.movies = _.sortBy(res.data, 'release_date').reverse()

          const newAvgMovies = []
          const getAvgRating = function (now_movie) {
              let score = null
              now_movie.reviews.forEach(review => {
                score += review.rating
              })
              return score / now_movie.reviews.length
          }

          res.data.forEach(movie => {
            if (movie.reviews.length){
              newAvgMovies.push({
                ...movie,
                avgRating: getAvgRating(movie)
              }) 
            } 
          })

          this.highRateMovies = _.sortBy(newAvgMovies, 'avgRating').reverse().slice(0,20)
          
        })
        .catch(err =>{
          console.log(err)
        })
    },
  },
  created: function () {
    this.getMovies()
  }
}
</script>

<style scoped>
.header-box {
  height: 500px;
}
.home-section {
  height: 1500px;
}

.movie-section  {
  height: 570px;
}

.movie-card {
  height: 510px;
  cursor: pointer;
}

.my-box {
  width: 100%;
  height: 400px;
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