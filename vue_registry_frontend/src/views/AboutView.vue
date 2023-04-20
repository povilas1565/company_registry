<template>
  <h2 class="text-start m-4">Rules for creating companies:</h2>

  <p class="text-start m-4">
    Companies must have total share capital at least 2500EUR. <br>
    Company name must be between 3 and 100 characters long and can contain only letters.<br>
    Registration date can't be in the future. <br>
    Company must have at least one shareholder.<br>
    Registration code must be 7 digits long and contain only numbers.<br>
    Physical shareholders must have 11 digit id code and first name and last name.<br>
    Juridical shareholders must have 7 digit registration code and name.<br>
    All shareholders must be unique.
  </p>

  <h2 class="text-start m-4">How-to:</h2>
  <p class="text-start m-4">
    The application is initialized with 3 companies:</p>
  <li class="text-start ms-4">0000000 - NULL AS</li>
    <li class="text-start ms-4">1234567 - TEST AS</li>
  <li class="text-start ms-4">7654321 - TEST OÜ</li>
  <p class="text-start m-4">
    Search companies on the main page by company name, registration code or shareholder name/code.<br>
 When adding a shareholder, autocomplete offers choices from the database upon entering reg/id code:<br>  </p>
    <li class="text-start ms-4">Physical Shareholder -  queries all physical shareholders for all companies</li>
    <li class="text-start ms-4">Juridical Shareholder - queries all created companies</li>
    <p class="text-start m-4">
    Selecting an option causes the info to be autofilled and the fields become locked for further editing. <br>
      To unlock the fields - click on the button next to the reg/id code field. <br>
      To add a brand new shareholder, just ignore the dropdown and enter the info.<br>
      After a company is created, it's possible to change shareholders by clicking on the edit button.

    </p>


<button @click="$router.back()" class="btn btn-secondary m-4 d-flex btn-sm">Back</button>
</template>

<script>

export default {
  name: 'AboutView',
}
</script>
