<template>
  <header>
    <div 
      class="h-96 bg-cover bg-center backdrop-box" 
      :style="{ 'background-image': 'url(' + getBackdropImgUrl + ')' }">
      <div class="max-w-6xl poster-hanger invisible md:visible">
        <div class="-mb-8 ml-3 poster-box border border-gray-200">
          <img :src="getPosterImgUrl" alt="" class="poster-img">
        </div>
      </div>
    </div>
    <div class="w-full bg-white shadow-xl p-2 h-80">
      <div class="w-full h-full p-2 header-detail">
        <div class="h-full md:ml-60">
          <div class="w-full h-full rounded md:col-span-9">
            <div class="w-full h-full grid grid-col-4 grid-rows-5">
              <div class="w-full pl-5 row-span-2 col-span-4 flex items-end">
                <div class="flex flex-col">
                  <h1 class="text-3xl font-extrabold">{{ movie.title }}</h1>
                  <h5 class="px-1">{{ movie.original_title }}</h5>
                </div>
              </div>
              <div class="w-full pl-5 row-span-1 col-span-4 flex items-start ">
                <h1 class="mt-1 pb-2 border-b-2">{{ movie.release_date }} ◾ {{ genresByName }} ◾ {{ movie.runtime }}분</h1>
              </div>
              <div v-if="myReview" class="row-span-2 col-span-4 grid grid-col-2">
                <div class="px-1 pb-1 pl-5 -mt-4 col-span-1 flex items-center">
                  <div class="flex flex-col items-center">
                    <p class="text-xs">내 평점 </p>
                    <star-rating class="pb-3 border-b-2 border-yellow-200" :rating="changeMyRating" :read-only="true" :increment="0.5" :show-rating="false" :star-size="40"></star-rating>
                  </div>
                </div>
                <div class="pl-5 p-2 col-span-1 flex items-center justify-between">
                  <div class="w-3/4 flex-shrink border-r-2">
                    <p v-if="myReview.content">{{ myReview.content.slice(0,50) }} ... </p>
                  </div>
                  <div class="flex jutify-center flex-grow gap-2">
                    <button @click="toggleModal" class="flex jutify-center items-center ml-2">
                      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                        <path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"/>
                      </svg>
                      <p>edit</p>
                      <!-- <p v-if="myReview.content">edit</p> -->
                      <!-- <p v-else>글 리뷰를 작성해주세요!</p> -->
                    </button>
                    <button @click="deleteMyReview" class="flex jutify-center items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                        <path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.12 10.47L12 12.59l-2.13-2.12-1.41 1.41L10.59 14l-2.12 2.12 1.41 1.41L12 15.41l2.12 2.12 1.41-1.41L13.41 14l2.12-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4zM6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9z"/>
                      </svg>
                      delete 
                    </button>
                  </div>
                </div>
              </div>

              <div v-else class="row-span-2 col-span-4 grid grid-col-4">
                <div class="px-1 pb-1 pl-5 -mt-4 col-span-1 flex items-center">
                  <div class="flex flex-col items-center">
                    <p class="text-xs">평균 평점 {{ Math.round((movieAverageRating + Number.EPSILON) * 100) / 100 }}</p>
                    <star-rating class="pb-3 border-b-2 border-yellow-200" :rating="changeAvgRating" :read-only="true" :increment="0.01" :show-rating="false" :star-size="40"></star-rating>
                  </div>
                </div>
                <div class="relative col-span-3">
                  <div v-if="!isLoggedIn" @click="toggleLoginModal" class="need-login h-full w-full flex justify-center items-center">
                    <h1 class="font-bold">로그인이 필요합니다.</h1> 
                  </div>
                  <div class="h-full flex justify-evenly" :class="{ 'login-blur': !isLoggedIn }">
                    <div class="flex items-center review-button">
                      <button @click="toggleModal" class="flex">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                          <path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"/>
                        </svg>
                        <p>리뷰작성</p>
                      </button>
                    </div>
                    <div class="flex items-center">
                      <button class="flex">
                        <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                          <g><rect fill="none" height="24" width="24"/></g>
                          <g><path d="M14,10H3v2h11V10z M14,6H3v2h11V6z M18,14v-4h-2v4h-4v2h4v4h2v-4h4v-2H18z M3,16h7v-2H3V16z"/></g>
                        </svg>
                        <p>보고싶은 영화에 추가</p>
                      </button>
                    </div>
                    <div class="flex items-center">
                      <button class="flex">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/>
                        <path d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"/></svg>
                      </button>
                      <p>보는중</p>
                    </div>
                    <div class="flex items-center">
                      <button class="flex">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                          <path d="M0 0h24v24H0V0zm0 0h24v24H0V0zm0 0h24v24H0V0zm0 0h24v24H0V0z" fill="none"/><path d="M12 6c3.79 0 7.17 2.13 8.82 5.5-.59 1.22-1.42 2.27-2.41 3.12l1.41 1.41c1.39-1.23 2.49-2.77 3.18-4.53C21.27 7.11 17 4 12 4c-1.27 0-2.49.2-3.64.57l1.65 1.65C10.66 6.09 11.32 6 12 6zm-1.07 1.14L13 9.21c.57.25 1.03.71 1.28 1.28l2.07 2.07c.08-.34.14-.7.14-1.07C16.5 9.01 14.48 7 12 7c-.37 0-.72.05-1.07.14zM2.01 3.87l2.68 2.68C3.06 7.83 1.77 9.53 1 11.5 2.73 15.89 7 19 12 19c1.52 0 2.98-.29 4.32-.82l3.42 3.42 1.41-1.41L3.42 2.45 2.01 3.87zm7.5 7.5l2.61 2.61c-.04.01-.08.02-.12.02-1.38 0-2.5-1.12-2.5-2.5 0-.05.01-.08.01-.13zm-3.4-3.4l1.75 1.75c-.23.55-.36 1.15-.36 1.78 0 2.48 2.02 4.5 4.5 4.5.63 0 1.23-.13 1.77-.36l.98.98c-.88.24-1.8.38-2.75.38-3.79 0-7.17-2.13-8.82-5.5.7-1.43 1.72-2.61 2.93-3.53z"/>
                        </svg>
                        <p>관심없어요</p>
                      </button>
                      </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from 'axios'
