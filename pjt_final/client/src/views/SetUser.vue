<template>
  <div class="container p-20">
    <div class="h-full bg-gray-100 flex flex-col justify-center items-center">
      <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">사용자 취향 정보 분석 중</h1>
      <div v-if="flag" class="w-full flex flex-col gap-6 border">
        <div v-for="movie in movies" :key="movie" >
          <div class="flex">
            <movie-card :movie="movie" class="movie-card py-4 px-4 w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0"></movie-card>
            <div class="w-96 p-5">
              <h1> 별점을 달아주세요 </h1>
              <star-rating 
                :increment="0.5"
                :show-rating="false" 
                :rating="rating"
                @update:rating="rating = $event"
                @click="setUser(movie.id)">
              </star-rating>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MovieCard from '@/components/MovieCard'
import axios from 'axios'
import _ from 'lodash'
import StarRating from 'vue-star-rating'

export default {
  name: "SetUser",
  components: {
    MovieCard, StarRating
  },
  data() {
    return {
      flag: false,
      movies: [1],
      rating: 0,
    }
  },
  methods: {
    getMovies() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/'
      })
        .then(res =>{

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

          const tempMovies = _.sortBy(newAvgMovies, 'avgRating').reverse().slice(0,100)
          this.movies = _.sampleSize(tempMovies, 15)
          this.flag = true
        })
        .catch(err =>{
          console.log(err)
        })
    },
    setUser(movieId) {
      const token = localStorage.getItem('token')
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/reviews/setuser/${movieId}/`,
        headers: {
          Authorization: `Token ${token}`
        },
        data: {
          rating: parseInt(parseFloat(this.rating)*2),
        }
      })
        .then(() => {
          var index = null
          for (let i=0; i < this.movies.length; i++) {
            if (this.movies[i].id === movieId) {
              index = i 
            }
          }
          if (index > -1) {
            this.movies.splice(index, 1)
          }
          this.rating = 0
          if (this.movies.length === 0) {
            this.$router.push({
            name: 'MyProfile',
          })
      }
        })
        .catch(err => console.error(err))
    }
  },
  created() {
    this.getMovies()
  },

}
</script>

<style scoped>
.movie-section  {
  height: 550px;
}

.movie-card {
  height: 470px;
  cursor: pointer;
}
</style>