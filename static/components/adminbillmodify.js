import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
   <div>
    <n></n>
    <div class="row border login-box">
    <div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/into.mp4" type="video/mp4" />
      Your browser does not support the video tag.
        </video></div>
                <div class="col-12 border" style="height: 750px; overflow-y: scroll">
                    <h2>Search Area</h2>
                            <div class="d-flex align-items-center gap-3 my-3">
                                <i class="bi bi-search"></i><input v-model="transData.search1" type="text" class="form-control" placeholder="......................Search....................">
                                <div class="d-flex align-items-center">
                                    <label for="source" class="form-label"> Filter-By</label>
                                    <select class="form-select" aria-label="Default select example" v-model="transData.filter1">
                                        <option selected>Open this select menu</option>
                                        <option value="staff_code">Staff-ID</option>
                                        <option value="staff_name">Name</option>
                                        <option value="quarters_number">Quarter-No</option>
                                        <option value="Month">Month</option>
                                    </select>
                                </div>
                        </div>
                         <div class="d-flex align-items-center gap-3 my-3">
                                <i class="bi bi-search"></i><input v-model="transData.search2" type="text" class="form-control" placeholder="......................Search....................">
                                <div class="d-flex align-items-center">
                                    <label for="source" class="form-label"> Filter-By</label>
                                    <select class="form-select" aria-label="Default select example" v-model="transData.filter2">
                                        <option selected>Open this select menu</option>
                                        <option value="staff_code">Staff-ID</option>
                                        <option value="staff_name">Name</option>
                                        <option value="quarters_number">Quarter-No</option>
                                        <option value="Month">Month</option>
                                    </select>
                                </div>
                        </div>

                        <button @click="handleSearch" class="btn btn-warning">
                            <i class="bi bi-search">Search</i>
                        </button>

                        <div v-for="t in transactions" class="card mt-2" style="width:4000px">
                            <table class="table table-bordered table-striped align-middle">
                                <thead class="table table-success table-striped">
                                    <tr>
                                    <th scope="col">Sl_no</th>
                                    <th scope="col">Actions</th>
                                    <th scope="col">staff_code</th>
                                    <th scope="col">staff_name</th>
                                    <th scope="col">quarters_number</th>
                                    <th scope="col">licence_fee</th>
                                    <th scope="col">Month</th>
                                    <th scope="col">meter_status</th>
                                    <th scope="col">initial_reading_1</th>
                                    <th scope="col">final_reading_1</th>
                                    <th scope="col">difference_reading_1</th>
                                    <th scope="col">meter_rent_1</th>
                                    <th scope="col">electric_charge</th>
                                    <th scope="col">common_initial_reading_2</th>
                                    <th scope="col">common_final_reading_2</th>
                                    <th scope="col">difference_reading_2</th>
                                    <th scope="col">common_meter_rent_2</th>
                                    <th scope="col">common_electric_charge</th>
                                    <th scope="col">total_electricity_charges</th>
                                    <th scope="col">water_charge</th>
                                    <th scope="col">coopt_electric_charge</th>
                                    <th scope="col">grg_charge</th>
                                    <th scope="col">other_charges</th>
                                    <th scope="col"class="table-active">net_amount</th>
                                    <th scope="col">remarks</th>
                                    </tr>
                                </thead>
                                <tbody>  
                                    <td>{{t.Sl_no}}</td>
                                    <td><router-link :to="{name:'adminserv2',params:{id: t.Sl_no,staff_name:t.staff_name,staff_code:t.staff_code,quarters_number:t.quarters_number,Month:t.Month,meter_status:t.meter_status,remarks:t.remarks,net_amount:t.net_amount}}" class="btn btn-warning">Update</router-link>
                                    <router-link :to="{name:'deletebill',params:{id: t.Sl_no,staff_name:t.staff_name,staff_code:t.staff_code}}" class="btn btn-danger">Delete</router-link></td>
                                    <td>{{t.staff_code}}</td>
                                    <td>{{t.staff_name}}</td>
                                    <td>{{t.quarters_number}}</td>
                                    <td>{{t.licence_fee}}</td>
                                    <td>{{t.Month}}</td>
                                    <td>{{t.meter_status}}</td>
                                    <td>{{t.initial_reading_1}}</td>
                                    <td>{{t.final_reading_1}}</td>
                                    <td>{{t.difference_reading_1}}</td>
                                    <td>{{t.meter_rent_1}}</td>
                                    <td>{{t.electric_charge}}</td>
                                    <td>{{t.common_initial_reading_2}}</td>
                                    <td>{{t.common_final_reading_2}}</td>
                                    <td>{{t.difference_reading_2}}</td>
                                    <td>{{t.common_meter_rent_2}}</td>
                                    <td>{{t.common_electric_charge}}</td>
                                    <td>{{t.total_electricity_charges}}</td>
                                    <td>{{t.water_charge}}</td>
                                    <td>{{t.coopt_electric_charge}}</td>
                                    <td>{{t.grg_charge}}</td>
                                    <td>{{t.other_charges}}</td>
                                    <td>{{t.net_amount}}</td>
                                    <td>{{t.remarks}}</td>

                                </tbody>
                            </table>
                        </div>
                </div>
                    </div>
                    <router-link to="/quaterbill" class="btn btn-success">Back</router-link>
                    </div>
                    </div>`,
                    data: function() {
                        return {
                    transactions: [],
                        transData: {
                            filter1:'',
                            filter2:'',
                            search1:'',
                            search2:''
                    }
                }
                    },

            mounted(){
                        this.handleSearch
                    },
                    methods:{
                        handleSearch(){
                            fetch('/api/billsearchfil',{
                                method:'POST',
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body:JSON.stringify(this.transData)
                            })
                            .then(response => response.json())
                            .then(data =>{
                                this.transactions=data
                            })
                        }
                    }
                }