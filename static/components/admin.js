import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
   <div>
    <n></n>
  <div class="d-flex align-items-center gap-3 login-box">
  <h2 class="my-2">Welcome, {{userData.username}}!</h2>
  <div class="dropdown">
    <button class="btn btn-secondary dropdown-toggle" type="button" id="adminDropdown" data-bs-toggle="dropdown" aria-expanded="false">
      QUATER-BILLING
    </button>
    <ul class="dropdown-menu" aria-labelledby="adminDropdown">
      <li><router-link to="/quaterbill" ><i class="fas fa-search">Quaterbill</i></router-link></li>
    </ul>
  </div>
</div>

        <div class="row border">
            <div class="text-end"><router-link to="/adminupdate" class="btn btn-warning">-----------Modify-Entries------------</router-link></div><br><br>
            <div class="text-center"><router-link to="/adminsummary" class="btn btn-success"><i class="bi bi-search">---------------------------- Search------------------------</i> </router-link></div>
        </div>
            <div class="row border">
                <div class="col-10 border" style="height: 800px; overflow-y: scroll" >
                    <h2>Master Control</h2>
                    <p>Complete List</p>
                        <div v-for="t in transactions" class="card mt-2" style="width:2000px">
                            <table class="table table-success table-striped "  >  
                                <thead class="table table-success table-striped">
                                    <tr>
                                    <th scope="col" class="px-4">Sl.No</th>
                                    <th scope="col" class="px-4">Name</th>  
                                    <th scope="col" class="px-4">Designation</th>
                                    <th scope="col" class="px-4">Quater-Type</th>
                                    <th scope="col" class="px-4">Area</th>
                                    <th scope="col" class="px-4">Date-Of-Allotment</th>
                                    <th scope="col" class="px-4">Date Of Vacation</th>
                                    <th scope="col" class="px-4">Year-Of Construction</th>
                                    <th scope="col" class="px-4">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <td class="px-4">{{t.id}}</td>
                                    <td class="px-4">{{t.name}}</td>
                                    <td class="px-4">{{t.Designation}}</td>
                                    <td class="px-4">{{ t.Type_of_Quater }}</td>
                                    <td class="px-4">{{t.Area}}</td>
                                    <td class="px-4">{{t.Date_of_allotment}}</td>
                                    <td class="px-4">{{t.Date_Of_Vacation}}</td>
                                    <td class="px-4">{{t.Year_of_construction}}</td>
                                    <td class="px-4">{{t.Status}}</td>
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
                    <div class="text-end"><router-link to="/newallot" class="btn btn-secondary btn-lg">New-Allotment</router-link></div>
                    </div>
            </div>
        </div>
        <button @click="csvd" class="btn btn-warning">
                             Download Report    <i class="bi bi-download"></i>
                        </button>
        <div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/into.mp4" type="video/mp4" />
      Your browser does not support the video tag.
        </video></div>
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
            fetch('/api/get', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": localStorage.getItem("auth_token")
                }
            })
            .then(response => response.json())
            .then(data => {
                this.transactions = data
                console.log(data)
            })
        },csvd() {
    fetch('/downloadcsv', {
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