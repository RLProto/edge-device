import { interfaceRoi } from "@/roi";
import { $, sendData, DEFAULT_URL } from "@/utils/utils";
import axios from 'axios';

const DOM_STATUS = $("#toast-status");
const DOM_STATUS_TEXT = $("#toast-status p");
const DOM_ACCURACY_TEXT = $("#accuracy-text");
const DOM_TIME_TEXT = $("#time-text")
const DOM_INPUT_MODEL = $("#input-file-model");
const DOM_BUTTON_UPLOAD_MODEL = $("#button-upload-model");
const DOM_STREAM_VIDEO = $("#stream-video");
const DOM_PAUSE_VIDEO = $("#pause-video");
const DOM_PREDICT = $("#predict");
const DOM_ENABLE_STREAM = $("#enable-webcam");
const DOM_LABEL_ADVANCED_PARAMETERS = $("#advanced-parameters-label");
const DOM_CONTAINER_ADVANCED_PARAMETERS = $("#advanced-parameters");
const DOM_INPUT_FILTER = $("#input-filter");
const DOM_INPUT_VIDEO_SOURCE = $("#input-video-source");

const DEFAULT_BLACK_IMAGE =  "./assets/black.png";

export let predict = false;
let stream;
let videoPlaying = false;
let socket;
let model_loaded = false

DOM_STREAM_VIDEO.src = DEFAULT_URL + "video";

checkStream()

function checkStream() {
  if (DOM_STREAM_VIDEO.src == DEFAULT_BLACK_IMAGE) {
    videoPlaying = false;
  } else {
    videoPlaying = true;
  }
}

async function checkFolderAndUpdateLabel() {
  try {
      const response = await axios.get(DEFAULT_URL+'check-model-loaded',{
        headers: {
        'Cache-Control': 'no-cache'
    }});
      const folderName = response.data.Arquivo;
      if (folderName) {
          DOM_BUTTON_UPLOAD_MODEL.textContent = folderName;
          model_loaded = true
          enablePredictButton()
      } else {
        DOM_BUTTON_UPLOAD_MODEL.textContent = "Carregar Modelo";
        model_loaded = false
      }
  } catch (error) {
      console.error('Error checking the folder:', error);
  }
}


DOM_ENABLE_STREAM.addEventListener("change", () => {
  if (videoPlaying) {
    DOM_PAUSE_VIDEO.classList.remove("pause-video-hidden");
    videoPlaying = false;
    if (predict) {
      predictionToggle();
    }
    DOM_PREDICT.disabled = true;
    DOM_STREAM_VIDEO.disabled = true;
    DOM_STREAM_VIDEO.src = DEFAULT_BLACK_IMAGE
    return;
  }

  DOM_PAUSE_VIDEO.classList.add("pause-video-hidden");
  videoPlaying = true;
  DOM_STREAM_VIDEO.disabled = false;
  DOM_STREAM_VIDEO.src = DEFAULT_URL + "video";
  if (model_loaded) {
    DOM_PREDICT.disabled = false;
  }
});

DOM_INPUT_VIDEO_SOURCE.addEventListener("change", () => {
  if (DOM_INPUT_VIDEO_SOURCE.value !== "") {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
    DOM_STREAM_VIDEO.srcObject = null;
    DOM_STREAM_VIDEO.src = DOM_INPUT_VIDEO_SOURCE.value;
    DOM_STREAM_VIDEO.type = "video/ogg";
    return;
  }
});

DOM_LABEL_ADVANCED_PARAMETERS.addEventListener("click", () => {
  DOM_CONTAINER_ADVANCED_PARAMETERS.classList.toggle("advanced-active");
  if (DOM_CONTAINER_ADVANCED_PARAMETERS.classList.contains("advanced-active")) {
    DOM_LABEL_ADVANCED_PARAMETERS.innerHTML = "▽";
  } else {
    DOM_LABEL_ADVANCED_PARAMETERS.innerHTML = "△";
  }
});

DOM_INPUT_FILTER.addEventListener("change", () => {
  const bufferSize = parseInt(DOM_INPUT_FILTER.value);
  const path = "filter";
  const headers = new Headers();
  const data = JSON.stringify({
    filter_value: bufferSize,
  });
  headers.append("Content-type", "application/json");
  try {
    sendData(path, headers, data);
  } catch (error) {
    alert(error);
  }
});

DOM_INPUT_MODEL.addEventListener("change", checkInputFieldsRight);

DOM_STREAM_VIDEO.addEventListener("pointerdown", interfaceRoi.startDrag);

