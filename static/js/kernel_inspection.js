var canvas = document.getElementById("input_canvas");
var context = canvas.getContext("2d");
var image_sample_size = 3
var img_path = "static/figures/articles/convolution/raccoon_resized.jpeg"
var hightlight_blue = 100
var img = new Image();
img.src = img_path;
var w = img.width / 2;
var h = img.height / 2;
var image_target_width = 120
var image_target_height = 80
var img_data = 0;
var kernel = [
  [-1, -1, -1],
  [-1, 4, -1],
  [-1, -1, -1],
];

// converts an RGBA image to an Grayscale image
function grayscaleImage(w, h) {
	var imageData = context.getImageData(0, 0, w, h);
  var data = imageData.data;

  for ( var i = 0, l = data.length; i < l; i += 4 ) {
  	var rgb = Math.round( ( data[ i ] + data[ i + 1 ] + data[ i + 2 ] ) / 3 );
      data[ i ]     = rgb;
      data[ i + 1 ] = rgb;
      data[ i + 2 ] = rgb;
      data[ i + 3 ] = 255;
  }
  context.putImageData( imageData, 0, 0 );
  return data
}

// draws a pixelated version of the original image
// the sample sample size param controles the resolution of the output image
function draw_img_pixelated(img_path, sample_size) {
  var img1 = new Image();
  img1.src = img_path;

  img1.onload = function () {
    w = image_target_width //img1.width / 2;
    h = image_target_height //img1.height / 2;

    context.drawImage(img1, 0, 0, w, h);
    pixelArr = grayscaleImage(w, h);
    img_data = pixelArr

    for (let y = 0; y < h; y += sample_size) {
      for (let x = 0; x < w; x += sample_size) {
        let p = (x + (y*w)) * 4;
        context.fillStyle = "rgb(" + pixelArr[p] + "," + pixelArr[p+1] + "," + pixelArr[p+2] + "," + pixelArr[p+3] + ")";
        context.fillRect(x, y, sample_size, sample_size);
      }
    }
  };
}

// This highlights a patch of an image
// given an inclusive pair of 2D coordinates defining the patch
// assuming x1 <= x2 and y1 <= y2
function highlightPatch(x1, y1, x2, y2) {
  context.drawImage(img, 0, 0, w, h);
  img_data = grayscaleImage(w, h);
  for (let y = 0; y < h; y += image_sample_size) {
    for (let x = 0; x < w; x += image_sample_size) {
      let p = (x + (y*w)) * 4;
      if (x > x1 && y > y1 && x <= x2 && y <= y2) {
        img_data[p+2] += hightlight_blue;
      }
      context.fillStyle = "rgb(" + img_data[p]
        + "," + img_data[p+1]
        + "," + img_data[p+2]
        + "," + img_data[p+3] + ")";
      context.fillRect(x, y, image_sample_size, image_sample_size);
    }
  }
}

// translates a default coordinate to the pixelated postion
function translate_to_patch_coor(xpos, ypos, patch_width, patch_height) {
  var mouse_offset = 10;
  var pixel_x1 = Math.floor((xpos / 2) - mouse_offset);
  var pixel_y1 = Math.floor((ypos / 2) - mouse_offset);
  var pixel_x2 = Math.floor((xpos / 2) - mouse_offset);
  var pixel_y2 = Math.floor((ypos / 2) - mouse_offset);

  if (patch_width > 0) {
    // pixel_x1 -= (patch_width / 2) * image_sample_size
    pixel_x1 -= patch_width * image_sample_size;
  }

  if (patch_height > 0) {
    // pixel_y1 -= (patch_height / 2) * image_sample_size
    pixel_y1 -= patch_height * image_sample_size;
  }

  return [pixel_x1, pixel_y1, pixel_x2, pixel_y2];
}

// Extractes the color values within the patch.
function getPatchColors(posx, posy, width, height) {
  pix = ctx.getImageData(posx, posy, width, height).data;

  // Loop over each pixel and invert the color.
  for (var i = 0, n = pix.length; i < n; i += 4) {
      pix[i  ] = 255 - pix[i  ]; // red
      pix[i+1] = 255 - pix[i+1]; // green
      pix[i+2] = 255 - pix[i+2]; // blue
      // i+3 is alpha (the fourth element)
      pix[i+2] -= hightlight_blue
  }
  return pix;
}

