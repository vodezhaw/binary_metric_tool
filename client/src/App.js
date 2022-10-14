import React, {useState, useEffect} from "react";

function App() {

    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/api/members").then(
            res => res.json()
        ).then(
            data => {setData(data)}
        )
    }, [])

    return (
        <div className="App">
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark static-top">
                <div className="container">
                    <a className="navbar-brand centered" href="/">EMNLP 2022 - Binary Metric Demo</a>
                </div>
            </nav>
            <div className="container">
                {(typeof data.members === "undefined") ? (<p>Loading .... </p>) : (
                    data.members.map((member, i) => (
                        <p key={i}>{member}</p>
                    ))
                )}
            </div>
        </div>
    );
}

export default App;
