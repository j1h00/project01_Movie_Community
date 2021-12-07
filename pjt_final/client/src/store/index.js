import axios from 'axios'
import router from '../router';
import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoggedIn: false,
    userInfo: null,
    myCreatedReview: null,
    searchInput: '',
    movieDetail: null,
    reviewDetail: null,
    similarMovies: null,
    movieAverageRating: null,
    myStarRating : null,
    reviewData : null,
  },
  mutations: {
    // Login Signup
    INIT(state) {
      state.isLoggedIn = true
    },
    ON_LOGOUT(state) {
      state.isLoggedIn = false
      state.userInfo = null
      state.myCreatedReview = null
    },
    ON_LOGIN(state) {
      state.isLoggedIn = true 
    },
    UPDATE_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
    },

    // SearchBar
    CHANGE_SEARCH_INPUT(state, searchInput) {
      state.searchInput = searchInput
    },

    // MovieDetail
    SAVE_MOVIE_DETAIL(state, movieDetail) {
      state.movieDetail = movieDetail
    },

    SAVE_REVIEW_DETAIL(state, reviewDetail) {
      state.reviewDetail = reviewDetail
    },

    SAVE_SIMILAR_MOVIES(state, similarMovies) {
      state.similarMovies = similarMovies
    },

    ON_CREATED_REVIEW(state, createdReview) {
      state.myCreatedReview = createdReview
    },

    SET_STAR_RATING(state, starRating){
      state.myStarRating = starRating
    },

    SET_AVERAGE_RATING(state, movieAverageRating){
      state.movieAverageRating = movieAverageRating
    },

    SET_REVIEW_DATA(state, reviewdata){
      state.reviewData = reviewdata
    },
  },
  actions: {
    // Login Signup
    init({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (token) {
        commit('INIT')
        dispatch('getUserInfo')
      }
    },
    onLogout({ commit }) {
      localStorage.removeItem('token')
      router.go()
      commit('ON_LOGOUT')
    },
    onLogin({ commit }) {
      commit('ON_LOGIN')
    },
    loginAfterSignup({ commit, dispatch }, credentials) {
      const token = localStorage.getItem('token')
      if (token) {
        router.push({ name: 'Home' })
      } else {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/accounts/login/',
          data: credentials,
        })
          .then(res => {
            localStorage.setItem('token', res.data.key)
            commit('ON_LOGIN')
            return res.data.key
          })
          .then(() => dispatch('getUserInfo'))
          .catch(err => console.error(err))
      }
    },
    getUserInfo({ commit }) {
      const token = localStorage.getItem('token')
      if (token) {
        axios({
          method : 'get',
          url : `http://127.0.0.1:8000/accounts/profile/myprofile/`,
          headers : {
              Authorization: `Token ${token}`
          },
        })
          .then(res => {
            commit('UPDATE_USER_INFO', res.data)
          })
          .catch(err => console.log(err))
      }
    },
    // SearchBar
    changeSearchInput({ commit }, searchInput) {
      commit('CHANGE_SEARCH_INPUT', searchInput)
    },
    
    // MovieDetail
    saveMovieDetail({ commit }, movieDetail) {
      commit('SAVE_MOVIE_DETAIL', movieDetail)
    },

    saveReviewDetail({ commit }, reviewDetail) {
      commit('SAVE_REVIEW_DETAIL', reviewDetail)
    },

    saveSimilarMovies({ commit }, similarMovies) {
      commit('SAVE_SIMILAR_MOVIES', similarMovies)
    },

    onCreatedReview({ commit }, createdReview) {
      commit('ON_CREATED_REVIEW', createdReview)
    },

    setStarRating({commit}, starRating){
      commit('SET_STAR_RATING', starRating)
    },

    setAverageRating({ commit }, movieAverageRating){
      commit('SET_AVERAGE_RATING', movieAverageRating)
    },

    setReviewData({ commit }, reviewdata){
      commit('SET_REVIEW_DATA', reviewdata)
    },
  },
  modules: {
  }
})
