<template>
  <div class = container>
    <input id="search"
           class= "form-control m-4"
           v-model="searchstring"
           @input="this.getCompanies()"
           placeholder="Search Company by registration code, name or shareholder details">

    <div v-if="this.companies === 'Not found'">No results</div>
    <div v-else-if="this.companies">
      <ul v-for="(comp,index) in this.companies" :key="index">
        <router-link :to="{ name: 'company', params: { reg_code: comp.reg_code }}">{{comp.reg_code}}</router-link> -- {{comp.name}}
      </ul>
    </div>
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
      // fetches companies from API based on input string
      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "http://registry-backend-alb-503252945.eu-north-1.elb.amazonaws.com"
      const path = apiurl + ':5000/company/?q_home='+this.searchstring;
      if (this.searchstring.length > 2) {
      axios.get(path)
        .then((res) => {
          if (res.data['result'].length) {
            this.companies = res.data['result']
            }
          else {
            this.companies = 'Not found'
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error.response.data);
        });
    }
      else {
        this.companies = undefined
      }
    },
  },
};
</script>
