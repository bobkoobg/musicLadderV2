var gulp = require('gulp');
var sass = require('gulp-sass');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const watch = require('gulp-watch');

function defaultTask(cb) {
  console.log("\t\tYes, I work");
  cb();
}

function productionTask(cb) {
  console.log("\t\tProduction!");

  gulp.src([
    'theme/scss/main.scss',
    'theme/scss/test.scss'
  ])
  .pipe(sass())
  .pipe(concat('main.css'))
  .pipe(gulp.dest('static/css'));

  gulp.src([
    'theme/scss/framework/metisMenu-vertical.scss',
    'theme/scss/framework/metisMenu.min.scss'
  ])
  .pipe(sass())
  .pipe(concat('libs.css'))
  .pipe(gulp.dest('static/css'));

  gulp.src([
    'theme/scss/flexee.scss'
  ])
  .pipe(sass())
  .pipe(concat('flexee.css'))
  .pipe(gulp.dest('static/css'));

  gulp.src([
    'theme/js/main.js',
    'theme/js/test.js'
  ])
  .pipe(concat('main.js'))
  .pipe(gulp.dest('static/js'));

  gulp.src([
    'theme/js/framework/chart-2.7.3.min.js',
    'theme/js/framework/chartbundle-2.7.3.min.js',
    'theme/js/framework/metisMenu.min.js',
    'theme/js/framework/metisMenu-active.js'
  ])
  .pipe(concat('libs.js'))
  .pipe(uglify())
  .pipe(gulp.dest('static/js'));

  gulp.src([
    'theme/js/framework/jquery-3.3.1.min.js'
  ])
  .pipe(concat('jquery.js'))
  .pipe(uglify())
  .pipe(gulp.dest('static/js'));

  cb();
}

// gulp.task('stream', function () {
// 	// Endless stream mode
//     return watch('scss/**/*.scss', { ignoreInitial: false })
//       .pipe(sass())
//       .pipe(concat('main.css'))
//       .pipe(gulp.dest('css'));
// });
//
// gulp.task('callback', function () {
// 	// Callback mode, useful if any plugin in the pipeline depends on the `end`/`flush` event
//   return watch('scss/**/*.scss', function () {
//       gulp.src('scss/**/*.scss')
//         .pipe(sass())
//         .pipe(concat('main.css'))
//         .pipe(gulp.dest('css'));
//   });
// });

exports.default = defaultTask
exports.production = productionTask
