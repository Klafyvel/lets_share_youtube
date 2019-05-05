var vm = new Vue({
  delimiters: ['[[', ']]'],
  el: "#app",
  data: {
    playlists: [],
  },
  mounted: function() {
    this.update_playlist();
    setInterval(this.update_playlist, 5000);
  },
  methods: {
    update_playlist: function() {
      api.get(api_url + "/playlists")
        .then(response => {
            this.playlists = response.data;
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
