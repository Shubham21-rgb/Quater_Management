import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
   <div>
    <n></n>
  <div class="d-flex align-items-center gap-3 login-box">
  <h2 class="my-2">QUATER BILL STATEMENT</h2>
</div>
<div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/into.mp4" type="video/mp4" />
      Your browser does not support the video tag.
        </video></div>

        <div class="row border login-box">
            <div class="text-end"><router-link to="/adminbillmod" class="btn btn-warning">---------------Modify-Bill---------------</router-link></div><br>
            <div class="text-center"><router-link to="/billsearch" class="btn btn-success"><i class="bi bi-search">---------------------------- Search------------------------</i> </router-link></div>
        </div>
            <div class="row border login-box">
                <div class="col-10 border" style="height: 750px; overflow-y: scroll">
                    <h2>Master Control</h2>
                    <p>Complete List</p>
                        <div v-for="t in transactions" class="card mt-2" style="width:4000px">
                            <table class="table table-bordered table-striped align-middle">
                                <thead class="table table-success table-striped">
                                    <tr>
                                    <th scope="col">Sl_no</th>
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
                                    <th scope="col">net_amount</th>
                                    <th scope="col">remarks</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <td>{{t.Sl_no}}</td>
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
            <div class="col-2 border" style="height: 750px;">
                <h4>Click Here For New Entry</h4>
                <br><br><br><br><br><br><br><br><br><br>
                    <div class="mb-3">
                    <div class="spinner-grow text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="text-end"><router-link to="/billnewentry" class="btn btn-secondary btn-lg">New-Entry</router-link></div>
                    </div>
            </div>
        </div>
        <button @click="csvd" class="btn btn-warning">
             Download Report    <i class="bi bi-download"></i>
            </button>
        <router-link to="/admin" class="btn btn-success">Back</router-link>
    </div>`,
    data: function(){
        return {
            userData: "",
            transactions: null,
            transData: {
                id: '',
                amount: '',
                service_name: '',
                Time_required: '',
                Description: '',
                prof_id:''
            },
            message:""

            
        }
    },
    mounted(){
        this.loadUser()
        this.loadTrans() 
    },
    methods:{
        loadUser(){
            fetch('/api/home', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => this.userData = data)
        },
        loadTrans(){
            fetch('/api/getvalofbill', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {
                this.transactions = data
            })
        },csvd() {
    fetch('/downloadbillcsv', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(this.transactions)
    })
    .then(response => {
        const disposition = response.headers.get("Content-Disposition");
        let filename = "download.csv"; 

        if (disposition && disposition.indexOf("filename=") !== -1) {
            filename = disposition
                .split("filename=")[1]
                .replace(/['"]/g, '');
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
    });
}
    }

}