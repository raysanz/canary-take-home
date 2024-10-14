<template>
  <div>
    <button @click="loginWithGoogle">Log-in with Google</button>
    <button v-if="githubLinked" @click="linkGitHub">Link GitHub Account</button>
    <div v-if="repos.length > 0">
      <ul>
        <li v-for="repo in repos" :key="repo.id">{{ repo.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useGoogleOauth } from 'vue3-google-oauth2'

export default {
  name: 'LoginPage',
  data() {
    return {
      githubLinked: true,
      repos: []
    }
  },
  methods: {
  setup() {
    const { login } = useGoogleOauth({
      clientId: '592389886839-13s600e9duul3rc5pvq6oalpi33aeuf4.apps.googleusercontent.com',
    });

    const loginWithGoogle = () => {
      // eslint-disable-next-line
      login().then(googleUser => {
        console.log('Logged in with Google:', googleUser);
      }).catch(error => {
        console.error('Google login error:', error);
      });
    };

    return { loginWithGoogle };
  },
    linkGitHub() {
      window.location.href = 'https://github.com/login/oauth/authorize?client_id=Ov23liu3cPIqQFF4pCRd'
    },
    fetchRepos() {
      axios.get('/api/repositories/')
        .then(response => {
          this.repos = response.data
        })
    }
  }
}
</script>
