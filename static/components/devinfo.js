export default {
  name: "DeveloperInfo",
  template: `
    <div class="container py-5">
      <!-- Profile Section -->
      <div class="text-center mb-5">
      <h1>College:</h1>
        <img :src="developer.photo" alt="Developer Photo" class="profile-img mb-3" />
        <h1 class="fw-bold">{{ developer.name }}</h1>
        <p class="text-muted">{{ developer.title }}</p>
      </div>

      <!-- About Section -->
      <div class="mb-5">
        <h3 class="section-title">About Me</h3>
        <p>{{ developer.bio }}</p>
      </div>

      <!-- Skills Section -->
      <div class="mb-5">
        <h3 class="section-title">Skills</h3>
        <div class="row">
          <div
            v-for="(skill, index) in developer.skills"
            :key="index"
            class="col-md-3 mb-2"
          >
            <span class="badge bg-primary">{{ skill }}</span>
          </div>
        </div>
      </div>

      <!-- Projects Section -->
      <div class="mb-5">
        <h3 class="section-title">Projects</h3>
        <ul>
          <li v-for="(project, index) in developer.projects" :key="index">
            <strong>{{ project.name }}</strong> – {{ project.description }}
          </li>
        </ul>
      </div>

      <!-- Contact Section -->
      <div>
        <h3 class="section-title">Contact</h3>
        <p><strong>Email:</strong> {{ developer.email }}</p>
        <p><strong>GitHub:</strong>
          <a :href="developer.github" target="_blank">{{ developer.github }}</a>
        </p>
        <p><strong>LinkedIn:</strong>
          <a :href="developer.linkedin" target="_blank">{{ developer.linkedin }}</a>
        </p>
        <p><strong>INFO:</strong>
      <img :src="developer.photo2" alt="Developer Photo" class="profile-img mb-3" style="width: 320px; height: auto;"/>
      </div>
      
      <router-link to="/admin" class="btn btn-warning mt-4">Back</router-link>
    </div>
  `,
  data() {
    return {
      developer: {
        name: "SHUBHAM CHAKRABORTY",
        photo: "static/IITM.png",
        photo2:"static/Linked.png",
        title: "Full Stack Developer | Python | Vue.js | Flask",
        bio: "I'm a passionate full-stack developer, with 1+ years of experience building modern web applications.I am also enthusiats about AI and ML",
        skills: ["Python", "Vue.js", "Flask", "SQL", "Bootstrap",'DBMS','BDM','ML-MODELS'],
        projects: [
          { name: "Mordern Houehold App", description: "Flask-based Household system" },
          { name: "Portfolio Website", description: "Responsive site using Vue & Bootstrap" },
          { name: "Quater-Management App", description: "A full web based app for a running institute of India" },
        ],
        email: "Shubhamrick65@gamil.com",
        github: "https://github.com/Shubham21-rgb/MAD2",
        linkedin: "https://www.linkedin.com/in/shubham-chakraborty-53974a278?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
      },
    };
  },
};
