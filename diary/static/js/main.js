// Use with bindScroll for infinite scroll
function loadMore(continuation_token) {
  if (continuation_token == null || continuation_token.length == 0) 
    return;

  $('.loading-shield').show();
  $.ajax({
    url: 'list-diaries?before=' + encodeURIComponent(continuation_token) + '&max=12',
    type: 'GET',
    success: function(data){ 
      $('.loading-shield').hide();
      $(window).bind('scroll', bindScroll(data.token));
      var $newCards = $(data.html);
      $("#cardlist").append($newCards).masonry('appended', $newCards);
    },
    error: function(data) {
      $('.loading-shield').hide();
      $(window).bind('scroll', bindScroll(data.token));
      alert("Status: " + data.status + "\nError: " + data.statusText);
    }
  });
}

// Bind scroll with this method to initiate infinite scroll
function bindScroll(continuation_token) {
  function bindMethod() {
      if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
          $(window).unbind('scroll');
          loadMore(continuation_token);
      }
  }
  return bindMethod
}

// localStorage names
const DIARYSTATS_NAME = 'diarystats';
const DARKMODE_NAME = 'darkmode';
const WALLPAPER_NAME = 'wallpaper';

// Load diary statistics
function loadDiaryStats(stats) {
  if (stats != null && stats.length > 0) {
    localStorage.setItem(DIARYSTATS_NAME, stats);
  }
  
  $('#diarystats').html(localStorage.getItem(DIARYSTATS_NAME));
}

// Handle dark mode
function applyDarkMode() {
  if (localStorage.getItem(DARKMODE_NAME) == 1) {
    $('body').attr('data-bs-theme', 'dark');
    $('#navbarContainer').css('background-color', '#212529');
  }
  else {
    $('body').attr('data-bs-theme', 'light');
    $('#navbarContainer').css('background-color', '#563d7c');
  }
  applyWallpaper();
}

// Handle wallpaper
let SupportedWallpapers = ['celebration', 'food', 'grocery', 'music', 'notes', 'places', 'recipe', 'travel', 'video'];

function applyWallpaper() {
  let currentWallpaper = localStorage.getItem(WALLPAPER_NAME);
  if (SupportedWallpapers.includes(currentWallpaper)) {
    let imageMode = localStorage.getItem(DARKMODE_NAME) == 1 ? 'dark' : 'light';
    $('.image-wallpaper').css('background-image', 'url(\"/static/img/' + currentWallpaper + '_' + imageMode + '.svg\")');
    $('#backgroundImageDropdownButton').html('Wallpaper: ' + currentWallpaper.charAt(0).toUpperCase() + currentWallpaper.slice(1));
  }
  else { // No wallpaper
    $('.image-wallpaper').css('background-image', 'none');
    $('#backgroundImageDropdownButton').html('Wallpaper: None');
  }
}

function setWallpaper(wallpaper) {
  if (SupportedWallpapers.includes(wallpaper) || wallpaper == 'none') {
    localStorage.setItem(WALLPAPER_NAME, wallpaper);
    applyWallpaper();
    populateWallpaperSelection();
  }
}

function populateWallpaperSelection() {
  let parentElement = $('#backgroundImageDropdownMenu');
  let currentWallpaper = localStorage.getItem(WALLPAPER_NAME);
  parentElement.empty();
  SupportedWallpapers.forEach(wp => {
    let linkClasses = 'dropdown-item btn image-menu border-bottom';
    if (wp == currentWallpaper) {
      linkClasses += ' active';
    }
    parentElement.append('<li><a class="' + linkClasses + '" href="#" onclick="setWallpaper(\'' + wp + '\')">' + wp.charAt(0).toUpperCase() + wp.slice(1) + '</a></li>');
  });
}

// Show diary details
function showDetails(diaryId) {
  $('.loading-shield').show();
  $.ajax({
    url: 'get-diary?id=' + encodeURIComponent(diaryId),
    type: 'GET',
    success: function(data){ 
      $('.loading-shield').hide();
      $('#diaryModal').html(data);
      $('#diaryModal').modal('show');
    },
    error: function(data) {
      $('.loading-shield').hide();
      alert("Status: " + data.status + "\nError: " + data.statusText);
    }
  });
}

// Initialize dark mode and wallpaper
$(document).ready(function() {
  $('#darkModeSwitch').prop('checked', localStorage.getItem(DARKMODE_NAME) == 1);
  applyDarkMode();

  $('#darkModeSwitch').change(function() {
    localStorage.setItem(DARKMODE_NAME,  this.checked ? 1 : 0);
    applyDarkMode();
  });

  populateWallpaperSelection();
});

// Path: diary/static/js/main.js