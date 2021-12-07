<template>
  <div v-if="review_data">
    <div class="absolute bg-cover bg-center backdrop-box z-0" 
      :style="{ 'background-image': 'url(' + getBackdropImgUrl + ')' }">
    </div>
    <div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center">
      <movie-modal ></movie-modal>
      <!-- <img :src="getBackdropImgUrl" alt="" class="absolute z-0"> -->
      <div class="title relative z-5">
        <h1 class="text-white font-bold text-6xl cursor-pointer" @click="toMovieDetail(review_data.movie.id)">
          {{ review_data.movie.title }}
        </h1>
      </div>
      <div class="relative container mx-auto flex justify-center items-center z-5">
        <div class="w-2/3 md:1/2 lg:w-1/3 h-2/3 bg-white rounded-lg shadow-lg " v-if="review_data">
          <div class="w-full h-96 flex flex-row" >
            <div class="w-full h-full text-left p-6 md:p-4">
              <div class="h-5/6 w-full">
                <div class="h-full detail-box">
                  <div class="pointer-box" @click="goUserProfile(review_data.user.id)">
                    <p class="text-xl text-gray-700 font-bold">{{ review_data.user.username }}</p> 
                    <span class="text-xs text-gray-400">{{ (review_data.created_at === review_data.updated_at) ? "생성시간 " + parse(review_data.created_at) : parse(review_data.updated_at) + " 수정됨" }}</span>
                  </div>
                  <star-rating :rating="changeRating" :read-only="true" :increment="0.5" :show-rating="false" :star-size="20"></star-rating>
                  <hr>
                  <div class="pt-3 h-3/4 w-full">
                    <!-- <div v-if="editMode" class="w-full">
                      <input v-model="contentInput" type="text" placeholder="리뷰를 작성해주세요." class="p-5 mb-5 bg-white border border-gray-200 rounded shadow-sm" id="">
                    </div> -->
                    <div>
                      <p class="break-words text-base text-gray-700">{{ review_data.content }} </p>
                    </div>
                  </div>
                </div>
              </div>
              <hr>
              <div class="w-full flex justify-between">
                <p>{{ review_data.like_users.length }}개의 추천이 있습니다.</p>
                <div v-if="userInfo && (review_data.user.id === userInfo.user_data.id)" class="flex jutify-center gap-2">
                  <button @click="toggleModal" class="flex jutify-center items-center ml-2">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                      <path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"/>
                    </svg>
                    edit
                  </button>
                  <button @click="deleteMyReview" class="flex jutify-center items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                      <path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.12 10.47L12 12.59l-2.13-2.12-1.41 1.41L10.59 14l-2.12 2.12 1.41 1.41L12 15.41l2.12 2.12 1.41-1.41L13.41 14l2.12-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4zM6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9z"/>
                    </svg>
                    delete 
                  </button>
                </div>
              </div>
              
              <div class="pt-3 flex justify-start">
                <div v-if="userInfo">
                  <div v-if="like_info.isLike">
                    <button @click="Like(review_data.id)" class="text-gray-500 hover:text-gray-600">
                      <svg class="animate-bounce" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                        <path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                      </svg>
                    </button>
                  </div>
                  <div v-else>
                    <button @click="Like(review_data.id)" class="text-gray-500 hover:text-gray-600">
                      <svg class="animate-bounce" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                        <path d="M0 0h24v24H0V0z" fill="none"/><path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>
                      </svg>
                    </button>
                  </div>
                </div>
                <div v-else>
                  <button @click="toggleLoginModal" class="text-gray-500 hover:text-gray-600">
                    <svg class="animate-bounce" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                      <path d="M0 0h24v24H0V0z" fill="none"/><path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 생성 -->
          <div v-if="userInfo">
            <strong v-if="errorMessage">
              {{ errorMessage }}
            </strong>
            <div class="flex items-center p-3">
              <input
                class="p-3 block w-full border-black bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0"
                minlength="1"
                maxlength="50"
                type="text" 
                v-model="title" 
                @keyup.enter="createComment(review_data.id)"
              >
              <button class="write-button ml-5 bg-blue-500 text-gray-100 text-xs rounded-lg focus:border-4 border-blue-300" @click="createComment(review_data.id)">
                <p>write</p>
              </button>
            </div>
          </div>
          <div v-else>
            <div class="flex items-center p-3">
              <input
                class="p-3 block w-full border-black bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0"
                placeholder="댓글을 작성하려면 로그인하세요."
                type="text" 
                disabled
              >
            </div>
          </div>
          <!-- 리스트 -->
          <div class="space-y-4 mx-2 mb-2" v-for="(comment, idx) in comments" :key="idx">
            <div>
              <comment-card :comment="comment" @comment-deleted="getComments(review_data.id)"></comment-card>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import CommentCard from '@/components/CommentCard.vue'
