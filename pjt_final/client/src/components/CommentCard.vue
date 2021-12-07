<template>
  <div>
    <div class="flex-col bg-white border rounded-lg px-4 py-2 sm:px-6 sm:py-4 leading-relaxed">
      <strong>{{ comment.user.username }}</strong> <span class="text-xs text-gray-400">{{ parse(comment.created_at) }}</span>
      <div class="flex justify-between">
        <p class="text-sm">
            {{ comment.content }}
        </p>
        <div v-if="userInfo && ( comment.user === userInfo.user_data.id || comment.user.id === userInfo.user_data.id )" class="flex items-center">
          <div class="text-sm text-gray-500 font-semibold">
            <button @click="deleteComment(comment)">
              댓글삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'CommentCard',
  props: {
    comment: Object,
  },
  computed: {
    ...mapState(['userInfo'])
  },
  methods: {
    setToken() {
      const token = localStorage.getItem('token')
      return {
        Authorization: `Token ${token}`
      }
    },
    parse(time){
      const date = time.slice(0, 10)
      const hour = String((parseInt(time.slice(11,13))+9)%24)+":"
      const minute = time.slice(14,19)
      return date + ' ' + hour + minute
    },
    deleteComment(comment) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/reviews/${comment.review}/comments/${comment.id}/`,
        headers: this.setToken()
      })
      .then(() => {
        this.$emit('comment-deleted')
      })
      .catch(err => console.error(err))
    },
  }
}
</script>

<style>

</style>