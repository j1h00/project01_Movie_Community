<template>
  <section>
    <div class="section-box lg:section-box2 bg-gray-100">
      <div class="h-full max-w-screen-lg mx-auto bg-white">
        <div class="h-1/2 p-3">
          <div class="flex flex-col lg:flex-row h-auto mt-10 mx-3 ">
            <div class="w-auto h-auto max-h-96 lg:w-1/3 flex flex-col bg-white rounded shadow-lg p-4 items-center border-b-8 lg:border-b-0 lg:border-r-8 border-red-400">
              <h2 class="font-bold">개요</h2>
              <p v-if="movie.overview" class="p-4 text-gray-600 overflow-ellipsis overflow-hidden">
                {{ movie.overview.slice(0,250) }} ... 
              </p>
            </div>
            <div class="w-full lg:w-2/3 ">
              <div class="video-container">
                <iframe :src="getTrailerUrl" frameborder="none" allowfullscreen></iframe>
              </div>
            </div>  
          </div>

          <h1 class="border-t-2 ml-3 mt-5 -mb-2 p-3 text-xl font-bold">출연/제작</h1>
          <div class="crew-section">
            <div class="h-full flex flex-wrap flex-col overflow-x-scroll wrapper-box ml-3">
              <div v-for="(crew, idx) in crews" :key="idx" class="profile-box my-3 mx-2">
                <crew-card :crew="crew"></crew-card>
              </div>
            </div>
          </div>
        
          <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">리뷰</h1>
          <div class="relative review-section">
            <review-list></review-list>
          </div>

          <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">비슷한 영화 추천</h1>
          <h1 class="ml-3 text-md font-bold text-blue-700">키워드 : {{ parsedKeywords }} / {{ parsedGenres }} </h1>
          <movie-recommend :similar-movies="similarMovies"></movie-recommend>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState } from 'vuex'
import ReviewList from '@/components/ReviewList.vue'
import CrewCard from '@/components/CrewCard.vue'
import MovieRecommend from '@/components/MovieRecommend.vue'

export default {
  name: 'MovieDetailSection',
  components: {
    ReviewList, CrewCard, MovieRecommend
  },
  data: function () {
    return {
      movie: this.movieDetail,
      crews: null,
      keywords: null,
    }
  },
  methods: {
  },
  computed: {
    ...mapState(['movieDetail', 'similarMovies']),
    getTrailerUrl: function() {
      const trailer_url = `https://www.youtube.com/embed/${this.movie.trailer_path}`
      return trailer_url
    },
    parsedKeywords: function() {
      const parsed = this.movie.keywords.map(keyword => keyword.name)
      return parsed.join(' / ')
    },
    parsedGenres() {
      const parsed = this.movie.genres.map(genre => genre.name)
      return parsed.join(' / ')
    },
  },
  created() {
    this.movie = this.movieDetail
    this.crews = this.movieDetail.crews
    this.keywords = this.movie.keywords.join('/') + '/' + this.movie.genres.join('/')
  }
}
</script>

<style>
.video-container {
	position: relative;
	padding-bottom: 56.25%;
  height: 0;
	overflow: hidden;
}
 
.video-container iframe,
.video-container object,
.video-container embed {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
}

.profile-box {
  width: 140px;
  height: 273px;
}

.crew-section {
  height: 320px;
}

.section-box {
  height: 2300px;
}

.review-section {
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

.scroll-box:before {
    background: linear-gradient(center top , #fff 0%, rgba(255, 255, 255, 0) 60%) repeat scroll 0 0 rgba(0, 0, 0, 0);
    content: "";
    display: block;
    height: 300px;
    left: 0;
    pointer-events: none;
    position: fixed;
    top: 0;
    width: 100%;
}

.scroll-box:after {
    background: linear-gradient(center bottom , #fff 0%, rgba(255, 255, 255, 0) 60%) repeat scroll 0 0 rgba(0, 0, 0, 0);
    bottom: 0;
    content: "";
    display: block;
    height: 300px;
    left: 0;
    pointer-events: none;
    position: fixed;
    width: 100%;
}
</style>