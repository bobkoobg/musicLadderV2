console.log("Hello World Song.js");


$.song = {
  push: {
    submitSong: function() {
      $.ajax({
        "url": "/song/insert",
        "type": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": JSON.stringify({
          'song-title': $("#song-title").val(),
          'song-url': $("#song-url").val()
        }),
        "success": function(data) {
          console.log("data : ", data);
          // location.reload();
        },
        "error": function(data) {
          console.log("data : ", data);
        }
      });
    }
  }
}
