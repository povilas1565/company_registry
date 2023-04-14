<template>
  <div class="alert alert-warning mt-1 mb-3 alert-dismissible fade show"
  v-if="this.error">
    <div id="errorMessage">
      {{ this.error }}</div>
      <button
      type="button"
      class="btn-close"
      data-bs-dismiss="alert"
      aria-label="Close">
      </button>
  </div>



    <div class="row justify-content-center">
      <div class="col-md-12">
        <form  class="row row-cols-lg-auto g-3 align-items-center justify-content-center mt-3">
          <div class="col-md-6">
            <div class="form-floating mb-3">
              <input
                  v-model="new_comp['name']"
                  maxlength="100" minlength="3"
                  class="form-control form-control-sm"
                  id="companyName"
                  @input="this.validateName()"
                  placeholder="Company Name"
              />
              <label for="companyName">Company Name</label>
          </div>
          </div>
          <div class="col-md-6">
            <div class="form-floating mb-3">
              <input v-model="this.regCode"
                     maxlength="7"
                     type="text"
                     class="form-control form-control-sm"
                     id="regCode"
                     placeholder="Registration Code"
              />
              <label for="regCode">Registration Code</label>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-floating mb-3">
              <input v-model="new_comp['reg_date']"
                     type="date"
                     class="form-control form-control-sm"
                     id="regDate"
                     />
              <label for="regDate">Registration date</label>
            </div>
</div>
          <div class="col-md-6">
            <div class="form-floating mb-3">
              <input v-model="this.totalShareCapital"
                     type="number"
                     class="form-control form-control-sm"
                     id="totalCapital"
                     disabled
                      :class="{'is-invalid' : this.totalShareCapital<2500}"/>
              <label for="totalCapital">Total Share Capital</label>
            </div>
          </div>

      </form>
        <hr>
        <div class="row row-cols-lg-auto g-3 align-items-start justify-content-start mt-3">
        <h3>Shareholders:</h3>
          <button
              v-if="!this.show_form"
              type="button"
              class="btn btn-outline-primary btn-sm"
              @click="this.show_form = !this.show_form"
              id="showFormButton">Add</button>
        </div>

      <div v-if="this.shareholders.length" >
      <table  class="table table-borderless">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Share Capital</th>
            <th></th>
          </tr>
        </thead>
        <tbody >
          <tr v-for="(shareholder,index) in this.shareholders" :key="index" :row-index="index">
            <td>
            <input v-model="shareholder['reg_code']"
                     type="text"
                     class="form-control form-control-sm"
                     id="code"
              disabled/>

</td>
            <td>

              <input v-model="shareholder['name']"
                     type="text"
                     class="form-control form-control-sm"
                     id="name"
              disabled/>


         </td>
            <td>
              <div class="input-group input-group-sm">
                <span class="input-group-text">€</span>

              <input v-model="shareholder['share_amount']"
                     type="number"
                     class="form-control form-control-sm"
                     id="capital"
                      @input="this.calculateShareCapital()"/>
                <span class="input-group-text">.00</span>

                </div>
            </td>

            <td>
              <div class="btn btn-danger btn-sm" @click="this.removeShareholder(index)"><BootstrapIcon
              icon="x-square-fill"
            flip-v /></div>
            </td>



        </tr>
        </tbody>
        </table>
        </div>
        <div v-else
        class="m-5">
          <h5>Add shareholders to continue</h5>
        </div>



      <div class="mt-5 col-md-12 shareholder-form" v-if="this.show_form">
        <div class = "row justify-content-center m-3">
         <div class="form-check col-md-3 m-3">
          <input checked @change="this.physical = true" name="shareholderType" type="radio" id="showPhysicalShareholderForm" class="form-check-input">
          <label for="showPhysicalShareholderForm" class="form-check-label">Physical Shareholder</label>
        </div>
        <div class="form-check col-md-3 m-3">
          <input @change="this.physical = false" name="shareholderType" type="radio" class="form-check-input" id="showJuridicalShareholderForm">
          <label class="form-check-label" for="showJuridicalShareholderForm">Juridical Shareholder</label>
      </div>
          </div>

        <Add_physical_shareholder_form
            founder
            v-if="this.physical"
            @add-shareholder="addShareholder"
            @close="this.show_form=false"/>
        <Add_juridical_shareholder_form
            founder
            v-else
            @add-shareholder="addShareholder"
            @close="this.show_form=false"/>
      </div>
      </div>
      </div>
           <div class="row justify-content-center m-3"
           v-if="!this.show_form">
    <button type="button" class="btn btn-secondary btn-block col-md-3 m-3" @click="this.$router.push({ path: '/'})">Back</button>
    <button type="button"
            class="btn btn-primary btn-block col-md-3 m-3"
            @click="postCompany()"
            id="createButton">Create company</button>
    </div>



