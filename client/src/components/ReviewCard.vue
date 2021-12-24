<template>
  <div class="w-full h-full bg-white border border-gray-200 rounded-lg shadow-lg flex flex-row" > 
    <div class="w-full text-left p-6 md:p-4">
      <div class="h-5/6 w-full" >
        <div class="h-full">
          <div class="pointer-box" @click="goUserProfile(review_data.user.id)">
            <p class="text-xl text-gray-700 font-bold">{{ review_data.user.username }}</p>
            <span class="text-xs text-gray-400">{{ (review_data.created_at === review_data.updated_at) ? "생성시간 " + parse(review_data.created_at) : parse(review_data.updated_at) + " 수정됨" }}</span>
          </div>
          <star-rating :rating="changeRating" :read-only="true" :increment="0.5" :show-rating="false" :star-size="20"></star-rating>
          <hr>
          <div class="h-3/4 pointer-box " @click="goReviewDetail(review)">
            <br>
            <p v-if="review_data.content" class="break-words text-base text-gray-700">{{ review_data.content.slice(0,180) }} ... </p>
          </div>
        </div>
      </div>
      <hr>
      <div>
        <p>{{ review_data.like_users.length }}개의 추천이 있습니다.</p>
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
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import StarRating from 'vue-star-rating'

export default {
  name : 'ReviewCard',
  components: {
    StarRating
  },
  props: {
    review : Object
  },
  data: function(){
    return {
      like_info: null,
      review_data: null,
    }
  },
  methods: {
    Like(reviewId) {
      const token = localStorage.getItem('token')
      axios({
        method: 'POST',
        url: `http://127.0.0.1:8000/reviews/${reviewId}/likes/`,
        headers: {
          Authorization : `Token ${token}`
        }
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
    parse(time){
      const date = time.slice(0, 10)
      const hour = String((parseInt(time.slice(11,13))+9) % 24)+":"
      const minute = time.slice(14,19)
      return date + ' ' + hour + minute
    },
    toggleLoginModal() {
      const loginModal = document.querySelector(".login-modal");
      loginModal.classList.toggle("hidden");
    },
    goReviewDetail(review){
      this.$router.push({
        name: 'ReviewDetail',
        params : {
          reviewId : review.id
        }
      })
    },
    goUserProfile(userId) {
      if (this.userInfo && (this.userInfo.user_data.id === userId)) {
          this.$router.push({ name: 'MyProfile'})
      } else {
        this.$router.push({
          name: 'UserProfile',
          params : {
            userId : userId
          }
        })
      }
    }
  },
  created: function(){
    this.review_data = this.review
    if (this.userInfo) {
      this.like_info = { isLike : this.review_data.like_users.includes(this.userInfo.user_data.id) }
    } else {
      false
    }
  },
  computed:{
    ...mapState(['userInfo']),
    changeRating() {
      return this.review_data.rating / 2
    }
  },
}
</script>

<style scoped>
.pointer-box {
  cursor: pointer
}

</style>