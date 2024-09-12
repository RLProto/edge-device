import { predict } from "@/main";
import { $, sendData } from "@/utils/utils";

function setStatusText(text, delay = 200, color = ["#ffffff", "#248642"]) {
  DOM_TOAST_STATUS.hidden = false;
  DOM_TOAST_STATUS.style.color = color[0];
  DOM_TOAST_STATUS.style.backgroundColor = color[1];
  DOM_TOAST_STATUS_TEXT.innerText = text;
  if (delay > 0) {
    statusTextTimeout(delay);
  }
}

function statusTextTimeout(delay) {
  setTimeout(() => {
    DOM_TOAST_STATUS.hidden = true;
  }, delay);
}

function saveRect() {
  const path = "crop";
  var headers = new Headers();
  headers.append("Content-type", "application/json");
  const data = JSON.stringify(
    marqueeRect,
  );
  try {
    sendData(path, headers, data);
  } catch (error) {
    alert(error);
  }
}

// DOM
const DOM_TOAST_STATUS = $("#toast-status");
const DOM_TOAST_STATUS_TEXT = $("#toast-status p");

const DOM_STREAM_VIDEO = $("#stream-video");
const DOM_MARQUEE = $("#marquee");
const DOM_SVG_LINE_MARQUEE_PREPARATION = $("#svg-line-marquee-preparation");
const DOM_TEXT_VIDEO_DIMENSIONS = $("#text-video-dimensions");

// Variables
let cropDefinition = "";
let disabledMarquee = false;

let startX = 0;
let startY = 0;

let marqueeRect = {
  x: 0,
  y: 0,
  width: 400,
  height: 400,
};

// Getters
function getProcessMask() {
  return DOM_STREAM_VIDEO;
}

function getDisabledMarquee() {
  return disabledMarquee;
}

function getMarqueeRect() {
  return marqueeRect;
}

function getCropDefinition() {
  return cropDefinition;
}

// Setters
function setCropDefinition() {
  if (disabledMarquee) return;

  cropDefinition = `x=${marqueeRect.x}, y=${marqueeRect.y}, largura=${marqueeRect.width}, altura=${marqueeRect.height}`;
  renderVideoCropDefinition();
}

function fixFullFrameCropDefinition() {
  const sizeFactor = DOM_STREAM_VIDEO.videoHeight / DOM_STREAM_VIDEO.height;

  cropDefinition = `
   x=${parseInt(marqueeRect.x * sizeFactor)}, 
   y=${parseInt(marqueeRect.y * sizeFactor)}, 
   largura=${parseInt(marqueeRect.width * sizeFactor)}, 
   altura=${parseInt(marqueeRect.height * sizeFactor)} 
   `;

  if (marqueeRect.width == 400) {
    cropDefinition = `
     x=${parseInt(marqueeRect.x * sizeFactor)}, 
     y=${parseInt(marqueeRect.y * sizeFactor)}, 
     largura=${DOM_STREAM_VIDEO.videoHeight}, 
     altura=${DOM_STREAM_VIDEO.videoHeight}
     `;
  }

  renderVideoCropDefinition();
}

function setDisabledMarquee(flag) {
  disabledMarquee = flag;
}

// Functions
function renderVideoCropDefinition() {
  DOM_TEXT_VIDEO_DIMENSIONS.innerHTML = cropDefinition;
}

function resetCropWhenSmallSelection(isSmallSelection) {
  marqueeRect = {
    x: 0,
    y: 0,
    width: 400,
    height: 400,
  };

  changeMarqueeStyle("white", "5, 5");

  if (isSmallSelection) {
    setStatusText(
      "Seleção muito pequena, tente fazer um pouco maior.",
      4000,
      "#ff0000"
    );
  }
}

function changeMarqueeStyle(color, dash) {
  DOM_SVG_LINE_MARQUEE_PREPARATION.style.setProperty("stroke", color);
  DOM_SVG_LINE_MARQUEE_PREPARATION.style.setProperty("stroke-dasharray", dash);
}

