import axios from "axios";
import {config} from "process";

const GENERATE_IMAGE = '/api/generate_image';
const GENERATE_IMAGES = '/api/generate_images';
const UPSCALE_IMAGE = '/api/upscale_image';
const SESSION_ID = '/api/new_session';
const UPGRADE_PROMPT = '/api/upgrade_propmt';
const GET_TRANSCRIPTION = '/api/get_transcription';


export default class ApiClient {

    drawImage(_data) {
        return axios.post(GENERATE_IMAGE, _data, config={responseType: 'blob'});
    }

    drawImages(_data) {
        return axios.post(GENERATE_IMAGES, _data, config={responseType: 'blob'});
    }

    upscaleImage(_data) {
        return axios.post(UPSCALE_IMAGE, _data, config={responseType: 'blob'});
    }

    upgradePropmpt(_data) {
        return axios.post(UPGRADE_PROMPT, _data);
    }

    getTranscript(_data) {
        return axios.post(GET_TRANSCRIPTION, _data);
    }

    get_session() {
        return axios.get(SESSION_ID);
    }
}