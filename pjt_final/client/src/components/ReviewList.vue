<template>
  <div v-if="reviewNotEmpty" class="h-full">
    <div class="h-full flex flex-wrap flex-col justify-start items-center overflow-x-scroll gap-6 wrapper-box ml-3 pb-3">
      <div v-for="review in reviews" :key="review" class="w-72 md:w-96 h-full">
        <review-card :review="review"></review-card>
      </div>
    </div>
  </div>
  <div v-else>
    <h1 class="ml-3 mt-1 p-3 text-xl">아직 작성된 리뷰가 없습니다.</h1>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions, mapState } from 'vuex'
import _ from 'lodash'
import ReviewCard from '@/components/ReviewCard.vue'

export default {
  name: 'ReviewList',
  components: {
    ReviewCard,
  },
  data: function () {
    return {
      reviews: null, 
      like_info : [],
      loading_sources: true,
      reviewNotEmpty: false,
      test: _.range(5)
    }
  },
  computed: {
    ...mapState(['movieDetail', 'myCreatedReview', 'movieAverageRating']),
  },
  methods: {
    ...mapActions(['setAverageRating']),
    getReviewListByMovie() {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/reviews/bymovie/${this.movieDetail.id}/`,
      })
        .then(res => {
          if (res.data.length > 0) {
            this.reviews = res.data
            this.reviewNotEmpty = true
            this.setAverageRating(this.averageRating())
          } else {
            this.reviews = null,
            this.reviewNotEmpty = false
            this.setAverageRating(null)
          }
          this.loading_sources = false
        })
        .catch(err => console.error(err))
    },
    go(review){
      this.$router.push({
        name: 'ReviewDetail',
        params : {
          reviewId : review.id,
        }
      })
    },
    averageRating() {
      let ratings = 0
      this.reviews.forEach(review => ratings += review.rating)
      return ratings / this.reviews.length
    },
  },
  created() {
    this.getReviewListByMovie()
  },
  watch: {
    myCreatedReview: function () {
      this.getReviewListByMovie()
    }
  }
}
</script>

<style scoped>
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