import MovieModal from '@/components/MovieModal.vue'

import axios from 'axios'
import { mapState, mapActions } from 'vuex'
import StarRating from 'vue-star-rating'

export default {
  name : 'ReviewDetail',
  components: {
    StarRating, CommentCard, MovieModal
  },
  data: function(){
    return {
      editMode: false,
      review_data : null,
      like_info: null,
      title: '',
      errorMessage: '',
      comments: null,
    }
  },
  methods: {
    ...mapActions(['saveReviewDetail']),
    setToken() {
      const token = localStorage.getItem('token')
      return {
        Authorization: `Token ${token}`
      }
    },
    toggleEditMode() {
      this.editMode = !this.editMode 
    },
    parse(time){
      const date = time.slice(0, 10)
      const hour = String((parseInt(time.slice(11,13))+9) % 24)+":"
      const minute = time.slice(14,19)
      return date + ' ' + hour + minute
    },
    toggleModal() {
      const modal = document.querySelector(".modal");
      modal.classList.toggle("hidden");
    },
    Like(reviewId) {
      axios({
        method: 'POST',
        url: `http://127.0.0.1:8000/reviews/${reviewId}/likes/`,
        headers: this.setToken()
      })
        .then(res => {
          this.like_info = res.data
          if (this.like_info.isLike){
            this.review_data.like_users.push(this.userInfo.user_data.id)
          } else {
              const index = this.review_data.like_users.indexOf(this.userInfo.user_data.id)
              if (index > -1){
                this.review_data.like_users.splice(index, 1)
              }
          }
        })
        .catch(err => console.error(err))
    },
    ReviewDetail(reviewId) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/reviews/detail/${reviewId}/`,
        // headers: this.setToken()
      })
        .then(res => {
          this.review_data = res.data
          this.saveReviewDetail(this.review_data)
          this.like_info = { isLike : this.userInfo ? this.review_data.like_users.includes(this.userInfo.user_data.id) : false}
        })
        .catch(err => console.error(err))
    },
    createComment(reviewId) {
      if (this.userInfo) {
        this.errorMessage = ''
        if (this.title.length < 1 || this.title.length > 50) {
          this.errorMessage = 'title is too long or short'
        }
        else {
          axios({
            method: 'POST',
            url: `http://127.0.0.1:8000/reviews/${reviewId}/comments/create/`,
            data: {
              content: this.title,
            },
            headers: this.setToken()
          })
            .then(() => { 
              this.getComments(reviewId)
              this.title = ''
            })
            .catch(err => console.error(err))
        }
      } else {
        this.toggleLoginModal()
      }
    },
    getComments(reviewId) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/reviews/${reviewId}/comments/`,
      })
        .then(res => {
          this.comments = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteComment(reviewId, comment) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/reviews/${reviewId}/comments/${comment.id}/`,
        headers: this.setToken()
      })
        .then(() => {
          this.getComments(reviewId)
        })
        .catch(err => console.error(err))
    },
    deleteMyReview(){
      var m = confirm( '정말로 리뷰를 삭제하시겠습니까?' );
      if (m) {
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/reviews/${this.$route.params.reviewId}`,
          headers: this.setToken()
        })
        .then(() => {
          this.$router.go(-1)
        })
        .catch(err => console.error(err))
        }
    },
    goUserProfile(userId) {
      this.$router.push({
        name: 'UserProfile',
        params : {
          userId : userId
        }
      })
    },
    toMovieDetail(movieId) {
      this.$router.push({
        name: 'MovieDetail',
        params : { movieId: movieId }
      })
    },
  },
  created: function(){
    this.ReviewDetail(this.$route.params.reviewId)
    this.getComments(this.$route.params.reviewId)  
  },
  computed: {
    ...mapState(['userInfo', 'myCreatedReview']),
    changeRating() {
      return this.review_data.rating / 2
    },
    getBackdropImgUrl: function(){ 
      const imgUrl = `https://image.tmdb.org/t/p/original/${this.review_data.movie.backdrop_path}`
      return imgUrl
    },
  },
  watch: {
    myCreatedReview(){
      this.review_data = this.myCreatedReview
      this.ReviewDetail(this.$route.params.reviewId)
    },
  }
}
</script>

<style>
.write-button  {
  width: 50px;
  height: 30px;
}

.pointer-box {
  cursor: pointer
}
.backdrop-box {
  width: 100%;
  height: 800px;
}
.title {
  margin-top: 200px;
  padding-bottom: 50px;
}
/* .poster-img {
  object-fit: cover;
}
.backdrop-hanger {
  margin-bottom: 200px;
}

.backdrop-box {
  width: 100%;
  height: 1000px;
} */
</style>