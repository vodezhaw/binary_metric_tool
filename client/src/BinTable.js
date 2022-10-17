import React, {Component} from 'react';
import ApiClient from "./api_client";
import {format} from 'react-string-format';

export default class BinTable extends Component {

    constructor(props) {
        super(props);
        this.state = {
            header_data: undefined,
            selected_data: [],
            input_values: [],
            wrong_n_var_alert: false,
            wrong_axis: false,
            table_data: undefined,
            is_computing_value: false,
            col_name: undefined,
            row_name: undefined,
            x_axis: "",
            plot_img: undefined,
            single_value: undefined
        }

        this.handleChange = this.handleChange.bind(this);
        this.handle_input_change = this.handle_input_change.bind(this);
        this.handleAxisChange = this.handleAxisChange.bind(this);

    }

    componentDidMount() {
        const apiClient = new ApiClient();
        apiClient.getHeaders().then(res => {
            let dictionary = Object.assign({}, ...res.data.header_data.map((x) => ({[x.header_name]: -1})));
            let val_dictionary = Object.assign({}, ...res.data.header_data.map((x) => ({[x.header_name]: 0})));
            this.setState({header_data: res.data.header_data, selected_data: dictionary, input_values: val_dictionary})
        }).catch((err) => {
            console.log(err)
        })
    }

    handleChange(event) {
        console.log('value is:', event.target.value, event.target.id, event.target.selectedOptions[0].value);
        var selected_data = this.state.selected_data;
        selected_data[event.target.id] = Number.parseInt(event.target.value)
        this.setState({selected_data: selected_data})
        console.log(selected_data[event.target.id])
    }

    handle_input_change(event) {
        var input_values = this.state.input_values;
        input_values[event.target.id] = Number.parseInt(event.target.value)
        this.setState({input_values: input_values})
    }

    handleAxisChange(event) {
        console.log(event.target.value)
        this.setState({x_axis: event.target.value})
    }

    get_table() {
        const apiClient = new ApiClient();
        const selected_data = this.state.selected_data;
        var filtered = Object.keys(selected_data).reduce(function (filtered, key) {
            if (selected_data[key] < 0) filtered[key] = selected_data[key];
            return filtered;
        }, {});
        if (Object.keys(filtered).length !== 2) {
            this.setState({wrong_n_var_alert: true})
        } else {
            this.setState({wrong_n_var_alert: false})
            apiClient.get_table_for_header_values({data: this.state.selected_data}).then((res) => {
                this.setState({
                    table_data: res.data,
                    x_axis: "",
                    plot_img: undefined,
                    col_name: res.data.table.col_name,
                    row_name: res.data.table.row_name
                })
            })
        }
    }

    get_single_value() {
        const apiClient = new ApiClient();
        console.log(this.state.input_values)
        this.setState({is_computing_value: true})
        apiClient.get_single_value_header_values({data: this.state.input_values}).then((res) => {
            console.log(res.data.value)
            this.setState({single_value: res.data.value, is_computing_value: false})
        })
    }

    get_plot() {
        const apiClient = new ApiClient();
        if (this.state.x_axis === "") {
            this.setState({wrong_axis: true})
        } else {
            this.setState({wrong_axis: false})
            var send_data = {
                table_data: this.state.table_data,
                x_axis: this.state.x_axis
            }
            apiClient.get_plot(send_data).then(res => {
                this.setState({plot_img: URL.createObjectURL(res.data)})
            })
        }

    }

    render_headers() {
        var header_render = undefined;
        if (this.state.header_data === undefined) {
            header_render = <p>Loading Header..</p>
        } else {
            header_render = this.state.header_data.map((header_entry, val_list) =>
                <div className="col-2">
                    <label htmlFor={format('sel_{0}', val_list)}
                           className="form-label col-12">{header_entry.header_name}</label>
                    <select
                        className="form-select col-12"
                        id={header_entry.header_name}
                        onChange={this.handleChange}
                    >
                        <option value={-1}>Variable</option>
                        {header_entry.header_values.map((val, idx) => (
                            <option
                                value={idx}
                                key={format('opt_{0}_{1}', idx, val_list)}
                            >
                                {Number.isInteger(val) ? val : val.toFixed(2)}
                            </option>
                        ))}
                    </select>
                </div>
            )
        }
        return header_render
    }

