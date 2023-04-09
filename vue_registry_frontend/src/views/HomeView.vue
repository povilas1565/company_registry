<template>
  <div class = container>

  <input id="search" class= "form-control m-4"  v-model="searchstring" @input="this.getCompanies()" placeholder="Search Company by registration code, name or shareholder details">

    <div v-if="this.companies">
    <ul v-for="(comp,index) in this.companies" :key="index"  >
      <router-link :to="{ name: 'company', params: { reg_code: comp.reg_code }}">{{comp.reg_code}}</router-link> -- {{comp.name}}
    </ul>
  </div>
    <div v-else-if="this.companies == []">No results</div>
  <div v-else>Please enter at least 3 characters to search </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      companies : undefined,
      searchstring:"",
    }
  },
  methods: {
    getCompanies() {
      const path = 'http://localhost:5000/company/?q_home='+this.searchstring;
      if (this.searchstring.length > 2) {
      axios.get(path, {
 headers: {
   "Access-Control-Allow-Origin": 'localhost'
 }
})
        .then((res) => {
          console.log(res)
          this.companies = res.data['result']
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
      else {
        this.companies = undefined
      }

      },
},
  created() {
    this.getCompanies();
  },
};
</script>
