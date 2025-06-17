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
                    <h2>Update---->Entries</h2>
                            <div class="d-flex align-items-center gap-3 my-3">
                                <i class="bi bi-search"></i><input v-model="transData.search" type="text" class="form-control" placeholder="......................Search....................">
                                <div class="d-flex align-items-center">
                                    <label for="source" class="form-label"> Filter-By</label>
                                    <select class="form-select" aria-label="Default select example" v-model="transData.filter">
                                        <option selected>Open this select menu</option>
                                        <option value="name">Name</option>
                                        <option value="dg">Designation</option>
                                        <option value="qt">Quater-Type</option>
                                        <option value="area">Area</option>
                                        <option value="doa">Date Of Allotment</option>
                                        <option value="yoc">Year Of Construction</option>
                                    </select>
                                </div>
                        </div>

                        <button @click="handleSearch" class="btn btn-warning">
                            <i class="bi bi-search">Search</i>
                        </button>

                        <div v-for="t in transactions"  class="card mt-2" style="width:1300px">
                            <table class="table table-bordered table-striped align-middle">
                                <thead class="table table-success table-striped">
                                    <tr>
                                    <th scope="col">Sl.No</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Designation</th>
                                    <th scope="col">Quater-Type</th>
                                    <th scope="col">Area </th>
                                    <th scope="col">Date Of Allotment</th>
                                    <th scope="col">Date Of Vacation</th>
                                    <th scope="col">Year Of Construction</th>   
                                    <th scope="col">Remarks</th>
                                    <th scope="col">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <td>{{t.id}}</td>
                                    <td>{{t.name}}</td>
                                    <td>{{t.Designation}}</td>
                                    <td>{{t.Type_of_Quater}}</td>
                                    <td>{{t.Area}}</td>
                                    <td>{{t.Date_of_allotment}}</td>
                                    <td>{{t.Date_Of_Vacation}}</td>
                                    <td>{{t.Year_of_construction}}</td>
                                    <td>{{t.Remarks}}</td>
                                    <td><router-link :to="{name:'adminserv',params:{id: t.id,name:t.name,Designation:t.Designation,Date_of_allotment:t.Date_of_allotment,Type_of_Quater:t.Type_of_Quater,Area:t.Area,Date_Of_Vacation:t.Date_Of_Vacation,Year_of_construction:t.Year_of_construction}}" class="btn btn-warning">Update</router-link></td>
                                    <td><router-link :to="{name:'deletebillsnew',params:{id: t.id,staff_name:t.name,staff_code:t.Type_of_Quater}}" class="btn btn-danger">Delete</router-link></td>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <br><br>
                    </div>
                    <router-link to="/admin" class="btn btn-success">Back</router-link>
                    </div>`,
                    data:function(){
                        return{
                            transactions:null,
                            transactions1:null,
                            transData:{
                                search:'',
                                filter:''
                            }
                        }
                    },
                    mounted(){
                        this.loadservice()
                    },
                    methods:{
                        loadservice(){
                            fetch('/api/adminser',{
                                method:'POST',
                                headers: {
                                    "Content-Type": "application/json",
                                    "Authentication-Token": localStorage.getItem("auth_token")
                                }
                            })
                            .then(response => response.json())
                            .then(data =>{
                                this.transactions1=data
                            })
                        },
                        handleSearch(){
                                fetch('/api/adminsearchin',{
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

