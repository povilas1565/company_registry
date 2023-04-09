<template>
<nav class="navbar bg-light">
  <div class="container-fluid">
      <span class="navbar-brand h3">Company registry</span>
    <nav class="navbar-nav">
    <router-link
        v-if="this.$route.name=='home'"
        class="btn btn-primary btn-sm " id="create" to="/create">Create new Company</router-link>
 </nav>
  </div>
</nav>
  <router-view/>

</template>

<style lang="scss">

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
