<template>
  <nav class="flex flex-col xs:items-center xs:justify-between px-6 py-2 shadow-lg xs:flex-row fixed transition text-gray-400 w-full z-50" :class="{ 'isTop': (scrollTop > 50), 'isNotTop': (scrollTop > 50) }">
      <!-- brand logo -->
      <div class="flex items-center ml-3 xs:ml-0 mb-3 xs:mb-0 mt-1 xs:mt-0">
        <div class="text-3xl font-bold">
          <router-link :to="{ name: 'Home' }">MOOOVIE</router-link>
        </div>
      </div>

      <!-- menu icons -->
      <div v-if="(width > 500 || scrollTop < 50)" class="w-full pb-2 xs:flex xs:items-center xs:justify-end xs:pb-0">
        <!-- serach bar -->
        <search-bar></search-bar>
        
        <div class="flex flex-col px-2 xs:flex-row">
          <div v-if="isLoggedIn">
            <button @click="onLogout" class="py-2 px-2 rounded">Logout</button>
            <router-link :to="{ name: 'MyProfile'}" class="py-2 px-2 rounded">MyProfile</router-link>
          </div>
          <div v-else>
            <button @click="toggleLoginModal" class="py-2 px-2 rounded">Login</button>
            <button @click="toggleSignupModal" class="py-2 px-2 rounded">Signup</button>
          </div>
        </div>
      </div>
  </nav>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
import { mapState, mapActions } from 'vuex'

export default {
  components: { SearchBar },
  name: 'Navbar',
  data: function () {
    return {
      scrollTop: 0,
      width: 0
    }
  },
  methods: {
    ...mapActions(['init', 'onLogout']),
    handleScroll() {
      this.scrollTop = document.documentElement.scrollTop
    },
    handleResize() {
        this.width = window.innerWidth;
    },
    toggleLoginModal() {
      const loginModal = document.querySelector(".login-modal");
      loginModal.classList.toggle("hidden");
    },
    toggleSignupModal() {
      const signupModal = document.querySelector(".signup-modal");
      signupModal.classList.toggle("hidden");
    },
  },
  computed: {
    ...mapState(['isLoggedIn']),
  },
  created() {
    this.init()
    window.addEventListener('resize', this.handleResize);
    window.addEventListener('scroll', this.handleScroll);
  },
  unmounted() {
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('resize', this.handleResize);
  },
}
</script>

<style>
.isTop {
  background-color: transparent;
}

.isNotTop {
  background-color: white;
}
</style>  