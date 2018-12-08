var ctx = document.getElementById("myChart").getContext('2d');

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
      'borderColor': bgColors[i % Object.keys(song_tournament_rating).length],
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
