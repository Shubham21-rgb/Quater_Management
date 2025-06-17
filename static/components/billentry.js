import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
    <div>
    <n></n>
    <div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/into.mp4" type="video/mp4" />
      Your browser does not support the video tag.
        </video></div>
    <div class="border rounded p-4 mb-4 bg-light shadow-sm">
    <div class="form-container mt-5">
      <h3 class="mb-4 text-center">New Bill Entry</h3>
      <form @submit.prevent="csvd">
        <div class="row mb-3">
          <div class="col-md-4">
            <label class="form-label">Staff Code:</label>
            <input v-model="formData.staff_code" type="text" class="form-control" placeholder="Enter Staff Code" required>
            <button class="btn btn-primary px-5" @click.prevent="gen">Generate+</button>
            <small class="text-muted d-block mt-2">Click to auto-fill Name and Quarter No from Staff Code</small>
          </div>
          <div class="col-md-4">
            <label class="form-label">Name: {{ genvalueret.name }}</label>
            <input v-model="formData.staff_name" type="text" class="form-control" placeholder="Enter Staff Name" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Quarter No: {{ genvalueret.quater_no }}</label>
            <input v-model="formData.quarters_number" type="text" class="form-control" placeholder="Enter the Quater No " required>
          </div>
        </div>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Licence Fee:</label>
            <input v-model="formData.licence_fee" type="number" step="0.01" class="form-control" placeholder="Enter the Lisence fee" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Meter Working Status</label>
            <select v-model="formData.meter_status" class="form-select">
              <option value="Working">Working</option>
              <option value="No Response">No Response</option>
              <option value="Lock">Lock</option>
              <option value="NA">NA</option>
            </select>
          </div>
        </div>
        <div class="border rounded p-4 mb-4 bg-light shadow-sm">
        <h6 class="text-primary mb-3">Individual Meter Information</h6>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Individual--Initial--Meter--Reading:</label>
            <input v-model="formData.initial_reading_1" type="number" step="0.01" class="form-control" placeholder="Enter Individual initial reading" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Individual--Final--Meter--Reading:</label>
            <input v-model="formData.final_reading_1" type="number" step="0.01" class="form-control" placeholder="Enter Individual Final reading" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Individual--Meter--Rent:</label>
            <input v-model="formData.meter_rent_1" type="number" step="0.01" class="form-control" placeholder="Enter Individual meter rent default set to 0.25">  
          </div>
          <div class="col-md-4">
            <label class="form-label">Individual---per--unit--charge:</label>
            <input v-model="formData.unit1" type="number" step="0.01" class="form-control" placeholder="For individual meters electric charge calculation enter per/unit charge cost " required>
          </div>
        </div>
        </div>
        <div class="border rounded p-4 mb-4 bg-info shadow-sm">
        <h6 class="text-primary mb-3">Common Meter Information</h6>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Common--Initial--Meter--Reading:</label>
            <input v-model="formData.common_initial_reading_2" type="number" step="0.01" class="form-control" placeholder="Enter Common Initial reading">
          </div>
        <div class="col-md-4">
            <label class="form-label">Common--Final--Meter--Reading:</label>
            <input v-model="formData.common_final_reading_2" type="number" step="0.01" class="form-control" placeholder="Enter Common Final reading">
          </div>
        <div class="col-md-4">
            <label class="form-label">Common--Meter--Rent:</label>
            <input v-model="formData.common_meter_rent_2" type="number" step="0.01" class="form-control" placeholder="Enter Common meter rent">
          </div>
        <div class="col-md-4">
            <label class="form-label">Common---per--unit--charge:</label>
            <input v-model="formData.unit2" type="number" step="0.01" class="form-control" placeholder="For Common meters electric charge calculation enter per/unit charge cost ">
          </div>
        </div>
        </div>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Billing Month</label>
            <div class="d-flex gap-2">
              <select class="form-select" @change="updateMonthYear" v-model="month">
                <option disabled value="">Month</option>
                <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
              </select>
              <select class="form-select" @change="updateMonthYear" v-model="year">
                <option disabled value="">Year</option>
                <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
              </select>
            </div>
            <small class="text-muted">Selected: {{ formData.join_month_year }}</small>
          </div>
        </div>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Water Charges</label>
            <input v-model="formData.water_charge" type="number" step="0.01" class="form-control" placeholder="Enter Water charges" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">COOPT-Electric-Charge</label>
            <input v-model="formData.coopt_electric_charge" type="number" step="0.01" class="form-control" placeholder="Enter COOPT-Electric charges" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">GRG-Charge</label>
            <input v-model="formData.grg_charge" type="number" step="0.01" class="form-control" placeholder="Enter GRG charges" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Other charges</label>
            <input v-model="formData.other_charges" type="number" step="0.01" class="form-control" placeholder="Enter Other charges" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Remarks</label>
            <input v-model="formData.remarks" type="text" class="form-control" placeholder="Enter Remarks" required>
          </div>
        </div>
        <br>

        <div class="text-center">
          <button class="btn btn-primary px-5">------------Save+-----------</button>
        </div>
        </form>
    </div>
  </div>
  <router-link to="/quaterbill" class="btn btn-success">Back</router-link>
    </div>
    `,
                    data: function() {
                        return {
                    transactions: [],
                        formData: {
                            staff_code:'',
                            staff_name:'',
                            quarters_number:'',
                            licence_fee:null,
                            meter_status:'',
                            initial_reading_1:null,
                            final_reading_1: null,
                            meter_rent_1:null,
                            unit1:null,
                            common_initial_reading_2:null,
                            common_final_reading_2:null,
                            common_meter_rent_2:null,
                            unit2:null,
                            join_month_year:'',
                            water_charge:null,
                            coopt_electric_charge:null,
                            grg_charge:null,
                            other_charges:null,
                            remarks:''

                    },
                    genvalueret:{
                      name:'',
                      quater_no:''
                    },
                    month: '',
                    year: '',
                    months: [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ],
                years: Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 5 + i)
                }
                    },

            mounted(){
                    
                    },
                    methods:{
                        csvd(){
                             fetch('/api/entrybillnew',{
                                method:'POST',
                                headers: {
                                    "Content-Type": "application/json",
                                    "Authentication-Token": localStorage.getItem("auth_token")
                                },
                                body:JSON.stringify(this.formData)
                            }).then(response => response.json())
    .then(data => {
        if (data.message ==='Success') {
            alert('Entry saved successfully!');
            this.$router.go(0);
            
        } 
        else {
            alert('Error: ' + data.message);  // or just 'Something went wrong!'
        }
    })
                        },
                        updateMonthYear() {
                        if (this.month && this.year) {
                            this.formData.join_month_year = `${this.month}_${this.year}`;
                            } else {
                            this.formData.join_month_year = '';
                        }
                    },
                    gen() {
  fetch('/api/genval', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Authentication-Token": localStorage.getItem("auth_token")
    },
    body: JSON.stringify(this.formData)
  })
  .then(response => response.json())
  .then(data => {
    if (Array.isArray(data) && data.length > 0) {
  let user = data[data.length - 1];

  // ✅ Overwrite formData without breaking reactivity
  Object.assign(this.formData, {
    staff_name: user.staff_name || '',
    quarters_number: user.quarters_number || '',
    licence_fee: user.licence_fee ?? null,
    initial_reading_1: user.initial_reading_1 ?? null,
    final_reading_1: user.final_reading_1 ?? null,
    meter_rent_1: user.meter_rent_1 ?? null,
    meter_status: user.meter_status || '',
    common_initial_reading_2: user.common_initial_reading_2 ?? null,
    common_final_reading_2: user.common_final_reading_2 ?? null,
    water_charge: user.water_charge ?? null,
    coopt_electric_charge: user.coopt_electric_charge ?? null,
    grg_charge: user.grg_charge ?? null,
    other_charges: user.other_charges ?? null,
    remarks: user.remarks || '',
    common_meter_rent_2: user.common_meter_rent_2 ?? null
  });

  alert('Auto details loaded successfully!');
}else {
      // Reset form and allow manual entry
      this.genvalueret = {};
    this.formData.staff_name = '';
    this.formData.quarters_number = '';
    this.formData.licence_fee = null;
    this.formData.initial_reading_1 = null;
    this.formData.final_reading_1 =null ;
      this.formData.meter_rent_1 =null ;
      this.formData.meter_status = '';
      this.formData.common_initial_reading_2 =null ;
      this.formData.common_final_reading_2 = null;
      this.formData.water_charge =null ;
      this.formData.coopt_electric_charge =null ;
      this.formData.grg_charge =null ;
      this.formData.other_charges =null ;
      this.formData.remarks ='' ;
      this.formData.common_meter_rent_2 = null;
      alert('No record found. Please fill in details manually.');
    }
  })
  .catch(error => {
    console.error("Error fetching genval:", error);
    alert('An error occurred. Try again.');
  });
}
                    }
                }