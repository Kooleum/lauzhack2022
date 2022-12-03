const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
const msg_erreur = document.getElementById("msg_erreur");
const msg_status = document.getElementById("msg_status");

const pose_landmaks_to_get = [0, 11, 12, 13, 14, 15, 16, 24, 23];

const pose_landmarks_to_keep = [13, 14, 16, 15, 0];

const take_photo = false;

let total_data = [];
let savedPoints = [];

let ellapsed_time, total_time = 0;
let start, end = 0;
let record = false;


function getLimits(points){
    let top_left = [1, 1];
    let bottom_right = [0, 0];
    for(let i = 0; i < points.length; i++){
        if(points[i][0] < top_left[0]){
            top_left[0] = points[i][0];
        }
        if(points[i][1] < top_left[1]){
            top_left[1] = points[i][1];
        }
        if(points[i][0] > bottom_right[0]){
            bottom_right[0] = points[i][0];
        }
        if(points[i][1] > bottom_right[1]){
            bottom_right[1] = points[i][1];
        }
    }
    return [top_left, bottom_right];

}

function normalizeXY(points){
    nomrPoints = [];

    let limits = getLimits(points);

    let top_left = limits[0];
    let bottom_right = limits[1];

    for(let i = 0; i < points.length; i++){
        normPoint = [];
        normPoint.push((points[i][0] - top_left[0]) / (bottom_right[0] - top_left[0]));
        normPoint.push((points[i][1] - top_left[1]) / (bottom_right[1] - top_left[1]));
        normPoint.push(points[i][2]);   
        nomrPoints.push(normPoint);
    }

    return nomrPoints;
}

function onResults(results) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
//   canvasCtx.drawImage(results.segmentationMask, 0, 0,
//                       canvasElement.width, canvasElement.height);

  // Only overwrite existing pixels.
    canvasCtx.globalCompositeOperation = 'source-in';
    canvasCtx.fillStyle = '#000000';
    canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

    // Only overwrite missing pixels.
    canvasCtx.globalCompositeOperation = 'destination-atop';
    canvasCtx.drawImage(
        results.image, 0, 0, canvasElement.width, canvasElement.height);

    canvasCtx.globalCompositeOperation = 'source-over';
    // drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,
    //                 {color: '#00FF00', lineWidth: 4});
    // drawLandmarks(canvasCtx, results.poseLandmarks,
    //                 {color: '#FF0000', lineWidth: 2});
    // drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS,
    //                 {color: '#CC0000', lineWidth: 5});
    // drawLandmarks(canvasCtx, results.leftHandLandmarks,
    //                 {color: '#00FF00', lineWidth: 2});
    // drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS,
    //                 {color: '#00CC00', lineWidth: 5});
    // drawLandmarks(canvasCtx, results.rightHandLandmarks,
    //                 {color: '#FF0000', lineWidth: 2});

    // console.log(results.poseLandmarks);


    if (results.poseLandmarks == null || results.rightHandLandmarks == null || results.leftHandLandmarks == null) {
        msg_erreur.innerHTML = "Veuillez vous placer devant la caméra";
        msg_erreur.hidden = false;
        return;
    }
    
    //Getting the values for upbody
    let values_landmark = [];
    let values_landmark_to_norm = [];
    for(let i = 0; i < pose_landmaks_to_get.length; i++){
        let visibility_landmark = results.poseLandmarks[pose_landmaks_to_get[i]].visibility;
        let x_landmark = results.poseLandmarks[pose_landmaks_to_get[i]].x;
        let y_landmark = results.poseLandmarks[pose_landmaks_to_get[i]].y;
        let z_landmark = results.poseLandmarks[pose_landmaks_to_get[i]].z;
        
        if (visibility_landmark > 0.5) {
            values_landmark.push([x_landmark, y_landmark, z_landmark]);
        }

        for (let j = 0; j < pose_landmarks_to_keep.length; j++) {
            if (pose_landmaks_to_get[i] == pose_landmarks_to_keep[j]) {
                values_landmark_to_norm.push([x_landmark, y_landmark, z_landmark]);
            }
        }
    }

    if (values_landmark.length < pose_landmaks_to_get.length) {
        msg_erreur.innerHTML = "Veuillez vous placer devant la caméra";
        msg_erreur.hidden = false;
        return;
    }

    let norm_values_landmark = normalizeXY(values_landmark_to_norm);
    // console.log(results.rightHandLandmarks);

    
    let rightHandLandmarks = [];
    if (results.rightHandLandmarks != null) {
        for(let i = 0; i < results.rightHandLandmarks.length; i++){

            let x_landmark = results.rightHandLandmarks[i].x;
            let y_landmark = results.rightHandLandmarks[i].y;
            let z_landmark = results.rightHandLandmarks[i].z;
            
            rightHandLandmarks.push([x_landmark, y_landmark, z_landmark]);
        }
    }
    
    let normalized_rightHandLandmarks = normalizeXY(rightHandLandmarks);

    let leftHandLandmarks = [];

    if (results.leftHandLandmarks != null) {
        for(let i = 0; i < results.leftHandLandmarks.length; i++){

            let x_landmark = results.leftHandLandmarks[i].x;
            let y_landmark = results.leftHandLandmarks[i].y;
            let z_landmark = results.leftHandLandmarks[i].z;
    
            leftHandLandmarks.push([x_landmark, y_landmark, z_landmark]);
        }
    }

    let normalized_leftHandLandmarks = normalizeXY(leftHandLandmarks);

    total_data = [];
    
    normalized_rightHandLandmarks.forEach((landmark) => {
        total_data.push(landmark);
    });
    normalized_leftHandLandmarks.forEach((landmark) => {
        total_data.push(landmark);
    });
    norm_values_landmark.forEach((landmark) => {
        total_data.push(landmark);
    });
    values_landmark_to_norm.forEach((landmark) => {
        total_data.push(landmark);
    });
    
    if (total_data.length < 52) {
        return;
    }
    
    msg_erreur.hidden = true;
    handle_timer();
    canvasCtx.restore();
}

const holistic = new Holistic({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
}});

holistic.setOptions({
  modelComplexity: 1,
  smoothLandmarks: false,
  enableSegmentation: true,
  smoothSegmentation: true,
  refineFaceLandmarks: false,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});

holistic.onResults(onResults);

const camera = new Camera(videoElement, {
  onFrame: async () => {
    await holistic.send({image: videoElement});
  },
  width: 720,
  height: 480
});
camera.start();



function handle_timer(){
    if(record == true){

        end = new Date();
        let time = end - start;
        ellapsed_time += time - ellapsed_time;

        if(ellapsed_time >= 10){
            savedPoints.push(total_data);
        }
        if(savedPoints.length >= 30){
            record = false;
            console.log("stop");
            console.log(savedPoints);
        }
    }
}

document.getElementById("btn_record").addEventListener("click", function(){
    console.log("record");
    record = true;
    savedPoints = [];
    ellapsed_time = 0;
    start = Date.now();
});