function checkMarqueeSize() {
  changeMarqueeStyle("white", "5, 5");

  if (marqueeRect.width < 50) {
    changeMarqueeStyle("red", "0");
  }

  if (marqueeRect.height < 50) {
    changeMarqueeStyle("red", "0");
  }
}

function drawRect(rect, data) {
  const { x, y, width, height } = data;
  rect.setAttributeNS(null, "width", width);
  rect.setAttributeNS(null, "height", height);
  rect.setAttributeNS(null, "x", x);
  rect.setAttributeNS(null, "y", y);

  return rect;
}

// Mouse Events Functions
function startDrag(e) {
  if (disabledMarquee) return;
  if (DOM_STREAM_VIDEO.disabled) return;
  if (predict) return;
  window.addEventListener("pointerup", stopDrag);
  DOM_STREAM_VIDEO.addEventListener("pointermove", moveDrag);
  DOM_MARQUEE.classList.remove("hide");
  DOM_SVG_LINE_MARQUEE_PREPARATION.classList.remove("hide");

  startX = e.offsetX;
  startY = e.offsetY;
  const width = 0;
  const height = 0;

  Object.assign(marqueeRect, {
    startX,
    startY,
    width,
    height,
  });

  drawRect(DOM_MARQUEE, marqueeRect);
  drawRect(DOM_SVG_LINE_MARQUEE_PREPARATION, marqueeRect);
}

function stopDrag(e) {
  window.removeEventListener("pointerup", stopDrag);
  DOM_STREAM_VIDEO.removeEventListener("pointermove", moveDrag);

  if (marqueeRect.width <= 10) {
    resetCropWhenSmallSelection();
  } else if (marqueeRect.width < 50) {
    resetCropWhenSmallSelection(true);
  }

  if (marqueeRect.height <= 10) {
    resetCropWhenSmallSelection();
  } else if (marqueeRect.height < 50) {
    resetCropWhenSmallSelection(true);
  }

  drawRect(DOM_MARQUEE, marqueeRect);
  drawRect(DOM_SVG_LINE_MARQUEE_PREPARATION, marqueeRect);

  if (
    e.target === DOM_STREAM_VIDEO &&
    marqueeRect.width &&
    marqueeRect.height
  ) {
    fixFullFrameCropDefinition();
  }
  setCropDefinition();
  saveRect();
}

function moveDrag(ev) {
  let x = 0;
  let y = 0;
  let endX = ev.offsetX;
  let endY = ev.offsetY;
  let quadrant = 4;

  const maxY = DOM_STREAM_VIDEO.height - startY;
  let width = startX - endX;
  let height = startY - endY;
  let side = width;

  if (width < 0) {
    side *= -1;
    quadrant = 3;
  }

  if (height < 0) {
    if (quadrant === 3) {
      quadrant = 2;
    } else {
      quadrant = 1;
    }
  }

  if (quadrant < 3) {
    side = Math.min(side, maxY);
  } else {
    side = Math.min(side, startY);
  }

  switch (quadrant) {
    case 1:
      x = endX;
      y = startY;
      width = side;
      height = side;
      break;
    case 2:
      x = startX;
      y = startY;
      width = side;
      height = side;
      break;
    case 3:
      x = startX;
      y = startY - side;
      width = side;
      height = side;
      break;
    case 4:
      x = startX - side;
      y = startY - side;
      width = side;
      height = side;
      break;

    default:
      break;
  }

  checkMarqueeSize();

  x=x.toFixed(2)
  y=y.toFixed(2)
  width=width.toFixed(2)
  height=height.toFixed(2)
  Object.assign(marqueeRect, {
    x,
    y,
    width,
    height,
  });

  drawRect(DOM_MARQUEE, marqueeRect);
  drawRect(DOM_SVG_LINE_MARQUEE_PREPARATION, marqueeRect);
  fixFullFrameCropDefinition();
}
// Export
export const interfaceRoi = {
  getProcessMask,
  getDisabledMarquee,
  setDisabledMarquee,
  getMarqueeRect,
  getCropDefinition,
  setCropDefinition,
  startDrag,
};