// draw patch
function drawPatch(coord) {
    var patch_x = coord[0];
    var patch_y = coord[1];

    var patch_width = coord[2] - coord[0];
    var patch_height = coord[3] - coord[1];

    var draw_pos_x = 20;
    var draw_pos_y = 100;

    var upsample_factor = 6;

    var conv_arr = new Array();

    for (let y = patch_y; y < coord[3]; y += image_sample_size) {
      draw_pos_x = 20;
      for (let x = patch_x; x < coord[2]; x += image_sample_size) {
        let p = (x + (y*w)) * 4;
        conv_arr.push(img_data[p]);
        context.fillStyle = "rgb(" + img_data[p] + "," + img_data[p+1]
          + "," + img_data[p+2] + "," + img_data[p+3] + ")";
        context.fillRect(
          draw_pos_x, draw_pos_y,
          image_sample_size * upsample_factor,
          image_sample_size * upsample_factor);
        context.fillStyle = "rgb(255, 255, 255, 255)";
        context.font = "8px Arial";
        context.fillText(img_data[p].toString(), draw_pos_x, draw_pos_y + patch_height);
        draw_pos_x += image_sample_size * upsample_factor;
      }
      draw_pos_y += image_sample_size * upsample_factor;
    }

    context.fillStyle = "rgb(0, 0, 0, 255)";
    context.font = "36px Arial";
    context.fillText('*', draw_pos_x + 15, draw_pos_y - 10);

    draw_pos_x = 120
    draw_pos_y = 100
    for (let y = 0; y < kernel.length; y += 1) {
      draw_pos_x = 120;
      for (let x = 0; x < kernel[0].length; x += 1) {
        conv_arr[x * y] = conv_arr[x * y] * kernel[y][x]
        context.fillStyle = "rgb(0,0,0,255)";
        context.strokeRect(
          draw_pos_x, draw_pos_y,
          image_sample_size * upsample_factor,
          image_sample_size * upsample_factor);
        context.font = "8px Arial";
        context.fillText(kernel[y][x].toString(), draw_pos_x, draw_pos_y + patch_height);
        draw_pos_x += image_sample_size * upsample_factor;
      }
      draw_pos_y += image_sample_size * upsample_factor;
    }

    context.fillStyle = "rgb(0, 0, 0, 255)";
    context.font = "36px Arial";
    context.fillText('=', draw_pos_x + 15, draw_pos_y - 10);

    // conv_arr = array.reduce(function(a, b){ return a + b; }, 0);
    // context.fillStyle = "rgb(" + conv_arr + "," + conv_arr
    //   + "," + conv_arr + "," + conv_arr + ")";
    // context.fillRect(
    //   draw_pos_x + 30, draw_pos_y,
    //   image_sample_size * upsample_factor,
    //   image_sample_size * upsample_factor);
    // context.fillStyle = "rgb(0, 0, 0, 255)";
    // context.font = "8px Arial";
    // context.fillText(conv_arr.toString(), draw_pos_x + 30, draw_pos_y);
}

// Returns the mouse position w.r.t. the canvas.
function getMousePosInCanvas(mouseEvent) {
  var xpos;
  var ypos;

  mouseEvent = mouseEvent || window.event;

  // var xpos = mouseEvent.pageX;
  // var ypos = mouseEvent.pageY;
  var xpos = mouseEvent.clientX;
  var ypos = mouseEvent.clientY;

  if (xpos === undefined) {
    xpos = mouseEvent.clientX
      + document.body.scrollLeft
      + document.documentElement.scrollLeft;
  }
  if (ypos === undefined) {
    ypos = mouseEvent.clientY
      + document.body.scrollTop
      + document.documentElement.scrollTop;
  }

  var rect = canvas.getBoundingClientRect();
  xpos -= rect.left;
  ypos -= rect.top;

  return [Math.round(xpos), Math.round(ypos)];
}

// convolution
function convolution(x, y) {
  // @todo this does not work for floor(1.5), thus a pixel is gone
  var patch_x1 = x - (Math.floor(kernel[0].length / 2)) * image_sample_size;
  var patch_y1 = y - (Math.floor(kernel.length / 2)) * image_sample_size;
  var patch_x2 = x + (Math.floor(kernel[0].length / 2)) * image_sample_size;
  var patch_y2 = y + (Math.floor(kernel.length / 2)) * image_sample_size;

  var conv_pixel_val = [0, 0, 0, 255];

  var pixel_idx_x = 0;
  var pixel_idx_y = 0;

  console.log(x + ", " + patch_y1 + ", " + patch_x2 + ", " + patch_y2);
  // console.log(patch_x1 + ", " + patch_y1 + ", " + patch_x2 + ", " + patch_y2);

  for (let y = patch_y1; y < patch_y2; y += image_sample_size) {
    pixel_idx_x = 0;
    for (let x = patch_x1; x < patch_x2; x += image_sample_size) {
      let p = (x + (y*w)) * 4;
      conv_pixel_val[0] += img_data[p] * kernel[pixel_idx_y][pixel_idx_x];
      conv_pixel_val[1] += img_data[p+1] * kernel[pixel_idx_y][pixel_idx_x];
      conv_pixel_val[2] += img_data[p+2] * kernel[pixel_idx_y][pixel_idx_x];
      pixel_idx_x += 1;
    }
    pixel_idx_y += 1;
  }
  return conv_pixel_val;
}

// draw the convolved image
function drawConvImg() {
  var conv_img_pos_x = 160;
  var conv_img_pos_y = 0;

  for (let y = image_sample_size; y < h - image_sample_size; y += image_sample_size) {
    for (let x = image_sample_size; x < w - image_sample_size; x += image_sample_size) {
      data = convolution(x, y)

      context.fillStyle = "rgb(" + data[0] + ","
        + data[1] + "," + data[2] + "," + data[3] + ")";
      context.fillRect(
        conv_img_pos_x + x,
        conv_img_pos_y + y,
        image_sample_size,
        image_sample_size);
    }
  }
}

// finds image coordiantes w.r.t. the current mouse pointer position
function findObjectCoords(mouseEvent)
{
  [xpos, ypos] = getMousePosInCanvas(mouseEvent)

  context.clearRect(0, 0, w, h);

  patch_pos = translate_to_patch_coor(xpos, ypos, kernel.length, kernel[0].length);
  highlightPatch(
    patch_pos[0], patch_pos[1],
    patch_pos[2], patch_pos[3]
  );
  drawPatch(patch_pos);
  drawConvImg();
  // document.getElementById("objectCoords").innerHTML =
  // patch_pos[0] + ", " + patch_pos[1] + ", " + patch_pos[2] + ", " + patch_pos[3];
}


draw_img_pixelated(img_path, image_sample_size);
document.getElementById("input_canvas").onmousemove = findObjectCoords;
