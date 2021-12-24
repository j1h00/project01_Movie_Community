<template>
  <div>
    <div v-if="!movie"></div>
    <!-- Modal -->

    <div v-else-if="!loading_sources && movie">
      <movie-modal></movie-modal>

      <!-- header -->
      <movie-detail-header></movie-detail-header>
      <br>
      <!-- section -->
      <movie-detail-section></movie-detail-section>
    
    </div>
  </div>
</template>

<script>
import MovieModal from '@/components/MovieModal.vue'
import MovieDetailHeader from '@/components/MovieDetailHeader.vue'
import MovieDetailSection from '@/components/MovieDetailSection.vue'
import { mapState, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name : 'MovieDetail',
  components: {
    MovieModal, MovieDetailHeader, MovieDetailSection
  },
  data: function(){
    return{
      movieId: this.$route.params.movieId,
      movie: null,
      loading_sources: true,
      createdReview: null,
    }
  },
  computed: {
    ...mapState(['movieDetail'])
  },
  methods:{
    ...mapActions(['saveMovieDetail', 'saveSimilarMovies']),
    getMovieDetail() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${this.movieId}`
      })
        .then(res => {
          const movieDetail = res.data.movie
          this.saveMovieDetail(movieDetail)
          this.saveSimilarMovies(res.data.similar_movies)
          this.movie = movieDetail
        })
        .then(() => {
          this.loading_sources = false
        })
        .catch(err => console.error(err))
    },
    reviewCreated(data) {
      this.createdReview = data
    }
  },
  created() {
    this.getMovieDetail()
  }
}
</script>

<style scoped>
</style>

