<template>
  <Carousel :autoplay="7000" :wrap-around="true" class="h-full">
    <Slide v-for="movie in movies" :key="movie">
      <div class="movie-img">
        {{ movie }}
      </div>
    </Slide>
    <template #addons>
      <Pagination />
    </template>
  </Carousel>
</template>

<script>
import 'vue3-carousel/dist/carousel.css';
import { Carousel, Slide, Pagination,  } from 'vue3-carousel';

export default {
  name: 'HomeHeader',
  components: {
    Carousel, Slide, Pagination, 
  },
  props: {
    movies: Object
  },
  methods: {
    getImgUrl: function(url){
      const imgUrl = `https://image.tmdb.org/t/p/original/${url}`
      return imgUrl
    },
  }
}
</script>

<style scoped>
.carousel__slide {
  padding: 10px;
}

.carousel__prev,
.carousel__next {
  box-sizing: content-box;
  border: 5px solid white;
}

.movie-img {
  height: 400px;
}
</style>