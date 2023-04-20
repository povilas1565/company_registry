<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid ">
		<a class="navbar-brand h3 m-3 " href="#">COMPANY REGISTRY</a>

    <ul class="navbar-nav ms-auto m-3 mb-lg-0 ">
			<li class="nav-item me-2">
            <router-link
            class="nav-link"
            id="about"
            to="/about"
            v-if="this.$route.name!='about'"
        >about</router-link>
			</li>
			<li class="nav-item">
    <router-link
            v-if="this.$route.name=='home'"
            class="btn btn-primary"
            id="create"
            to="/create"
        >Create new Company</router-link>
			</li>
    </ul>
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