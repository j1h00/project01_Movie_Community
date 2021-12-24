<template>
   <div>
      <!-- Header -->
      <div class="h-10">
      </div>
      <h1 v-if="userInfo" class="border-t-2 ml-3 mt-5 p-3 text-3xl font-bold">{{ userInfo.user_data.username }}</h1>
      
      <section class="bg-gray-100">
         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">추천 영화</h1>
         <div v-if="rMovies && rMovies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-y-hidden overflow-x-scroll wrapper-box ml-3">
            <div v-for="(movie, idx) in rMovies" :key="idx" class="movie-card py-4 px-4 w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
               <movie-card :movie="movie" :score="Math.round(movie.score * alpha)"></movie-card>
            </div>
         </div>

         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">내가 본 영화</h1>
         <div v-if="myMovies && myMovies.length" class="movie-section overflow-y-hidden p-5 h-full flex flex-wrap flex-col gap-10 overflow-x-scroll wrapper-box ml-3">
            <div v-for="(movie, idx) in myMovies" :key="idx" class="movie-card py-4 px-4 bg-white w-72 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
               <movie-card :movie="movie"></movie-card>
            </div>
         </div>

         <div v-else>
         <h1 class="ml-7 text-lg">검색 결과가 없습니다.</h1>
         </div>

         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">내가 작성한 리뷰</h1>
         <div v-if="reviewNotEmpty" class="review-box">
            <div class="h-full p-3 review-box flex flex-wrap flex-col justify-start items-center overflow-x-scroll gap-6 wrapper-box ml-3 pb-3">
               <div v-for="(review, idx) in myReviews" :key="idx" class="shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 w-72 md:w-96 h-full">
                  <review-card :review="review"></review-card>
               </div>
            </div>
         </div>
         <div v-else>
            <h1 class="ml-3 mt-1 p-3 text-xl">아직 작성된 리뷰가 없습니다.</h1>
         </div>

         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">내가 작성한 댓글</h1>
         <div v-if="commentNotEmpty" class="comment-box">
            <div class="h-full flex flex-wrap flex-col overflow-x-scroll gap-6 wrapper-box ml-3 pb-3">
               <div v-for="(comment, idx) in myComments" :key="idx" class="w-72 md:w-96 h-full">
                  <button @click="goReviewDetail(comment.review)" class="ml-2 text-sm font-bold go-review">해당 리뷰로 이동</button>
                  <comment-card :comment="comment" @comment-deleted="getUserInfo()"></comment-card>
               </div>
            </div>
         </div>
         <div v-else class="comment-box">
            <h1 class="ml-3 mt-1 p-3 text-xl">아직 작성된 댓글이 없습니다.</h1>
         </div>
      </section>
   </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
import ReviewCard from '@/components/ReviewCard.vue'
import CommentCard from '@/components/CommentCard.vue'

import { mapState, mapActions } from 'vuex'
import _ from 'lodash'

export default {
   name : 'UserProfile',
   components: {
      MovieCard, ReviewCard, CommentCard
   },
   data (){
      return{
         myReviews: null,
         myComments: null,
         myInfo: null,
         myMovies: null,
         reviewNotEmpty: false,
         commentNotEmpty: false,
         rMovies: null,
         rMovies2: null,
      }
   },
   methods: {
      ...mapActions(['getUserInfo']),
      goReviewDetail(review){
         this.$router.push({
         name: 'ReviewDetail',
         params : {
            reviewId : review
         }
         })
      },  
   },
   computed: {
      ...mapState(['userInfo']),
      alpha() {
         return 99 / this.rMovies[0].score
      }
   },
   watch: {
      userInfo() {
         if (this.userInfo){
            this.myInfo = this.userInfo.user_data
            this.myMovies = this.userInfo.user_moviedata
            this.myReviews = this.userInfo.user_data.reviews
            this.myComments = this.userInfo.user_data.comments
            this.rMovies2 = JSON.parse(this.userInfo.user_recommendation)
            this.rMovies = this.userInfo.r_movies
            
            const newRMovies = []
            const getScore = function (now_movie, target_movies) {
               let score = null
               target_movies.forEach(target_movie => {
                  if (target_movie.target_id === now_movie.id) {
                     score = target_movie.score
                  }
               })
               return score
            }

            const target_movies = this.rMovies2
            this.rMovies.forEach(movie => newRMovies.push({
               ...movie,
               score: getScore(movie, target_movies)
            })
            )
            this.rMovies = _.sortBy(newRMovies, 'score').reverse()

            if (this.myReviews.length > 0) {
               this.reviewNotEmpty = true
            }
            if (this.myComments.length > 0) {
               this.commentNotEmpty = true
            }
         } else {
            this.myReviews = null
            this.myComments = null
            this.myInfo = null
            this.myMovies = null
            this.reviewNotEmpty = false
            this.commentNotEmpty = false
            this.rMovies = null
            this.rMovies2 = null
         }
      },
   },
   created() {
      this.getUserInfo()
   },

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

.review-box {
   height: 400px;
}

.comment-box {
   height: 200px;
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

.go-review {
  cursor: pointer
}
</style>