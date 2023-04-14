<template>
  <form id ="shareholder_form">
  <div class="row m-3 justify-content-center" v-if="this.error">
    <div class="col-md-10">
      <div id="validationError" class="alert alert-warning mb-3">
        {{ this.error }}
      </div>
    </div>
  </div>
<div class="row mb-3 justify-content-center">

    <label for="idCode" class="col-md-2 form-label col-form-label">ID Code</label>
  <div class="col-md-6">
    <div class="input-group">
  <input
        v-model="this.idCode"
        class="form-control"
        :class="{ 'mb-3' : this.id_error }"
        id="idCode"
        type="text"
        maxlength="11"
        required
        @input="this.getPersons()"
    /><span class="input-group-text"><BootstrapIcon
              icon="search"
            /></span>
    </div>
    <strong id="lengthError" class="justify-content-start d-flex error-message" v-if="id_error">{{this.id_error}}</strong>
 </div>


</div>
  <div class="row mb-3 justify-content-center">
    <label for="firstName" class="col-md-2 form-label col-form-label">First Name</label>
    <div class="col-md-6">
    <input
        v-model="this.fname"
        @input="this.validateName()"
        class="form-control"
        id="firstName"
        type="text"
        :disabled="this.locked"
        required/>
  </div>
    </div>
<div class="row mb-3 justify-content-center ">
    <label for="lastName" class="col-md-2 form-label col-form-label">Last Name</label>
  <div class="col-md-6 ">
    <input
        v-model="this.lname"
        @input="this.validateName()"
        class="form-control"
        id="lastName"
        type="text"
        :disabled="this.locked"
        required/>
  </div>
</div>
    <div class="row justify-content-center m-3">
    <button type="button"
            @click="this.$emit('close')"
            class="btn btn-outline-secondary col-md-3 m-3"
            id="closeButton">Close</button>
    <button type="button"
            @click="this.submit()"
            class="btn btn-outline-primary col-md-3 m-3"
            id="addButton">Add Shareholder</button>
  </div>
    </form>
</template>

<script>

import axios from "axios";
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons';

export default {

  name: "add_physical_shareholder_form",
  components: {BootstrapIcon},
  props:{founder :Boolean},
  emits :{
          addShareholder: null,
          close : null
        },

  data() {
  return {
    results:false,
    locked:false,
    persons: [],
    id_error:undefined,
    error:undefined,
    fname:undefined,
    lname:undefined,
    idCode:"",
    shareholder : {
      name:undefined,
      reg_code:undefined,
      physical_person : true,
      founder : false,
      share_amount : 0
    }
  }
},
  watch:{
    idCode(value) {
      this.validate_reg_code(value)
    }
  },
  methods: {
    validate_reg_code(value) {
      if(value){
      this.idCode = value.replace(/[^0-9]/gi, "");
}
    },
    validateName() {
      this.fname = this.fname.replaceAll(/[^a-zA-Z ]/g, "");
      this.lname = this.lname.replaceAll(/[^a-zA-Z ]/g, "");
    },
    submit() {
      this.id_error = undefined;
      if (this.idCode.length != 11) {
        this.id_error = "ID code must be exactly 11 digits long"
        return
      } else {
        this.id_error = undefined;
      }

      if (this.fname && this.lname && this.idCode && !this.id_error) {
        if (this.founder) {
          this.shareholder["founder"] = true
        }
        this.error = undefined;
        this.shareholder['name'] = this.fname + " " + this.lname;
        this.shareholder['reg_code'] = this.idCode;
        this.$emit("addShareholder", this.shareholder);
        document.getElementById('idCode').value ="";
        document.getElementById('firstName').value ="";
        document.getElementById('lastName').value ="";
        this.fname = undefined;
        this.lname = undefined;
        this.idCode = undefined;

      } else {
        this.error = "All fields must be filled"
      }

    },


    getPersons() {
      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "http://localhost"
      const path = apiurl +':5000/person/?q=' + this.idCode;
      if (this.idCode.length > 2) {
        axios.get(path, {
          headers: {
            "Access-Control-Allow-Origin": 'localhost'
          }
        })
            .then((res) => {
              if (res.data['result'].length) {
                this.results=true
              this.persons = res.data['result']}
              else {
                this.results = false
              }
              })
            .catch((error) => {
              console.log("here")
              console.error(error);
            });
      } else {
        this.persons = []
      }},
    selectPerson(person) {
      this.idCode = person["reg_code"]
      this.fname = person["firstName"]
      this.lname = person["lastName"]
      this.persons = []
      this.results = false
    }
  }
}
</script>

<style scoped>
  .error-message{
    font-size: 10pt;
    color:red;
    text-align: left;
  }
</style>