import adminnav from "./adminnav.js"
export default {
    components:{
       "n": adminnav
    },
    template: `
   <div>
    <n></n>
    <div class="row border">
                <div class="col-12 border" style="height: 750px; overflow-y: scroll">
                    <h2>Search Area</h2>
                            <div class="d-flex align-items-center gap-3 my-3">
                                <input v-model="transData.search" type="text" class="form-control" placeholder="......................Search....................">
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

                        <div v-for="t in transactions"  class="card mt-2">
                            <table class="table table-bordered table-striped align-middle">
                                <thead class="bg-info text-white">
                                    <tr>
                                    <th scope="col">Sl.No</th>
                                    <th scope="col">Name</th>
                                    <th scope="col">Designation</th>
                                    <th scope="col">Quater-Type</th>
                                    <th scope="col">Area </th>
                                    <th scope="col">Date Of Allotment</th>
                                    <th scope="col">Year Of Construction</th>
                                    <th scope="col">Remarks</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <td>{{t.id}}</td>
                                    <td>{{t.name}}</td>
                                    <td>{{t.Designation}}</td>
                                    <td>{{t.Type_of_Quater}}</td>
                                    <td>{{t.Area}}</td>
                                    <td>{{t.Date_of_allotment}}</td>
                                    <td>{{t.Year_of_construction}}</td>
                                    <td>{{t.Remarks}}</td>
                                </tbody>
                            </table>
                        </div>
                        <button @click="csvd" class="btn btn-warning">
                            <i class="bi bi-search">Download Report</i>
                        </button>
                    </div>
                    <router-link to="/admin" class="btn btn-success">Back</router-link>
                    </div>
                    </div>`,
                    data:function(){
                        return{
                            transactions:null,
                            transData:{
                                search:'',
                                filter:''
                            }
                        }
                    },
                    mounted(){
                        this.handleSearch
                    },
                    methods:{
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
                        },
                        csvd() {
    fetch('/downloadcsv', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(this.transactions)
    })
    .then(response => {
        const disposition = response.headers.get("Content-Disposition");
        let filename = "download.csv"; 

        if (disposition && disposition.indexOf("filename=") !== -1) {
            filename = disposition
                .split("filename=")[1]
                .replace(/['"]/g, '');
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
    .then(({ blob, filename }) => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
    });
}
                    }
                }