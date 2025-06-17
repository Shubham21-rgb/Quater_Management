export default{
    template:`
            <div class="container mt-5">
        <h1 align="center">Waiting for Confirmation</h1>
        <div class="d-flex justify-content-center align-items-center vh-80">
            <div class="alert alert-primary" role="alert" style="width: 800px; height: 200px; padding: 20px; font-size: 18px;">
            <h4>Admin Management</h4>
                <p>Are you sure you want to Accept the request</p>
                <p>You are going to change the status from {{status}} to Accepted for id {{id}}</p>
                <button class="btn btn-success" @click="save">Confirm</button>
                <router-link to="/admin" class="btn btn-warning">Back</router-link>
            </div>
        </div>
    </div>
        `,
                data:function(){
                    return{
                        id:null,
                        status:null,
                        message:""
                    }
                },
                mounted(){
                    this.cr()
                },
                methods:{
                    cr(){
                        this.id = this.$route.params.id,
                        this.status= this.$route.params.status
                    },

                    save(){
                        const data12={
                            id : this.$route.params.id,
                            status: this.$route.params.status
                        };
                        fetch(`/api/accept/${this.$route.params.id}`,{
                            method:'POST',
                            headers: {
                                "Content-Type":'application/json',
                                "Authentication-Token":localStorage.getItem("auth_token")
                            },
                            body:JSON.stringify(data12)
                    }).then(response => response.json())
                    .then(data =>{
                        console.log(data);
                        const message=data;
                        alert("Succesfull");
                        this.$router.push('/admin');
                    }
                    )}
                    }
                }   