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
                <p>Update Service------------->>  id-{{id}}</p>
                <h4>Update Entry Details</h4>
                <p>SL.No:{{id}}</p>
                <p>Name:{{name1}}</p>
                <p>Date Of Allotment:{{Date_of_allotment1}}</p>
                <p>Quater-Type:{{Type_of_Quater1}}</p>
                <p>Area:{{Area1}}</p>
                <p>Year_of_construction:{{Year_of_construction1}}</p>
                <p>Date_Of_Vacation:{{Date_Of_Vacation1}}</p>
                <p>Designation:{{Designation1}}</p>


                <div class="mb-3">
                    <label for="type" class="form-label">Name</label>
                    <input type="text" class="form-control" id="amount" v-model="date.name">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Date Of Allotment</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Date_of_allotment">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Date Of Vacation</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Date_Of_Vacation">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Quater_Type</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Type_of_Quater">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Designation</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Designation">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Area</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Area">
                </div>
                
                <div class="mb-3">
                    <label for="type" class="form-label"> Year Of Construction</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Year_of_construction">
                </div>
                <div class="mb-3">
                    <label for="type" class="form-label"> Status</label>
                    <input type="text" class="form-control" id="amount" v-model="date.Status">
                </div>
                <button class="btn btn-success" @click="save">Save+</button>
                <router-link to="/adminupdate" class="btn btn-warning">Back</router-link>
            </div>
        </div>
    </div>
        `,
                data:function(){  
                    return{
                        id:null,
                        name1:null,
                        Date_of_allotment1:null,
                        Type_of_Quater1:null,
                        Area1:null,
                        Year_of_construction1:null,
                        Date_Of_Vacation1:null,
                        Designation1:null,


                        date: {
                            name:'',
                            Date_of_allotment:'',
                            Type_of_Quater:'',
                            Area:'',
                            Year_of_construction:'',
                            Date_Of_Vacation:'',
                            Remarks:'',
                            Designation:''
                        }
                    }
                },
                mounted(){
                    this.cr()
                },
                methods:{
                    cr(){
                        this.id = this.$route.params.id,
                        this.name1=this.$route.params.name,
                        this.Date_of_allotment1=this.$route.params.Date_of_allotment,
                        this.Type_of_Quater1=this.$route.params.Type_of_Quater,
                        this.Area1=this.$route.params.Area,
                        this.Year_of_construction1=this.$route.params.Year_of_construction,
                        this.Date_Of_Vacation1=this.$route.params.Date_Of_Vacation,
                        this.Designation1=this.$route.params.Designation
                      
                    },

                    save(){
                        fetch(`/api/update/${this.$route.params.id}`,{
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
                        this.$router.push('/adminupdate');

                    }
                    )}
                    }
                }