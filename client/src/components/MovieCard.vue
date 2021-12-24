<template>
  <div class="w-sm" @click="toMoviedetail(movie)">
    <img class="w-64 rounded-md shadow-lg" :src="getImgUrl(movie.poster_path)" alt="Poster Image" />
    <div class="mt-4 text-black text-center flex flex-col items-center">
      <h1 class="text-xl font-bold">{{ movie.title }}</h1>
      <div v-if="(this.$route.name === 'MovieDetail')">
        <div class="w-60 bg-gray-100 rounded-xl shadow-sm overflow-hidden p-1">
          <div class="similar progress-bar relative h-5 flex items-center justify-center">
          </div>
        </div>
      </div>
      <div v-else-if="score">
        <div class="w-60 bg-gray-100 rounded-xl shadow-sm overflow-hidden p-1">
          <div class="score progress-bar relative h-5 flex items-center justify-center">
          </div>
        </div>
      </div>
      <div v-else-if="avgRating" class="flex items-center">
        <star-rating :rating="changeAvgRating" :read-only="true" :increment="0.5" :show-rating="false" :star-size="20"></star-rating>
        <p class="text-xs font-bold ml-1 mt-1">{{ Math.round((this.avgRating + Number.EPSILON) * 100) / 100 }}</p>
      </div>
      <div v-else>
        <p class="mt-1 text-gray-600">{{ movie.release_date }}</p>
      </div>

      <!-- <button class="mt-8 mb-4 py-2 px-14 rounded-full bg-green-600 text-white tracking-widest hover:bg-green-500 transition duration-200">MORE</button> -->
    </div>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'

export default {
  name: "MovieCard",
  components: {
    StarRating
  },
  data: function () {
    return {
      nowMovie: null,
      nowScore: this.score,
      nowSimilarity: this.similarity
    }
  },
  props: {
    movie: Object,
    similarity: Number,
    score: Number,
    avgRating: Number
  },
  methods: {
    toMoviedetail(movie) {
      if (this.$route.name === 'SetUser'){
        var m = confirm("사용자 취향 정보를 수집중입니다.\n영화 상세 페이지로 이동하시겠습니까? ");
        if (m) {
          this.$router.push({
            name: 'MovieDetail',
            params : { movieId: movie.id }
          })
        }
      } else {
        this.$router.push({
          name: 'MovieDetail',
          params : { movieId: movie.id }
        })
      }
    },
    getImgUrl: function(url){
      const imgUrl = `https://image.tmdb.org/t/p/original/${url}`
      return imgUrl
    },
  },
  created() {
    this.nowMovie = this.movie
  },
  computed: {
    changeAvgRating() {
      return Math.round((this.avgRating + Number.EPSILON) * 100) / 100 / 2
    },
  },
  watch() {
    if (this.score) {
      const progressBar = document.querySelector('.score')
      const div = `<div class="absolute top-0 bottom-0 left-0 rounded-lg bg-blue-300" style="width: ${this.score}%;"></div>
              <div class="relative font-medium text-sm">${ this.score } %</div>`
      progressBar.innerHTML = div
      progressBar.classList.toggle('score')
    }
    if (this.similarity) {
      const progressBar = document.querySelector('.similar')
      const div = `<div class="absolute top-0 bottom-0 left-0 rounded-lg bg-blue-300" style="width: ${this.similarity}%;"></div>
              <div class="relative font-medium text-sm">${ this.similarity } %</div>`
      progressBar.innerHTML = div
      progressBar.classList.toggle('similar')
    }
  },
  mounted() {
    if (this.score) {
      const progressBar = document.querySelector('.score')
      const div = `<div class="absolute top-0 bottom-0 left-0 rounded-lg shadow-lg bg-blue-300" style="width: ${this.score}%;"></div>
              <div class="relative font-medium text-sm">${ this.score } %</div>`
      progressBar.innerHTML = div
      progressBar.classList.toggle('score')
    }
    if (this.similarity) {
        const progressBar = document.querySelector('.similar')
        const div = `<div class="absolute top-0 bottom-0 left-0 rounded-lg bg-blue-300" style="width: ${this.similarity}%;"></div>
                <div class="relative font-medium text-sm">${ this.similarity } %</div>`
        progressBar.innerHTML = div
        progressBar.classList.toggle('similar')
        
      }
  }
}
</script>

<style>

</style>