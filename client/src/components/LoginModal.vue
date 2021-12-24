<template>
  <div class="login-modal flex justify-center items-center antialiased hidden">
    <div class="modal__overlay"></div>
    <div class="relative w-8/12 sm:w-4/6 lg:w-1/2 max-w-md mx-auto">
        <div class="card bg-gray-800 shadow-lg  w-full h-full rounded-3xl absolute  transform -rotate-6"></div>
        <div class="card bg-blue-900 shadow-lg  w-full h-full rounded-3xl absolute  transform rotate-6"></div>
        <div class="relative w-full rounded-3xl  px-6 py-4 bg-gray-100 shadow-md">

          <!-- 상단 -->
          <div class="flex flex-row justify-between p-6">
            <label for="" class="block mt-3 text-sm text-gray-700 text-center font-semibold">
                Login
            </label>
            <button @click="toggleLoginModal">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <!-- body -->
          <div class="">
            <input v-model="credentials.username" type="username" placeholder="  사용자 이름을 입력해주세요." class="p-3 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">
          </div>
          <div v-if="errorMessage.username" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.username.toString() }}
          </div>
          <div class="mt-7">                
            <input @keyup.enter="login" v-model="credentials.password" type="password" placeholder="  비밀번호를 입력해주세요." class="p-3 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">                           
          </div>
          <div v-if="errorMessage.password" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.password.toString() }}
          </div>
          <div v-if="errorMessage.non_field_errors" class="text-md text-red-900">
            <span class="animate-ping text-sm rounded">!</span>
            {{ errorMessage.non_field_errors.toString() }}
          </div>
          <div class="mt-7">
            <button @click="login" class="bg-blue-900 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                Login
            </button>
          </div>
  
          <div class="flex mt-7 items-center text-center">
            <hr class="border-gray-300 border-1 w-full rounded-md">
            <p class="block font-medium text-sm text-gray-600 w-full">
                Social login
            </p>
            <hr class="border-gray-300 border-1 w-full rounded-md">
          </div>

          <div class="flex mt-7 justify-center w-full">
            <button class="mr-5 bg-gray-700 border-none px-4 py-2 rounded-xl cursor-pointer text-white shadow-xl hover:shadow-inner transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
              Facebook
            </button>

            <button class="bg-blue-900 border-none px-4 py-2 rounded-xl cursor-pointer text-white shadow-xl hover:shadow-inner transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
              Google
            </button>
          </div>

          <div class="mt-7">
            <div class="flex justify-center items-center">
                <label class="mr-2" >No account?</label>
                <button @click="changeModal" class=" text-blue-500 transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                  signup
                </button>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import axios from 'axios' 

export default {
  name: 'LoginModal',
  data: function(){
    return{
      credentials: {
        username: null,
        password: null,
      },
      errorMessage: ''
    }
  },
  methods: {
    ...mapActions(['getUserInfo', 'onLogin']),
    changeModal() {
      this.toggleLoginModal()
      this.toggleSignupModal()
    },
    toggleLoginModal() {
      const loginModal = document.querySelector(".login-modal");
      loginModal.classList.toggle("hidden");
    },
    toggleSignupModal() {
      const signupModal = document.querySelector(".signup-modal");
      signupModal.classList.toggle("hidden");
    },
    login() {
      const token = localStorage.getItem('token')
      if (token) {
        this.$router.push({ name: 'Home' })
      } else {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/accounts/login/',
          data: this.credentials,
        })
          .then(res => {
            localStorage.setItem('token', res.data.key)
            this.onLogin()
          })
          .then(() => this.getUserInfo())
          .then(() => this.$router.go())
          .catch(err => {
            this.errorMessage = err.response.data
          })
      }
    },
  },
  created() {
  }
}
</script>

<style>
.login-modal {
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