import Home from './components/Home.js' 
import Login from './components/Login.js' 
import Register from './components/Register.js' 
import Navbar from './components/Navbar.js' 
import Footer from './components/Footer.js' 

import admin from './components/admin.js'
import adminsearch from './components/adminsearch.js'
import admindelserv from './components/admindelserv.js'
import adminserviceupdate from './components/adminserviceupdate.js'
import admindelservices from './components/admindelservices.js'
import adminsummary from './components/adminsummary.js'
import Quaterbill from './components/Quaterbill.js'
import adminbillsearch from './components/adminbillsearch.js'
import billentry from './components/billentry.js'
import adminbillmodifyentry from './components/adminbillmodifyentry.js'
import adminbillmodify from './components/adminbillmodify.js'
import adelete from './components/adelete.js'
import allotment from './components/allotment.js'
import adelete2 from './components/adelete2.js'
import devinfo from './components/devinfo.js'

const routes=[
    {path: '/',component: Home},
    {path: '/login',component: Login},
    {path: '/register',component: Register},
    {path:'/adminserviceupdate/:id',name:'adminserv',component:adminserviceupdate},
    {path:'/adminservicedelete/:id',name:'admindelservice',component:admindelservices},
    {path:'/admin',component:admin},
    {path:'/adminupdate',component:admindelserv},
    {path:'/adminsearchin',component:adminsearch},
    {path:'/adminsummary',component:adminsummary},
    {path:'/quaterbill',component:Quaterbill},
    {path:'/billsearch',component:adminbillsearch},
    {path:'/billnewentry',component:billentry},
    {path:'/adminbillmodifyentry/:id',name:'adminserv2',component:adminbillmodifyentry},
    {path:'/adminbilldelete/:id',name:'deletebill',component:adelete},
    {path:'/adminbilldeletequaters/:id',name:'deletebillsnew',component:adelete2},
    {path:'/adminbillmod',component:adminbillmodify},
    {path:'/newallot',component:allotment},
    {path:'/developer/info',component:devinfo}
    

]
const router=new VueRouter({ 
    routes

})
const app = new Vue({
    el:"#app",
    router,
    template:`
    <div class="container">Welcome To Our Portal from Developer
    <router-view></router-view>
    <foot></foot>
    </div>
    `,
    data:{
        section:"frontend"
    },
    components:{
        "nav-bar":Navbar,
        "foot":Footer
    }
})