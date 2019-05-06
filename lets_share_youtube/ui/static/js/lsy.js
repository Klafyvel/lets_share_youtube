const api_url = "http://localhost:8000";

const api = axios.create({
  baseURL: api_url,
  timeout: 1000,
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});



function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

Vue.component('modal', {
  template: '#modal-template'
})

var lsy = new Vue({
  delimiters: ['[[', ']]'],
  el: "#main-nav",
  data: {
    show_create: false,
    show_login: false,
    show_msg: false,
    msg: "",
    logged: false,
    username: "",
    domain: "",
    create_id: "",
  },
  mounted: function () {
    this.domain = document.domain;
    setInterval(this.check_logged,5000);
    setInterval(this.renew_token, 50000);
    this.check_logged();
  },
  methods: {
    message: function(msg) {
      this.msg = msg;
      this.show_msg = true;
    },
    login: function () {
      var username = this.$refs.username.value;
      var login_form_data = new FormData();
      login_form_data.set('username', username);
      login_form_data.set('csrfmiddlewaretoken', readCookie('csrftoken'));
      login_form_data.set('password', this.$refs.password.value);
      login_form_data.set('next', '/accounts/am_i_logged/');
      api.post(
        '/accounts/login/',
        login_form_data
      )
        .then(response => {
          this.show_login = false;
          if(response.headers["content-type"].includes('application/json')) {
            this.username = response.data.user;
            this.logged = true;
            this.message("Welcome back " + this.username + " !");
          }
          else {
            this.message("Wrong username or password.");
          }
        })
        .catch(function (error) {
          this.logged = false;
          console.log(error);
        })
    },
    logout: function () {
      axios.get(
        '/accounts/logout/'
      ).then(() => {
          this.logged = false;
          this.message("Hope you had fun, see you soon " + this.username + " !");
      }).catch(function (error) {
        this.logged = false;
        console.log(error)
      })
    },
    check_logged: function () {
      api.get(
        '/accounts/am_i_logged/',
      ).then((response) => {
        this.logged = true;
        this.username = response.data.user
      }).catch(function (error) {
        this.logged = false;
      })
    },
    create: function () {
      console.log('coin');
      api.post(
        '/playlists/',
        {
          title: this.$refs.title.value,
          token: this.$refs.id.value,
          public: this.$refs.public.value
        }
      ).then((response) => {
        window.location.href = '/p/' + response.data.token;
      }).catch(function (error) {
        console.log(error);
      })
    }
  }
})
