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
