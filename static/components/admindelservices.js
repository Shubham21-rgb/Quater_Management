import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
   <div>
    <n></n>
    <div class="row border">
    <h5>Are you sure you want to delete</h5>
    <p>Deleting Details</p>
    <p>Service Type:{{service}}</p>
    <p>Time-Required:{{time}}</p>
    <p>Description:{{desc}}</p>
    <p>Amount:{{amount}}</p>
    <p>Unique ID is {{unique}}</p>
        <button @click="save" class="btn btn-success">Confirm</button>
        <router-link to="/adminupdate" class="btn btn-warning">Back</router-link>
    </div>
    </div>`,
            data:function(){
                return{
                    id:null,
                    service:null,
                    time:null,
                    desc:null,
                    amount:null,
                    unique:null,
                    }
                },
                    mounted(){
                        this.cr()
            
                    },
                    methods:{
                        cr(){
                            this.id = this.$route.params.id,
                            this.service=this.$route.params.service,
                            this.time=this.$route.params.time,
                            this.desc=this.$route.params.desc,
                            this.amount=this.$route.params.amount,
                            this.unique=this.$route.params.unique
                        },
                        save(){
                            fetch(`/api/delete/${this.$route.params.id}`,{
                                method:'DELETE',
                                headers: {
                                    "Content-Type":'application/json',
                                    "Authentication-Token":localStorage.getItem("auth_token")
                                }
                            })
                            .then(response => response.json())
                            .then(data =>{
                                console.log(data);
                                let message=data;
                                alert(message);
                                this.$router.push('/adminupdate');
                            }
                            )
                    }
                    }
                }