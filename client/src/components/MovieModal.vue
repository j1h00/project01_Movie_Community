<template>
  <div class="modal flex justify-center items-center antialiased hidden">
    <div class="modal__overlay"></div>
    <div class="modal__content flex flex-col w-11/12 sm:w-5/6 lg:w-1/2 max-w-2xl mx-auto rounded-lg border border-gray-300 shadow-xl">
    
      <!-- 상단 -->
      <div class="flex flex-row justify-between p-6 bg-white border-b border-gray-200 rounded-tl-lg rounded-tr-lg">
        <!-- <p class="font-semibold text-gray-800">{{ movie.title }}</p> -->
        <button @click="toggleModal">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>

      </div>

      <!-- body -->
      <div class="flex flex-col px-6 py-5 bg-gray-50">
        <div>
          <p class="mb-2 font-semibold text-gray-700">평점</p>
          <star-rating 
            :increment="0.5"
            :show-rating="false" 
            :rating="rating"
            @update:rating="rating = $event">
          </star-rating>
          <div style="margin-top:10px;font-weight:bold;">{{currentRatingText}}</div>
        </div>
        <p class="mb-2 font-semibold text-gray-700">리뷰</p>
        <textarea v-model="contentInput" type="text" placeholder="리뷰를 작성해주세요." class="p-5 mb-5 bg-white border border-gray-200 rounded shadow-sm h-40" id=""></textarea>
        <div class="flex flex-col sm:flex-row items-center mb-5 sm:space-x-5"></div>
        <div class="flex items-center mt-5 mb-3 space-x-4"></div>
      </div>
      <div class="flex flex-row items-center justify-between p-5 bg-white border-t border-gray-200 rounded-bl-lg rounded-br-lg">
        <button @click="toggleModal">
          <p class="font-semibold text-gray-600">Cancel</p>
        </button>
        <button @click="requestCreateReview" class="px-4 py-2 text-white font-semibold bg-blue-500 rounded">
          Save
        </button>
      </div>
    </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import axios from 'axios'
import StarRating from 'vue-star-rating'

export default {
  name: 'MovieModal',
  components: {
    StarRating
  },
  data: function(){
    return{
      movie: null,
      contentInput: null,
      rating: null, // 별점선택 0.5단위로 올라감 
    }
  },
  methods: {
    ...mapActions(['onCreatedReview']),
    toggleModal() {
      const modal = document.querySelector(".modal");
      modal.classList.toggle("hidden");
    },
    requestCreateReview() {
      if (this.$route.name === 'ReviewDetail'){
        const token = localStorage.getItem('token') 
        axios({
          method: 'PUT',
          url: `http://127.0.0.1:8000/reviews/${this.$route.params.reviewId}/`, // movie pk 받음
          headers: {
            Authorization: `Token ${token}`
          },
          data: {
            rating: parseInt(parseFloat(this.rating)*2),
            content: this.contentInput,
          }
        })
          .then((res) => {
            this.contentInput = res.data.content
            this.rating = res.data.rating / 2
            // this.setStarRating(parseInt(parseFloat(this.rating)*2))
            this.onCreatedReview(res.data)
            this.toggleModal()
          })
          .catch(err => console.error(err))
      } else if (this.myCreatedReview) {
        const token = localStorage.getItem('token') 
        axios({
          method: 'PUT',
          url: `http://127.0.0.1:8000/reviews/${this.myCreatedReview.id}/`, // movie pk 받음
          headers: {
            Authorization: `Token ${token}`
          },
          data: {
            rating: parseInt(parseFloat(this.rating)*2),
            content: this.contentInput,
          }
        })
          .then((res) => {
            this.contentInput = res.data.content
            this.rating = res.data.rating / 2
            // this.setStarRating(parseInt(parseFloat(this.rating)*2))
            this.toggleModal()
            this.onCreatedReview(res.data)
          })
          .catch(err => console.error(err))
      } else {
        const token = localStorage.getItem('token')
        axios({
          method: 'post',
          url: `http://127.0.0.1:8000/reviews/create/${this.movieDetail.id}/`,
          headers: {
            Authorization: `Token ${token}`
          },
          data: {
            rating: parseInt(parseFloat(this.rating)*2),
            content: this.contentInput,
          }
        })
          .then((res) => {
            // this.setStarRating(parseInt(parseFloat(this.rating)*2))
            this.toggleModal()
            this.onCreatedReview(res.data)
          })
          .catch(err => console.error(err))
      }
    },
  },
  computed: {
    ...mapState(['movieDetail','myCreatedReview', 'reviewDetail']),
    currentRatingText() {
      return this.rating
        ? "당신이 생각하는 점수는" + parseInt(parseFloat(this.rating)*2) + "점이군요"
        : "원하는 점수 만큼 별을 선택해주세요";
    },
  },
  created() {
    this.movie = this.movieDetail
  },
  watch: {
    reviewData(){
      this.movie = this.reviewData
    },
    myCreatedReview(){
      if (this.myCreatedReview){
        this.contentInput = this.myCreatedReview.content
        this.rating = this.myCreatedReview.rating / 2
      } else {
        this.contentInput = null
        this.rating = null
      }
    },
    reviewDetail() {
      if (this.reviewDetail) {
        this.contentInput = this.reviewDetail.content
        this.rating = this.reviewDetail.rating / 2
      } else {
        this.contentInput = null
        this.rating = null
      }
    },

  }
}
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 100;
}

.modal__overlay { 
  background: rgb(0, 0, 0, 0.6);
  width: 100%;
  height: 100%;
  position: absolute
}

.modal__content { 
  z-index: 101;
}
</style>