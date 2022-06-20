import React, { Component } from 'react';
import './App.css';

import Projects from '../Projects/Projects';

class App extends Component {
  	render (){
		return (
			<React.Fragment>
				<nav className="navbar navbar-expand-lg navbar-dark bg-dark">
					<div className="container-fluid">
						<a className="navbar-brand mb-0 h1" href="#">Sheriff Olaoye</a>
						<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
							<span className="navbar-toggler-icon"></span>
						</button>
						<div className="collapse navbar-collapse" id="navbarText">
							<ul className="navbar-nav me-auto mb-2 mb-lg-0">
								<li className="nav-item">
									<a className="nav-link active" aria-current="page" onClick={() => console.log("Projects")}>Projects</a>
								</li>
								<li className="nav-item">
									<a className="nav-link" onClick={() => console.log("About")}>About</a>
								</li>
							</ul>
						</div>
					</div>
				</nav>

				{/* <Projects /> */}
			</React.Fragment>
		);
    }
}

export default App;
