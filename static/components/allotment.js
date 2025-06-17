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
      <h3 class="mb-4 text-center">New Quater Allotment</h3>
      <form @submit.prevent="csvd">
        <div class="row mb-3">
          <div class="col-md-4">
            <label class="form-label">Name:</label>
            <input v-model="formData.name" type="text" class="form-control" placeholder="Enter Name" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Designation:</label>
            <input v-model="formData.Designation" type="text" class="form-control" placeholder="Enter Designation" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Type_of_Quater:</label>
            <input v-model="formData.Type_of_Quater" type="text" class="form-control" placeholder="Enter the Quater No " required>
          </div>
        </div>
        <div class="row mb-3">
        <div class="col-md-4">
            <label class="form-label">Area</label>
            <input v-model="formData.Area" type="number" step="0.01" class="form-control" placeholder="Enter Area" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Date_of_allotment</label>
            <input v-model="formData.Date_of_allotment" type="date" class="form-control" placeholder="Enter Date_of_allotment" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Year_of_construction</label>
            <input v-model="formData.Year_of_construction" type="text" class="form-control" placeholder="Year_of_construction" required>
          </div>
        </div>
        <br>

        <div class="text-center">
          <button class="btn btn-primary px-5">------------Save+-----------</button>
        </div>
        </form>
    </div>
  </div>
  <router-link to="/admin" class="btn btn-success">Back</router-link>
    </div>
    `,
                    data: function() {
                        return {
                    transactions: [],
                        formData: {
                            name:'',
                            Type_of_Quater:'',
                            Designation:'',
                            Area:'',
                            Date_of_allotment:'',
                            Year_of_construction:''

                    }
                }
                    },

            mounted(){
                    
                    },
                    methods:{
                        csvd(){
                             fetch('/api/newallotment',{
                                method:'POST',
                                headers: {
                                    "Content-Type": "application/json",
                                    "Authentication-Token": localStorage.getItem("auth_token")
                                },
                                body:JSON.stringify(this.formData)
                            }).then(response => response.json())
    .then(data => {
            alert('Entry saved successfully!');
            this.$router.push('/admin');
            
        
    })
                        }
                    }
                }