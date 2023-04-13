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
        required
        @input="this.getCompanies()"
    />    <span class="input-group-text"><BootstrapIcon
              icon="search"
            /></span>
        </div>

        <strong id="lengthError" class="justify-content-start d-flex error-message" v-if="id_error">{{this.id_error}}</strong>
  </div></div>


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

        if (!value.length) {
          this.id_error = undefined;
        } else if (value.length != 7) {
          this.id_error = "Registration code must be exactly 7 digits long"
        } else {
          this.id_error = undefined;
        }
      }
    },
    validateName() {
      this.name = this.name.replaceAll(/[^a-zA-Z ]/g, "");
    },
    submit() {
      if (this.name && this.regCode && !this.id_error) {
        if (this.founder) {
          this.shareholder["founder"] = true
        }
        this.shareholder['reg_code'] = this.regCode;
        this.shareholder['name'] = this.name;
        this.$emit("addShareholder", this.shareholder);
        this.regCode = undefined;
        this.name = undefined;
      } else {
        this.error = "All fields must be filled"
      }
    },
    getCompanies() {
      const apiurl = process.env.NODE_ENV === "test" ? "http://registryapi" : "http://ec2co-ecsel-1gcsef12y4ymn-605589819.eu-north-1.elb.amazonaws.com"
      const path = apiurl+':5000/company/?q_shareholder=' + this.regCode;
      if (this.regCode.length > 2) {
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
      } else {
        this.companies = []
      }

    },
    selectComp(company) {
      this.regCode = company["reg_code"]
      this.name = company["name"]
      this.companies = []
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
</style>