import StarRating from 'vue-star-rating'

export default {
  name: 'MovieDetailHeader',
  components: {
    StarRating
  },
  data: function () {
    return {
      movie: this.movieDetail,
      myReview: null,
    }
  },
  methods: {
    ...mapActions(['onCreatedReview']),
    toggleModal() {
      const modal = document.querySelector(".modal");
      modal.classList.toggle("hidden");
    },
    toggleLoginModal() {
      const loginModal = document.querySelector(".login-modal");
      loginModal.classList.toggle("hidden");
    },
    getMyReview() {
      const token = localStorage.getItem('token')
      if (token) {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/reviews/myreview/${this.movie.id}/`,
          headers: {
            Authorization: `Token ${token}`
          },
        })
          .then(res => {
            this.myReview = res.data[0]
            this.onCreatedReview(this.myReview)
          })
          .catch(err => console.error(err))
      } else {
        this.myReview = null
      }
    },
    deleteMyReview() {
      const token = localStorage.getItem('token')
      if (token) {
        axios({
          method: 'delete',
          url: `http://127.0.0.1:8000/reviews/${this.myReview.id}`,
          headers: {
            Authorization: `Token ${token}`
          },
        })
          .then(() => {
            this.myReview = null
            this.onCreatedReview(null)
          })
          .catch(err => console.error(err))
      }
    },
  },
  computed: {
    ...mapState(['isLoggedIn', 'movieDetail', 'myCreatedReview', 'movieAverageRating']),
    getPosterImgUrl: function(){
      const imgUrl = `https://image.tmdb.org/t/p/original/${this.movie.poster_path}`
      return imgUrl
    },
    getBackdropImgUrl: function(){ 
      const imgUrl = `https://image.tmdb.org/t/p/original/${this.movie.backdrop_path}`
      return imgUrl
    },
    genresByName() {
      const genres = [] 
      this.movie.genres.forEach(genre => genres.push(genre.name))
      return genres.join('/')
    },
    changeMyRating() {
      return this.myReview.rating / 2
    },
    changeAvgRating() {
      return Math.round((this.movieAverageRating + Number.EPSILON) * 100) / 100 / 2
    },
  },
  watch: {
    isLoggedIn: function() {
      this.getMyReview()
    },
    myCreatedReview: function () {
      this.myReview = this.myCreatedReview
    },
  },
  created() {
    this.movie = this.movieDetail
    this.getMyReview()
  }
}
</script>

<style scoped>
@import "https://fonts.googleapis.com/icon?family=Material+Icons";
      
.poster-hanger {
  max-width: 960px;
  margin: 0px auto;
  height: 10px;
}

.poster-box{
  position: relative;
  width: 222px;
  height: 333px;
  box-shadow: rgb(0 0 0 / 30%) 0px 0px 2px;
  z-index: 10;
}

.poster-img {
  vertical-align: top;
  object-fit: cover;
  transition: opacity 420ms ease 0s;
}

.backdrop-box {
  padding: 350px 0px 0px;
}

.header-detail {
  max-width: 960px;
  margin: 0px auto;
}

.need-login { 
  background: rgb(0, 0, 0, 0.1);
  position: absolute;
  cursor: pointer;
  z-index: 99;
}
.login-blur {
  --tw-blur: blur(24px);
  opacity: 0.2;
}
</style>