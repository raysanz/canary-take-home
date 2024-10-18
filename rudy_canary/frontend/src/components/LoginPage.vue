<!-- Login.vue -->
<template>
  <div>
    <button @click="loginWithGoogle">Login with Google</button>
    <p v-if="loggedIn">Welcome, {{ user.name }}!</p>

    <div v-if="repos">
      <h3>Your GitHub Repositories:</h3>
      <ul>
        <li v-for="repo in repos" :key="repo.id">{{ repo.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: null,
      loggedIn: false,
    };
  },
  mounted() {
    const queryParams = new URLSearchParams(window.location.search);
    const code = queryParams.get('code');

    if (code) {
      this.exchangeCodeForToken(code);
    }
  },
  methods: {
    loginWithGoogle() {
      const googleOAuthURL = 'https://accounts.google.com/o/oauth2/auth';
      const clientId = '592389886839-13s600e9duul3rc5pvq6oalpi33aeuf4.apps.googleusercontent.com';  // hard coding wip env
      const redirectUri = 'http://localhost:8000/github/callback/';  
      const scope = 'profile email';
      const responseType = 'code';
      
      // Redirect the user to Google's OAuth page
      const url = `${googleOAuthURL}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&response_type=${responseType}`;
      window.location.href = url;
    },
    async exchangeCodeForToken(code) {
   try {
     const response = await axios.post('http://localhost:8000/api/auth/social/google/', {
       code: code,
       redirect_uri: 'http://localhost:8000/github/repos',
     });

     // On success, store user data and mark as logged in
     this.user = response.data.user;
     this.loggedIn = true;
     
     // Fetch GitHub repos after login
     this.fetchRepos();
   } catch (error) {
     console.error('OAuth login failed', error);
   }
},
    async fetchRepos() {
      try {
        const response = await axios.get('http://localhost:8000/github/repos');
        this.repos = response.data;
      } catch (error) {
        console.error('Failed to fetch GitHub repos', error);
      }
    }
  }
}
</script>