    render_input_header() {
        var header_render = undefined;
        if (this.state.header_data === undefined) {
            header_render = <p>Loading Header..</p>
        } else {
            header_render = this.state.header_data.map((header_entry, val_list) =>
                <div className="col-2">
                    <label htmlFor={format('sel_{0}', val_list)}
                           className="form-label col-12">{header_entry.header_name}</label>
                    <input
                        className="form-select col-12"
                        type="number"
                        min={0}
                        onChange={this.handle_input_change}
                        defaultValue={this.state.input_values[header_entry.header_name]}
                        id={header_entry.header_name}/>
                </div>
            )
        }
        return header_render
    }

    render_table() {
        var table = undefined
        if (this.state.table_data === undefined) {
            table = <p>No Table Yet</p>
        } else {
            let col_name = this.state.table_data.table.col_name;
            let row_name = this.state.table_data.table.row_name;
            const col_names = this.state.table_data.table.col_values.map((entry, idx) => (<th>{entry}</th>))

            const table_rows = <tbody>
            {this.state.table_data.table.row_values.map((entry, idx) => (
                <tr>
                    <tr>{entry.toFixed(2)}</tr>
                    {this.state.table_data.table.data[idx].map((eps, idx) => (
                        <td>{eps[1].toFixed(4)}</td>
                    ))}
                </tr>
            ))
            }
            </tbody>

            table = <table className="table">
                <thead>
                <tr>
                    <th>{format('{0}/{1}', row_name, col_name)}</th>
                    {col_names}
                </tr>
                </thead>
                {table_rows}
            </table>
        }
        return table
    }

    render_single_value() {
        var value = "Computing..."
        if (!this.state.is_computing_value) {
            if (this.state.single_value === undefined) {
                value = <p>No Value Computed...</p>
            } else {
                value = <p>{this.state.single_value.toFixed(4)}</p>
            }
        }

        return value
    }


    render_plot() {
        var plot = undefined
        if (this.state.table_data === undefined) {
            plot = <p>No Plot</p>
        } else {
            var image = <p>No Plot Yet..</p>;
            if (!(this.state.plot_img === undefined)) {
                image = <img
                    src={this.state.plot_img}
                    alt="logo"
                    className="border border-secondary img-fluid"
                />
            }

            plot =
                <div className='col-12'>
                    <div className='row'>
                        <div className="col-12 alert alert-danger" hidden={!this.state.wrong_axis}>
                            Please Select Axis
                        </div>
                    </div>
                    <div className='row'>
                        <select
                            className="form-control col-6"
                            onChange={this.handleAxisChange}
                            value={this.state.x_axis}
                        >
                            <option>Select X-Axis</option>
                            <option>{this.state.col_name}</option>
                            <option>{this.state.row_name}</option>
                        </select>
                        <button type="button"
                                className="btn btn-secondary col-2"
                                onClick={() => this.get_plot()}>
                            Plot
                        </button>
                    </div>

                    <div className='row'>
                        {image}
                    </div>
                </div>
        }
        return plot
    }

    render() {
        var header_render = this.render_headers();
        var table = this.render_table();
        var header_input_render = this.render_input_header();
        var single_value = this.render_single_value();
        var plot = this.render_plot();

        return (
            <div className="container">
                <div className='card mb-2'>
                    <div className="row">
                        <div className="col-12 alert alert-danger" hidden={!this.state.wrong_n_var_alert}>
                            Wrong Number of Varialbe, Choose exatly 2
                        </div>
                    </div>
                    <div className="row">
                        {header_render}
                    </div>
                    <div className='card'>
                        {table}
                    </div>
                    <div className="row">
                        <div className="col-12">
                            <button
                                type="button"
                                className="btn btn-secondary col-12"
                                onClick={() => this.get_table()}
                            >Render Table
                            </button>
                        </div>
                    </div>
                    <div className='card'>
                        {plot}
                    </div>

                </div>

                <div className='card mb-2'>
                    <div className="row">
                        {header_input_render}
                    </div>
                    <div className='card'>
                        {single_value}
                    </div>
                    <div className="row">
                        <div className="col-12">
                            <button
                                type="button"
                                className="btn btn-secondary col-12"
                                onClick={() => this.get_single_value()}
                            >Compute Single Value
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}