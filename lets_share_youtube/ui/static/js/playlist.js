Vue.component('video-card', {
  delimiters: ['[[', ']]'],
  template: '#video-template',
  props: ['token', 'title', 'index', 'url']
  // data: function () {
  //   return {
  //     token: "",
  //     title: ""
  //   }
  //}
});

var vm = new Vue({
  delimiters: ['[[', ']]'],
  el: "#app",
  data: {
    playlist: [],
    title: "",
    player: null,
    current: -1
  },
  mounted: function() {
		Notification.requestPermission();
    this.update_playlist();
    axios.get(api_url + "/playlists/" + playlist_token)
      .then(response => {
        this.title = response.data.title;
      })
      .catch(
        function (error) {
          console.log(error);
        }
      )
    setInterval(this.update_playlist, 5000);
  },
  methods: {
		error: function (msg) {
			new Notification('LSY Error', { body: msg });
		},
		notify_current: function (name) {
			new Notification('LSY now playing', { body: name });
		},
		notify_added: function (name) {
			new Notification('LSY', { body: 'Successfully added ' + name + ' to ' + this.title });
		},
		notify_deleted: function (name) {
			new Notification('LSY', { body: 'Successfully removed ' + name + ' from ' + this.title });
		},
    update_playlist: function() {
      axios.get(api_url + "/playlists/" + playlist_token + '/videos')
        .then(response => {
            this.playlist = response.data;
						var playing_token = this.player.getVideoData().video_id;
						var current = Math.min(this.current, this.playlist.length - 1);
						if (playing_token != this.playlist[current].token) {
							this.set_current(current);
						}
          }
        )
        .catch(error => {
            this.error(error);
          }
        )
    },
    play: function () {
      this.player.playVideo();
    },
		pause: function () {
			this.player.pauseVideo();
		},
    set_current: function (index) {
			console.log("Setting current to " + index);
      if (index >= 0 && index < this.playlist.length) {
        this.current = index;
				this.player.loadVideoById(this.playlist[this.current].token);
				this.notify_current(this.playlist[this.current].title);
        this.play();
      }
    },
    next: function () {
      this.set_current(this.current + 1);
		},
 		prev: function () {
      this.set_current(this.current - 1);
		},
    on_player_ready: function (event) {
      if(this.playlist.length > 0 && this.current < (this.playlist.length - 1)) {
            this.next();
        }
    },
		on_player_state_change: function (event) {
			if (event.data == YT.PlayerState.ENDED) {
				this.next();
  		}
		},
		add_video: function () {
			var url = this.$refs.url.value;
			axios.post(
				api_url + '/playlists/' + playlist_token + '/videos/from_url/',
				{
					url: url
				})
				.then(() => {
					this.update_playlist();
					this.$refs.url.value = "";
					this.notify_added(url)
				})
				.catch(error => {
					this.error(error);
				});
		},
		up_video: function (url) {
			axios.post(url + 'up/', {})
				.then(this.update_playlist)
				.catch(error => {
					this.error(error);
				});
		},
		down_video: function (url) {
			axios.post(url + 'down/', {})
				.then(this.update_playlist)
				.catch(error => {
					this.error(error);
				});
		},
		delete_video: function (data) {
			console.log('plop');
			axios.delete(data.url)
				.then(() => {
					this.notify_deleted(data.title);
					this.update_playlist();
				})
				.catch(error => {
					this.error(error);
				});
		}
  }
});

function onYouTubeIframeAPIReady() {
  vm.player = new YT.Player('player', {
    height: '390',
    width: '640',
    events: {
      'onReady': vm.on_player_ready,
      'onStateChange': vm.on_player_state_change
    }
  });
}
