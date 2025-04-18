<template>
      <div class="not-found">
        <h1>404 - Page Not Found</h1>
        <p>Oops! The page you are looking for does not exist.</p>
        <router-link to="/">Go to Home</router-link>
      </div>
    </template>
    
    <script lang="ts">
    export default {
      name: 'NotFound',
    };
    </script>
    
    <style scoped>
    .not-found {
      text-align: center;
      margin-top: 50px;
    }
    
    .not-found h1 {
      font-size: 2.5em;
      margin-bottom: 20px;
    }
    
    .not-found p {
      font-size: 1.2em;
    }
    
    .not-found a {
      text-decoration: none;
      color: #007bff;
      font-weight: bold;
    }
    </style>
    