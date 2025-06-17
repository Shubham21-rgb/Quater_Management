export default{
    template:`
    <div class="container mt-5">
        <h1 align="center">Waiting for Confirmation</h1>
        <div class="d-flex justify-content-center align-items-center vh-80">
            <div class="alert alert-primary" role="alert" style="width: 800px; height: 200px; padding: 20px; font-size: 18px;">
            <h4>Admin Management</h4>
                <p>Are you sure you want Change the status of service</p>
                <p>Changing Status {{status}} to Closed for id-{{id}}</p>
                <button class="btn btn-success" @click="save">Procced</button>
                <router-link to="/admin" class="btn btn-warning">Back</router-link>
            </div>
        </div>
    <div>
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
                        fetch(`/api/aclose/${this.$route.params.id}`,{
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
                        alert("Changed Succesfully");
                        this.$router.push('/admin');
                    }
                    )}
                    }
                }