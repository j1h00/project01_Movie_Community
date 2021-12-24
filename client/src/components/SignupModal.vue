<template>
  <div class="signup-modal flex justify-center items-center antialiased hidden">
    <div class="modal__overlay"></div>
    <div class="relative w-8/12 sm:w-4/6 lg:w-1/2 max-w-md mx-auto">
        <div class="card bg-gray-800 shadow-lg  w-full h-full rounded-3xl absolute  transform -rotate-6"></div>
        <div class="card bg-blue-900 shadow-lg  w-full h-full rounded-3xl absolute  transform rotate-6"></div>
        <div class="relative w-full rounded-3xl  px-6 py-4 bg-gray-100 shadow-md">
          <div class="flex flex-row justify-between p-6">
            <label for="" class="block mt-3 text-sm text-gray-700 text-center font-semibold">
                Signup
            </label>
            <button @click="toggleSignupModal">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div>
              <input v-model="credentials.username" type="username" placeholder="  사용자 이름을 입력해주세요." class="p-3 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">
          </div>
          <div v-if="errorMessage.username" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.username.toString() }}
          </div>
          <div class="mt-7">                
              <input v-model="credentials.password1" type="password" placeholder="  비밀번호를 입력해주세요." class="p-3 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">                           
          </div>
          <div v-if="errorMessage.password1" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.password1.toString() }}
          </div>
          <div class="mt-7">                
              <input @keyup.enter="signup" v-model="credentials.password2" type="password" placeholder="  비밀번호 확인" class="p-3 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">                           
          </div>
          <div v-if="errorMessage.password2" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.password2.toString() }}
          </div>
          <div class="mt-7">
              <button @click="signup" class="bg-blue-900 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                  Signup
              </button>
          </div>
  
          <div class="flex mt-7 items-center text-center">
            <hr class="border-gray-300 border-1 w-full rounded-md">
          </div>

          <div class="mt-7">
            <div class="flex justify-center items-center">
                <label class="mr-2" >계정이 있으신가요?</label>
                <button @click="changeModal" class=" text-blue-500 transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                  login
                </button>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
  name: 'LoginModal',
  data: function(){
    return{
      credentials: {
        username: null,
        password1: null,
        password2: null,
      },
      errorMessage: ''
    }
  },
  methods: {
    ...mapActions(['loginAfterSignup']),
    changeModal() {
      this.toggleLoginModal()
      this.toggleSignupModal()
    },
    toggleSignupModal() {
      const signupModal = document.querySelector(".signup-modal");
      signupModal.classList.toggle("hidden");
    },
    toggleLoginModal() {
      const loginModal = document.querySelector(".login-modal");
      loginModal.classList.toggle("hidden");
    },
    signup() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: this.credentials
      })
        .then(() => {
          const credentials = {
            username: this.credentials.username,
            password: this.credentials.password2
          }

          this.loginAfterSignup(credentials)

          this.credentials = {
            username: null,
            password1: null,
            password2: null,
          }

          this.toggleSignupModal()
        })
        .then(() => this.$router.push({ name: 'SetUser' }))
        .catch(err => {
          this.errorMessage = err.response.data
        })
    }
  },
  created() {
  }
}
</script>

<style>
.signup-modal {
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