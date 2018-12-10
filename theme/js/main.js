$.main = {
  navigation: {
    open: function() {
      document.getElementById("sidenav").style.width = "250px";
    },
    close: function() {
      document.getElementById("sidenav").style.width = "0";
    }
  }
}
