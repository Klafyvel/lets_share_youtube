var api_url = "http://localhost:8000";

// Vue.component('playlist', {
//   data: function () {
//     return {
//       url: '#',
//       title: '',
//       is_anonymous: true,
//       owner: ''
//     }
//   },
//   template: '<article><a v-bind:href="url">{{ title }} <span v-if="is_anonymous">by {{owner}}</span></a></article>'
// })


var vm = new Vue({
  delimiters: ['[[', ']]'],
  el: "#playlists",
  data: {
    playlists: [],
    plop: 'plop'
  },
  mounted: function() {
    this.update_playlist();
    setInterval(this.update_playlist, 5000);
  },
  methods: {
    update_playlist: function() {
      axios.get(api_url + "/playlists")
        .then(response => {
            console.log(response.data);
            this.playlists = response.data;
            console.log(this.playlists);
          }
        )
        .catch(
          function (error) {
            console.log(error);
          }
        )
    }
  }
});
