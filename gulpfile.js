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
  .pipe(gulp.dest('css'));

  gulp.src([
    'theme/js/main.js',
    'theme/js/test.js',
  ])
  .pipe(concat('main.js'))
  // .pipe(uglify())
  .pipe(gulp.dest('js'));

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
