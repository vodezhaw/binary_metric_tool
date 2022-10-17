import React from "react";
import BinTable from "./BinTable";

function App() {
    return (
        <div className="App">
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark static-top">
                <div className="container">
                    <a className="navbar-brand centered" href="/">EMNLP 2022 - Binary Metric Demo</a>
                </div>
            </nav>
            <div className="container">
                <BinTable />
            </div>
        </div>
    );
}

export default App;
