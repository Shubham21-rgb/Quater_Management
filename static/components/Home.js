import Navbar from "./Navbar.js"
export default{
    components:{
        'n':Navbar,
    },
    template:`
    <div class="row border login-box">
    <n></n>
        <div class="col" style="height: 750px;">
            <div class="border mx-auto mt-5 login-box" style="height: 700px; width: 600px;">
                <img src="static/Quater_manage.png" class="img-fluid rounded mx-auto d-block" alt="Home">
            </div>
        </div>
        <div class="overlay"><video autoplay muted loop id="bg-video">
      <source src="static/into.mp4" type="video/mp4" />
      Your browser does not support the video tag.
        </video></div>
    </div>`
}