$.tournament = {
  push: {
    startCup: function( tournament_id ) {
      $.ajax({
        "url": "/init/tournament/cup/"+tournament_id,
        "type": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": JSON.stringify({}),
        "success": function(data) {
          console.log("data : ", data);
          location.reload();
        },
        "error": function(data) {
          console.log("data : ", data);
        }
      });
    },
    submitMatch: function() {
      $.ajax({
        "url": "/game/"+$(".matchmaking-wrapper").attr("data-game-id"),
        "type": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": JSON.stringify({
          'tournament-id': parseInt($(".matchmaking-wrapper").attr("data-tournament-id")),
          'song-left-id': parseInt($(".matchmaking-wrapper").attr("data-song-left-id")),
          'song-right-id': parseInt($(".matchmaking-wrapper").attr("data-song-right-id")),
          'song-left-score': parseInt($("#left-song-points").html()),
          'song-right-score': parseInt($("#right-song-points").html())
        }),
        "success": function(data) {
          console.log("data : ", data);
          location.reload();
        },
        "error": function(data) {
          console.log("data : ", data);
        }
      });
    }
  },
  loadChart: function() {

    var ctx = document.getElementById("myChart");

    if(ctx == undefined) {
      return;
    } else {
      ctx.getContext('2d');
    }

    var bgColors = [
      'rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)','rgba(153, 102, 255, 0.2)','rgba(255, 159, 64, 0.2)'];
    var brdColor = [
      'rgba(255,99,132,1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)',
      'rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)'];
    var datasets = [];
    var labels = [];
    var i = 0;
    for (var k in song_tournament_rating) {
        labels.push(i+1);
        datasets.push({
          'label': song_tournament_rating[k]['song_title'],
          'data':  song_tournament_rating[k]['song_ratings'],
          'backgroundColor': bgColors[i % Object.keys(song_tournament_rating).length],
          'borderColor': brdColor[i % Object.keys(song_tournament_rating).length],
          'borderWidth': 1
        })
        i++;
    }

    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        }
    });
  },
  loadSlider: function() {
    $( "#slider" ).slider({
      value:5,
      min: 0,
      max: 10,
      step: 1,
      slide: function( event, ui ) {
        console.log(" ? ", ui.value);
        $("#left-song-points").html(ui.value);
        $("#right-song-points").html(10-ui.value);
        console.log("> ", ui.value + " : " + (10-ui.value));
        $("#current-result").html( ui.value + " : " + (10-ui.value) );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
  },
  loadProjectedResults: function() {
    var ctx = document.getElementById("projected-results-chart");

    if(ctx == undefined) {
      return;
    } else {
      ctx.getContext('2d');
    }

    var bgColors = [
      'rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)','rgba(153, 102, 255, 0.2)','rgba(255, 159, 64, 0.2)'];
    var brdColor = [
      'rgba(255,99,132,1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)',
      'rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)'];
    var datasets = [];
    var labels = [];
    var i = 0;
    song_ratings = {
      'left': [],
      'right': []
    };
    for (var k in projected_results['results']) {
      labels.push(projected_results['results'][k]['l_score'] + ":" + projected_results['results'][k]['r_score']);
      song_ratings['left'].push(projected_results['results'][k]['l_rating'])
      song_ratings['right'].push(projected_results['results'][k]['r_rating'])
    }

    datasets = [{
      'label': projected_results['title']['left'],
      'data': song_ratings['left'],
      'backgroundColor': bgColors[0],
      'borderColor': brdColor[0],
      'borderWidth': 1
    },{
      'label': projected_results['title']['right'],
      'data': song_ratings['right'],
      'backgroundColor': bgColors[1],
      'borderColor': brdColor[1],
      'borderWidth': 1
    }];

    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        }
    });
  }
}

$.tournament.loadChart();
$.tournament.loadSlider();
$.tournament.loadProjectedResults();
