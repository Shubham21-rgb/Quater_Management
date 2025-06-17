import Navbar from "./Navbar.js"

export default {
  components: {
    'n': Navbar
  },
  template: `
  <div>
    <!-- Video Background -->
    <!-- Optional dark overlay -->

    <!-- Content -->
    <div class="row border content-container login-box">
      <n></n>
      <div class="col" style="height: 750px; width:600px;" >  
        <div class="border mx-auto mt-5 login-box"  style="height: 600px; width: 500px;">
          Login-Area
          <div>
            <h2 class="text-center">Login-Form</h2>
            <div>
              <label for="email" class="col-sm-2 col-form-label">Email:</label>
              <input type="text" id="email" class="form-control" v-model="formData.email">
            </div>
            <div>
              <label for="pass" class="col-sm-2 col-form-label">Password:</label>
              <input type="password" id="pass" class="form-control" v-model="formData.password">
            </div>
            <div>{{message}}</div>
            <div>
              <br><br>
              <button class="btn btn-primary" @click="loginUser">Login</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/NITDGP.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video></div>
  </div>
  `,
  data: function () {
    return {
      formData: {
        email: "",
        password: ""
      },
      message: ""
    }
  },
  methods: {
    loginUser: function () {
      fetch('/api/login', {
        method: 'POST',
        headers: {
          "Content-Type": 'application/json'
        },
        body: JSON.stringify(this.formData)
      })
        .then(response => response.json())
        .then(data => {
          if (Object.keys(data).includes('auth-token')) {
            localStorage.setItem("auth_token", data["auth-token"])
            if (data.roles.includes('admin')) {
              this.$router.push('/admin')
            } else if (data.roles.includes('user')) {
              this.$router.push('/dashboard')
            } else {
              this.$router.push('/pdashboard')
            }
          } else {
            this.message = data.message
          }
        })
    }
  }
}
