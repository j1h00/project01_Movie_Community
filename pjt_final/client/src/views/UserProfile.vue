<template>
   <div v-if="nowUserInfo">
      <!-- Header -->
      <div class="h-10">
      </div>
      <h1 class="ml-3 mt-5 p-3 text-3xl font-bold">{{ nowUserInfo.user_data.username }}</h1>

      <section class="bg-gray-100">
         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">{{ nowUserInfo.user_data.username }}님이 평가한 영화</h1>
         <div v-if="userMovies && userMovies.length" class="movie-section p-5 h-full flex flex-wrap flex-col gap-10 overflow-x-scroll wrapper-box ml-3">
            <div v-for="(movie, idx) in userMovies" :key="idx" class="movie-card py-4 px-4 bg-whit w-72 bg-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition duration-500 mx-auto md:mx-0">
               <movie-card :movie="movie"></movie-card>
            </div>
         </div>

         <div v-else>
         <h1 class="ml-7 text-lg">검색 결과가 없습니다.</h1>
         </div>

         <h1 class="border-t-2 ml-3 mt-5 p-3 text-xl font-bold">{{ nowUserInfo.user_data.username }}님이 작성한 리뷰</h1>
         <div v-if="reviewNotEmpty" class="review-box">
            <div class="h-full flex flex-wrap flex-col justify-start items-center overflow-x-scroll gap-6 wrapper-box ml-3 pb-3">
               <div v-for="(review, idx) in userReviews" :key="idx" class="w-72 md:w-96 h-full">
                  <review-card :review="review"></review-card>
               </div>
            </div>
         </div>
         <div v-else>
            <h1 class="ml-3 mt-1 p-3 text-xl">아직 작성된 리뷰가 없습니다.</h1>
         </div>
      </section>
   </div>
</template>

<script>
import MovieCard from '@/components/MovieCard.vue'
import ReviewCard from '@/components/ReviewCard.vue'

import axios from 'axios'

export default {
   name : 'UserProfile',
   components: {
      MovieCard, ReviewCard
   },
   data (){
      return{
         nowUserInfo: null,

         userMovies: null,
         userReviews: null,

         reviewNotEmpty: false,
      }
   },
   methods: {
      goReviewDetail(review){
         this.$router.push({
         name: 'ReviewDetail',
         params : {
            reviewId : review
         }
         })
      },  
      getOthersUserInfo() {
         axios({
            method : 'get',
            url : `http://127.0.0.1:8000/accounts/profile/${this.$route.params.userId}/`,
         })
            .then(res => {
               this.nowUserInfo = res.data
               this.userMovies = this.nowUserInfo.user_moviedata
               this.userReviews = this.nowUserInfo.user_data.reviews
               if (this.userReviews.length > 0) {
                  this.reviewNotEmpty = true
               }
            })
            .catch(err => console.log(err))
      }
   },
   computed: {
      
   },
   watch: {
      nowUserInfo() {
         this.userMovies = this.nowUserInfo.user_moviedata
         this.userReviews = this.nowUserInfo.user_data.reviews
         if (this.userReviews.length > 0) {
            this.reviewNotEmpty = true
         }
      },
   },
   created() {
      this.getOthersUserInfo()
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