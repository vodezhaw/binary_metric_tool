import axios from "axios";
import {config} from "process";

const GET_HEADERS = '/api/get_headers';
const GET_TABLE = '/api/get_table_for_header_values';
const GET_SINGLE_VALUE = '/api/compute_single_value';
const GET_PLOT = '/api/get_plot_for_table';
const SESSION_ID = '/api/new_session';
const UPGRADE_PROMPT = '/api/upgrade_propmt';
const GET_TRANSCRIPTION = '/api/get_transcription';


export default class ApiClient {
    getHeaders() {
        return axios.get(GET_HEADERS);
    }

    get_table_for_header_values(data) {
        return axios.get(GET_TABLE, {params: data});
    }

    get_single_value_header_values(data) {
        return axios.get(GET_SINGLE_VALUE, {params: data});
    }
    get_plot(data) {
        return axios.post(GET_PLOT, data, config={responseType: 'blob'});
    }
}