async function checkInputFieldsRight() {
  if (!DOM_INPUT_MODEL.files.length) {
    DOM_PREDICT.disabled = true;
    model_loaded = false;
    return;
  }
  model_loaded = await sendModelToBack()
  enablePredictButton();
}

async function enablePredictButton() {
  if (model_loaded && videoPlaying)
    DOM_PREDICT.disabled = false;
  else
    DOM_PREDICT.disabled = true;
}

async function sendModelToBack(){
  const files = DOM_INPUT_MODEL.files;
  if (files.length > 0) {
    const file = files[0];

    DOM_BUTTON_UPLOAD_MODEL.textContent = file.name;

    try {
      const path = "upload-model";
      const headers = new Headers();
      const formData = new FormData();
      formData.append("file", file);
      const responseData = await sendData(path, headers, formData);
      if (responseData.detail) throw new Error(responseData.detail);
      setStatusText("Modelo treinado carregado com sucesso!", 4000);
      return true
    } catch (error) {
      unloadModel();
      alert(error.message);
      return false
    }
  }
}

DOM_PREDICT.addEventListener("click", () => {
  predictionToggle();
});

function unloadModel() {
  DOM_INPUT_MODEL.value = "";
  DOM_BUTTON_UPLOAD_MODEL.textContent = "Carregar Modelo";
  DOM_PREDICT.disabled = true;
}

function registerReloadWarning() {
  window.addEventListener("beforeunload", function (event) {
    event.preventDefault();
    event.returnValue = "";
  });
}

function predictionToggle() {
  if (!predict) {
    predict = true;
    DOM_PREDICT.textContent = "Parar predição!";
    DOM_BUTTON_UPLOAD_MODEL.disabled = true;
    DOM_ACCURACY_TEXT.hidden = false;
    DOM_TIME_TEXT.hidden = false
    startPrediction();
    return;
  }
  closeWebSocket();
  stopPrediction();
  predict = false;
  DOM_PREDICT.textContent = "Predizer!";
  DOM_BUTTON_UPLOAD_MODEL.disabled = false;
  DOM_ACCURACY_TEXT.hidden = true;
  DOM_TIME_TEXT.hidden = true
}

function statusTextTimeout(delay) {
  setTimeout(() => {
    DOM_STATUS.hidden = true;
  }, delay);
}

function setStatusText(text, delay = 200, color = "#248642") {
  DOM_STATUS.hidden = false;
  DOM_STATUS.style.backgroundColor = color;
  DOM_STATUS_TEXT.innerText = text;
  if (delay > 0) {
    statusTextTimeout(delay);
  }
}

function setPredictedClassLabel(classificationData){
  const predictedClass = classificationData["classification"]
  const predictedConfidence = classificationData["confidence-score"]
  DOM_ACCURACY_TEXT.innerHTML = `<strong>${predictedClass}</strong><br />${predictedConfidence}% confiança`
  DOM_TIME_TEXT.innerHTML = new Date().toLocaleString()
}

function blockChangeModel(){
  predict = true
  DOM_PREDICT.textContent = "Parar predição!";
  DOM_BUTTON_UPLOAD_MODEL.disabled = true;
  DOM_ACCURACY_TEXT.hidden = false;
  DOM_TIME_TEXT.hidden = false
  }

function openWebSocket() {
  if (!socket || socket.readyState === WebSocket.CLOSED) {
    socket = new WebSocket("ws"+ DEFAULT_URL.slice(4)+"predict");

    socket.onopen = function () {
      console.log("WebSocket Conectado");
    };

    socket.onmessage = function (event) {
       setPredictedClassLabel(JSON.parse(event.data))
       blockChangeModel()
    };

    socket.onerror = function (error) {
      console.error("WebSocket Erro:", error);
    };

    socket.onclose = function () {
      console.log("WebSocket Desconectado");
      setTimeout(openWebSocket, 1000);
    };
  }
}

function closeWebSocket() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }
}

async function startPrediction() {
  registerReloadWarning();
  const path = "continuous-inference"
  const headers = new Headers();
  const data = JSON.stringify({
    "status": "start",
  });
  headers.append("Content-type", "application/json");
  sendData(path,headers,data)
}

async function stopPrediction() {
  const path = "continuous-inference"
  const headers = new Headers();
  const data = JSON.stringify({
    "status": "stop",
  });
  headers.append("Content-type", "application/json");
  sendData(path,headers,data)
}

openWebSocket();
document.addEventListener("DOMContentLoaded", checkFolderAndUpdateLabel);