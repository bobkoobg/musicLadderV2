var gulp = require('gulp');
var sass = require('gulp-sass');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const watch = require('gulp-watch');

function scssJob(){
  console.log("\t\tscssJob");
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
}

function jsJob(){
  console.log("\t\tjsJob");
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
}

function productionJob() {
  console.log("\t\tproductionJob");
  scssJob();
  jsJob();
}

function defaultTask(cb) {
  console.log("\t\tdefaultTask");
  productionJob();
  cb();
}

function productionTask(cb) {
  console.log("\t\tproductionTask");
  productionJob();
  cb();
}

function watchTask(cb) {
  console.log("\t\twatchTask");
  gulp.watch('theme/scss/*.scss', gulp.series('production'));
  gulp.watch('theme/js/*.js', gulp.series('production'));
  cb();
}

exports.default = defaultTask
exports.production = productionTask
exports.watch = watchTask
