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

  <div id="successMessage"
  class="alert alert-success mt-1 mb-3 alert-dismissible fade show"
  v-else-if="this.success">
      Successfully updated
      <button
      ype="button"
      class="btn-close"
      data-bs-dismiss="alert"
      aria-label="Close">
      </button>
  </div>

<div class="container">
    <div class="row row-cols-lg-auto justify-content-start mt-5 p-3 border rounded border-info">
      <div class="col-md-12">
        <h1 id="companyHeader">{{this.company['reg_code'] + ' - ' + this.company['name'].toUpperCase()}}<sup></sup> </h1>
        <div class="row justify-content-start">
<span class="text-start">First registered: {{this.company['reg_date']}}</span>

      </div>
        <div class="row justify-content-start">
<span class="text-start">Total Share Amount: {{this.totalShareCapital}}</span>

      </div>
      </div>



    </div>


      <div class="row mt-4 row-cols-md justify-content-start">
        <div class="col-md-6 justify-content-start">
        <u><h3>Shareholders:</h3></u>
          <button
              v-if="!this.show_form"
              type="button"
              class="btn btn-outline-primary btn-sm"
              @click="this.show_form = !this.show_form"
              id="showFormButton"
          :hidden="!this.edit">Add
          </button>
          </div>
        <div class="col-md-6 justify-content-end d-flex">
        <button
              type="button"
              class="btn text-primary "
              @click="this.edit = !this.edit"
              id="editButton"
    ><BootstrapIcon
              icon="pencil-square"
            /><u> edit</u></button>
        </div>
        </div>

      <div v-if="this.company['shareholders'].length" >
      <table  id="shareholdersTable" class="table table-borderless">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Share Capital</th>
            <th>Founder</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(shareholder,index) in this.company['shareholders']" :key="index" :row-index="index">
            <td>
            <input v-model="shareholder['reg_code']"
                     type="text"
                     class="form-control form-control-sm border-0 bg-white text-center"
                     id="code"

              disabled/>

</td>
            <td>

              <input v-model="shareholder['name']"
                     type="text"
                     class="form-control form-control-sm border-0 bg-white text-center"
                     id="name"

              disabled/>


         </td>
            <td>


                <input v-model="shareholder['share_amount']"
                     type="number"
                     class="form-control form-control-sm  bg-white text-center"
                       :class="{'border-0':!this.edit}"
                     id="capital"
                      @input="this.calculateShareCapital()"
              :disabled="!this.edit"/>


            </td>
            <td>

              <input v-model="shareholder['founder']"
                     type="text"
                     class="form-control form-control-sm border-0 bg-white text-center"
                     id="founder"

              disabled/>


         </td>
            <td>
              <div v-if="this.edit" class="btn btn-danger btn-sm" @click="this.removeShareholder(index)"><BootstrapIcon
              icon="x-square-fill"
            flip-v /></div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="mt-5 col-md-12 shareholder-form" v-if="this.show_form">
        <div class = "row justify-content-center m-3">
         <div class="form-check col-md-3 m-3">
          <input checked @change="this.physical = true" name="shareholderType" type="radio" id="showPhysicalShareholderForm" class="form-check-input">
          <label for="showPhysicalShareholderForm" class="form-check-label">Physical Shareholder</label>
        </div>
        <div class="form-check col-md-3 m-3">
          <input @change="this.physical=false" name="shareholderType" type="radio" class="form-check-input" id="showJuridicalShareholderForm">
          <label class="form-check-label" for="showJuridicalShareholderForm">Juridical Shareholder</label>
      </div>
          </div>

        <Add_physical_shareholder_form

            v-if="this.physical"
            @add-shareholder="addShareholder"
            @close="this.show_form=false"/>
        <Add_juridical_shareholder_form

            v-else
            @add-shareholder="addShareholder"
            @close="this.show_form=false"/>
      </div>
<div class="row justify-content-center m-3"
           v-if="!this.show_form">
    <button type="button" class="btn btn-secondary btn-block col-md-3 m-3" @click="this.$router.push({ path: '/'})">Back</button>
<button type="button"
            class="btn btn-primary btn-block col-md-3 m-3"
            @click="updateCompany()"
            id="updateButton">Update</button>
</div>
</template>

<script>
import axios from 'axios';
import BootstrapIcon from "@dvuckovic/vue3-bootstrap-icons";
import Add_physical_shareholder_form from "@/components/add_physical_shareholder_form.vue";
import Add_juridical_shareholder_form from "@/components/add_juridical_shareholder_form.vue";
export default {
  name: 'CompanyView',
    components: {BootstrapIcon,Add_juridical_shareholder_form,Add_physical_shareholder_form},
  data() {
    return {
      success:undefined,
      physical:true,
      show_form:false,
      error:undefined,
      company:undefined,
      edit:false,
      totalShareCapital:0
    }
  },
  methods: {
    getCompany() {
      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "http://localhost"
      const path = apiurl + ':5000/company/' + this.$route.params.reg_code;
      axios.get(path)
        .then((res) => {
            this.company = res.data


        })
        .catch((error) => {
          // eslint-disable-next-line
          this.error =error.response.data["Error"]
        })
    },updateCompany() {
      this.error = undefined;
      var reg_codes = []
      for (let i = 0; i < this.company['shareholders'].length; i++) {
        if(reg_codes.includes(this.company['shareholders'][i]["reg_code"]))
        {
          this.error = "Each shareholder must have unique code"
          return
        }
        else if (!this.company['shareholders'][i]["share_amount"]){
        this.error = "All shareholders must have share capital"
          return
        }
        reg_codes.push(this.company['shareholders'][i]["reg_code"])
      }
      if (this.totalShareCapital <2500) {
          this.error = "Total share capital must be at least 2500EUR."
          return
      }

      const apiurl = window.location.host == "registryfrontend"  ? "http://registryapi" : "http://localhost"
      const path = apiurl + ':5000/company/'+this.company["reg_code"];
      axios.put(path, this.company)
          .then((res) => {
            if (res.status == 201) {
              this.success=true
              this.edit=false


            }})
          .catch((error) => {
            // eslint-disable-next-line
            if (error.response.status == 400) {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);

            this.error = error.response.data["Error"]
              }
          });
    },
    calculateShareCapital() {
      this.totalShareCapital = 0
      this.company['shareholders'].forEach(sh => {
        this.totalShareCapital += sh['share_amount']
      })
},    removeShareholder(index) {
      this.company['shareholders'].splice(index, 1)
    },
        addShareholder(shareholder) {
      this.company['shareholders'].push(JSON.parse(JSON.stringify(shareholder)))
    },
  },
created() {
    this.getCompany();
},
  mounted(){
    this.calculateShareCapital()
  }
};
</script>
<style>

</style>