</template>

<script>
import axios from 'axios';
import Add_physical_shareholder_form from "@/components/add_physical_shareholder_form.vue";
import Add_juridical_shareholder_form from "@/components/add_juridical_shareholder_form.vue";
import router from "@/router";
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons';
// eslint-disable-next-line no-unused-vars
import isLetter from "@/helpers/isLetter";

export default {
  name: 'CreateView',
  components: {Add_physical_shareholder_form,Add_juridical_shareholder_form,BootstrapIcon},

  data() {
    return {
      totalShareCapital:0,
      regCode:undefined,
      new_comp:{
        name:undefined,
        reg_code:undefined,
        reg_date:undefined,
        shareholders:[]
      },
      shareholders:[],
      error:undefined,
      created_company:undefined,
      physical:true,
      show_form:false
    }
  },
      watch:{
    regCode(value) {
      console.log(value)
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
    postCompany() {
      this.new_comp["reg_code"] = this.regCode
      this.error = undefined;
      var reg_codes = []
      for (let i = 0; i < this.shareholders.length; i++) {
        if(reg_codes.includes(this.shareholders[i]["reg_code"]))
        {
          this.error = "Each shareholder must have unique code"
          return
        }
        else if (!this.shareholders[i]["share_amount"]){
        this.error = "All shareholders must have share capital"
          return
        }
        reg_codes.push(this.shareholders[i]["reg_code"])
      }
      if (this.totalShareCapital <2500) {
          this.error = "Total share capital must be at least 2500EUR."
          return
      }
      if (!this.new_comp['reg_code'] || !this.new_comp['reg_date'] || !this.new_comp['name']) {
          this.error = "All fields must be filled"
          return
      }

      this.new_comp["shareholders"] = this.shareholders
      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "htttp://" + window.location.host
      const path = apiurl + ':5000/company/';
      axios.post(path, this.new_comp)
          .then((res) => {
            if (res.status == 201) {
              router.push({name: 'company', params: {reg_code: this.new_comp['reg_code']}})
            }})
          .catch((error) => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
            if (error.response.status == 400) {


            this.error = error.response.data["Error"]
              }
          });
    },
    addShareholder(shareholder) {
      this.shareholders.push(JSON.parse(JSON.stringify(shareholder)))
    },
    removeShareholder(index) {
      this.shareholders.splice(index, 1)
    },
    validateName() {
      this.new_comp['name'] = this.new_comp['name'].replaceAll(/[^a-zA-Z ]/g, "");

      this.new_comp['name'] = this.new_comp['name'].toUpperCase()
    },
    calculateShareCapital() {
      this.totalShareCapital = 0
      this.shareholders.forEach(sh => {
        this.totalShareCapital += sh['share_amount']
      })
    },
  },

computed:{

},
  mounted(){
    var today = new Date().toISOString().split("T")[0];
    this.new_comp["reg_date"] = today
    document.getElementById('regDate').setAttribute("max", today)

  }
};
</script>
<style>
.shareholder-form {


  border: 1px solid black;
}

</style>