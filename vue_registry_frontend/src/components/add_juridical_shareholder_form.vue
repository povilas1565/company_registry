<template>
    <div class="row m-3 justify-content-center" v-if="this.error">
    <div class="col-md-10">
      <div id="validationError" class="alert alert-warning mb-3">
        {{ this.error }}
      </div>
    </div>
  </div>
<div class="row mb-3 justify-content-center">
    <label for="regCode" class="col-md-2 form-label col-form-label">Registration Code</label>
  <div class="col-md-6">
        <div class="input-group">
    <input
        v-model="this.regCode"
        class="form-control"
        :class="{ 'mb-3' : this.id_error }"
        maxlength="7"
        id="shareholderRegCode"
        type="text"
                :disabled="this.locked"
        required
        @input="this.getCompanies()"
        placeholder="Type to search..."
    />    <span id="unlock" @click="this.unlock()" v-if="this.locked" class="input-group-text unselect-button"><BootstrapIcon
              icon="x"
            /></span> </div>
              <ul v-if="this.companies.length"
    class="w-full rounded bg-white border border-gray-300 px-4 py-2 space-y-1 absolute z-10" style="list-style-type:none;">
      <li id="autofillResult" v-for="company in this.companies" :key="company.reg_code"
      class="px-1 pt-1 pb-2 font-bold border-b border-gray-200 text-start hover-effect"
      @click="this.selectCompany(company)">
        {{company.reg_code}} - {{company.name}}</li>
    </ul>


        <strong id="lengthError" class="justify-content-start d-flex error-message" v-if="id_error">{{this.id_error}}</strong>
  </div>
</div>

<div class="row mb-3 justify-content-center">
    <label for="companyName" class="col-md-2 form-label col-form-label">Name</label>
  <div class="col-md-6">
    <input v-model="this.name"
           class="form-control"
           id="shareholderName"
           type="text"
           :disabled="this.locked"
           @input="this.validateName()"/>
  </div></div>
  <div class="row justify-content-center m-3">
    <button type="button" id="closeButton" @click="this.$emit('close')" class="btn btn-outline-secondary col-md-3 m-3">Close</button>
    <button type="button" id="addButton" @click="submit()" class="btn btn-outline-primary col-md-3 m-3">Add Shareholder</button>
  </div>
</template>

<script>
import axios from "axios";
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons';
export default {
  name: "add_juridical_shareholder_form",
    components: {BootstrapIcon},
  props: {founder: Boolean},
  emits: {
    addShareholder: null,

    close: null
  },

  data() {
    return {
      locked: false,
      companies: [],
      id_error: undefined,
      error: undefined,
      regCode: undefined,
      name: undefined,
      shareholder: {
        name: undefined,
        reg_code: undefined,
        physical_person: false,
        founder: false,
        share_amount: 0
      }
    }
  },
  watch: {
    regCode(value) {
      this.validate_reg_code(value)
    }
  },

  methods: {

    validate_reg_code(value) {
      if (value) {
        this.regCode = value.replace(/[^0-9]/gi, "");

      }
    },
    validateName() {
      this.name = this.name.replaceAll(/[^a-zA-Z öäõüÖÄÜÕ]/g, "");
      this.name = this.name.toUpperCase()
    },
    submit() {
      if (this.regCode.length != 7) {
        this.id_error = "Registration code must be exactly 7 digits long"
        return
      }
      if (this.name && this.regCode) {
        if (this.founder) {
          this.shareholder["founder"] = true
        }
        this.shareholder['reg_code'] = this.regCode;
        this.shareholder['name'] = this.name;
        this.$emit("addShareholder", this.shareholder);
        this.regCode = undefined;
        this.name = undefined;
        this.locked = false
      } else {
        this.error = "All fields must be filled"
      }
    },
    getCompanies() {
      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "http://registry-backend-alb-503252945.eu-north-1.elb.amazonaws.com"
      const path = apiurl+':5000/company/?q_shareholder=' + this.regCode;
      if (this.regCode.length > 2) {
        axios.get(path)
            .then((res) => {
              console.log(res)
              this.companies = res.data['result']
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
            });
      } else {
        this.companies = []
      }

    },
    selectCompany(company) {
      this.regCode = company["reg_code"]
      this.name = company["name"]
      this.companies = []
      this.locked = true
    },
    unlock(){
      this.regCode = undefined
      this.name = undefined
      this.locked = false
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

.hover-effect:hover {
    opacity: 0.5;
}

  li { cursor: pointer; }

  .unselect-button { cursor: pointer; }
</style>