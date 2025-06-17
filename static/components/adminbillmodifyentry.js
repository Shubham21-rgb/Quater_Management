export default{
    template:`
    <div class="container mt-5">
        <h1 align="center">Service Update</h1>
        <div class="d-flex justify-content-center align-items-center vh-80">
            <div class="alert alert-primary" role="alert" style="width: 800px; height: 1500px; padding: 20px; font-size: 18px;">
            <h2>Admin Management Area</h2>
            <p>General Information : Do Not need to fill all the area where update is required do that only</p>
            <p>So please Fill it carefully</p>
            <br><br>
                <p>Update bill Details------------->>  id-{{id}}</p>
                <h4>Update Entry Details</h4>
                <p>SL.No:{{id}}</p>
                <p>Name:{{staff_name1}}</p>
                <p>Staff Code:{{staff_code1}}</p>
                <p>Quater-No:{{quarters_number1}}</p>
                <p>Month:{{Month1}}</p>
                <p>Meter Status:{{meter_status1}}</p>
                <p>Net-Amount:{{net_amount1}}</p>
                <p>Remarks:{{remarks1}}</p>


                <div class="mb-3">
                    <label for="type" class="form-label">Name</label>
                    <input type="text" class="form-control" id="amount" v-model="date.staff_name">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Staff-Code</label>
                    <input type="text" class="form-control" id="amount" v-model="date.staff_code">
                </div>
                <div class="mb-3">
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
            <small class="text-muted">Selected: {{ date.Month }}</small>
          </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Quater_Type</label>
                    <input type="text" class="form-control" id="amount" v-model="date.quarters_number">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Meter-status</label>
                    <input type="text" class="form-control" id="amount" v-model="date.meter_status">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Remarks</label>
                    <input type="text" class="form-control" id="amount" v-model="date.remarks">
                </div>
                <button class="btn btn-success" @click="save">Save+</button>
                <router-link to="/quaterbill" class="btn btn-warning">Back</router-link>
            </div>
        </div>
    </div>
        `,
                data:function(){  
                    return{
                        id:null,
                        staff_name1:null,
                        staff_code1:null,
                        quarters_number1:null,
                        Month1:null,
                        meter_status1:null,
                        remarks1:null,
                        net_amount1:null,


                        date: {
                            staff_name:'',
                            staff_code:'',
                            Month:'',
                            quarters_number:'',
                            meter_status:'',
                            remarks:''
                        },month: '',
                    year: '',
                    months: [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ],
                years: Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - 5 + i)
                    }
                },
                mounted(){
                    this.cr()
                },
                methods:{
                    cr(){
                        this.id = this.$route.params.id,
                        this.staff_name1=this.$route.params.staff_name,
                        this.staff_code1=this.$route.params.staff_code,
                        this.quarters_number1=this.$route.params.quarters_number,
                        this.Month1=this.$route.params.Month,
                        this.meter_status1=this.$route.params.meter_status,
                        this.remarks1=this.$route.params.remarks,
                        this.net_amount1=this.$route.params.net_amount
                      
                    },

                    save(){
                        fetch(`/api/update_bill/${this.$route.params.id}`,{
                            method:'PUT',
                            headers: {
                                "Content-Type":'application/json',
                                "Authentication-Token":localStorage.getItem("auth_token")
                            },
                            body:JSON.stringify(this.date)
                    }).then(response => response.json())
                    .then(data =>{
                        console.log(data);
                        alert("Succesfully updated");
                        this.$router.push('/adminbillmod');

                    }
                    )},
                    updateMonthYear() {
                        if (this.month && this.year) {
                            this.date.Month = `${this.month}_${this.year}`;
                            } else {
                            this.date.Month = '';
                        }
                    }
                    }
                }