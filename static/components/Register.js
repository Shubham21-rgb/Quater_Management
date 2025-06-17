import Navbar from "./Navbar.js"
export default{
    components:{
        'n':Navbar,
    },
    template:`
    <div class="row border">
    <n></n>
        <div class="col" style="height: 750px;" >
            <div class="border mx-auto mt-5" style="height: 600px; width: 500px;">
                This is to inform this is ony base registartion page addition info can be added once you enter the User-dashboard
            <div class="container w-100">
    <h2 class="text-center">User-Registration-Form</h2>
    <div>
        <label for="email" class="col-sm-2 col-form-label">Enter Your Email:</label>
        <input type="text" id="email" class="form-control" v-model="formData.email">
    </div>
    <div>
        <label for="pass" class="col-sm-2 col-form-label">Create Username:</label>
        <input type="text" class="form-control" id="pass" v-model="formData.username" placeholder="Username must be unique">
    </div>
    <div>
        <label for="pass" class="col-sm-2 col-form-label">Create  Password:</label>
        <input type="password" class="form-control" id="pass" v-model="formData.password">
    </div>
    <div>{{message}}</div>
    <div>
        <button class="btn btn-primary" @click="RegisUser">Register</button>
    </div>
</div>
            </div>
        </div>
    </div>`,
    data: function(){
        return{
            formData:{
                email:"",
                username:"",
                password:""
            },
            message:""
        }
    },
    methods:{
        RegisUser: function(){
            fetch('/api/cregister',{
                method: 'POST',
                headers: {
                    "Content-Type":'application/json'
                },
                body:JSON.stringify(this.formData)

            })
            .then(response => response.json())
            .then(data=>alert(data.message),
                this.$router.push('/login'))
                  
        }
    }
}  

