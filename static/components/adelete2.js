export default{
    template:`
    <div class="container mt-5">
        <h1 align="center">Waiting for Confirmation</h1>
        <div class="d-flex justify-content-center align-items-center vh-80">
            <div class="alert alert-primary" role="alert" style="width: 800px; height: 300px; padding: 20px; font-size: 18px;">
            <h4>Admin Management</h4>
                <p>Are you sure you want to Delete the Entry</p>
                <p>You are going delete id {{id}} permenantly</p>
                <p>Name:{{staff_name}}---- Quater-Type:{{staff_code}}</p>
                <button class="btn btn-success" @click="save">Confirm+</button>
                <router-link to="/adminbillmod" class="btn btn-warning">Back</router-link>
            </div>
        </div>
    </div>
        `,
                data:function(){
                    return{
                        id:null,
                        staff_name:null,
                        staff_code:null,
                        message:""
                    }
                },   
                mounted(){
                    this.cr()
                },
                methods:{
                    cr(){
                        this.id = this.$route.params.id,
                        this.staff_name= this.$route.params.staff_name
                        this.staff_code=this.$route.params.staff_code
                    },

                    save(){
                        const data12={
                            id : this.$route.params.id,
                            staff_name:this.$route.params.staff_name,
                            staff_code:this.$route.params.staff_code
                        };
                        fetch(`/api/delete/${this.$route.params.id}`,{
                            method:'DELETE',
                            headers: {
                                "Content-Type":'application/json',
                                "Authentication-Token":localStorage.getItem("auth_token")
                            },
                            body:JSON.stringify(data12)
                    }).then(response => response.json())
                    .then(data =>{
                        alert("Succesfully Deleted Redirecting");
                        this.$router.push('/admin');
                    }
                    )}
                    }
                }