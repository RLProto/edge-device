const tf = require("@tensorflow/tfjs");
const tfn = require("@tensorflow/tfjs-node");
const fs = require("fs");
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 7987, typeof: "blob" });
require('dotenv').config();

const MOBILE_NET_INPUT_WIDTH = 224;
const MOBILE_NET_INPUT_HEIGHT = 224;
const DEFAULT_PATH = process.env.MODEL_PATH

let customModel = null;
let featureExtractor = null;
let parameters = null;
let modelJson = null;

wss.on("connection", function connection(ws) {
  loadLocalModel();
  ws.on("message", async function incoming(message) {
    try {
      const messageString = message.toString("utf8");
      const imageBuffer = Buffer.from(messageString, "base64");
      const image = tfn.node.decodeImage(imageBuffer, 3);

      const predictionResult = await predictImage(image);

      ws.send(JSON.stringify(predictionResult));

      tf.dispose(image);
    } catch (error) {
      console.error("Error processing image:", error);
      ws.send(JSON.stringify({ error: "Error processing image" }));
    }
  });
});

loadMobileNetFeatureModel();

async function loadMobileNetFeatureModel() {
  // Caminho do diretório onde o modelo MobileNet está localizado
  const mobileNetPath = "graph_model/mobilenet/model.json";
  const handler = tfn.io.fileSystem(mobileNetPath);
  featureExtractor = await tf.loadGraphModel(handler);
  console.log("MobileNet Feature Model carregado com sucesso!");

  tf.tidy(function () {
    let answer = featureExtractor.predict(
      tf.zeros([1, MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH, 3])
    );
    console.log(answer.shape);
  });
}

async function loadLocalModel() {
  const modelJsonPath = DEFAULT_PATH + "model.json";
  const weightsPath = DEFAULT_PATH + "model.weights.bin";
  const parametersPath = DEFAULT_PATH + "parameters.json";
  let modelWeightsBuffer = null;
  try {
    modelJson = JSON.parse(fs.readFileSync(modelJsonPath).toString());
    parameters = JSON.parse(fs.readFileSync(parametersPath).toString());
    modelWeightsBuffer = fs.readFileSync(weightsPath);

    console.log("Modelo carregado com sucesso!");

    customModel = await tf.models.modelFromJSON(modelJson);

    const weightSpecs = modelJson.weightSpecs;
    const weightData = new Uint8Array(modelWeightsBuffer);
    const tensors = tf.io.decodeWeights(weightData, weightSpecs);
    customModel.setWeights(Object.values(tensors));
  } catch (error) {
    console.error("Erro ao carregar o modelo:", error);
  }
}

function calculateFeaturesOnCurrentFrame(image) {
  return tf.tidy(function () {
    // const videoFrameAsTensor = tf.browser.fromPixels(image);
    const resizedTensorFrame = tf.image.resizeBilinear(
      image,
      [MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH],
      true
    );

    const normalizedTensorFrame = resizedTensorFrame.div(255);

    return featureExtractor
      .predict(normalizedTensorFrame.expandDims())
      .squeeze();
  });
}

async function predictImage(rawImage) {
  if (!customModel || !featureExtractor) return;
  return tf.tidy(() => {
    const imageFeatures = calculateFeaturesOnCurrentFrame(rawImage);
    const prediction = customModel
      .predict(imageFeatures.expandDims())
      .squeeze();
    const highestIndex = prediction.argMax().arraySync();
    const predictionArray = prediction.arraySync();

    const predictedClass = parameters.classNames[highestIndex];
    const predictedConfidence = Math.floor(predictionArray[highestIndex] * 100);
    return {
      classification: predictedClass,
      "confidence-score": predictedConfidence,
    };
  });
}
