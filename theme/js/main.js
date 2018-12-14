$.main = {
  navigation: {
    open: function() {
      document.getElementById("sidenav").style.width = "250px";
      document.getElementById("sidenav").style.borderRight = "2px solid #818181";
      document.getElementById("slider-wrapper").style.marginLeft = "240px";
    },
    close: function() {
      document.getElementById("sidenav").style.width = "0";
      document.getElementById("sidenav").style.borderRight = "";
      document.getElementById("slider-wrapper").style.marginLeft = "0px";
    }
  }
}
