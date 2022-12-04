import React, { useEffect, useState } from "react";
import { app } from "@microsoft/teams-js";
import MediaQuery from 'react-responsive';
// import socketIOClient from "socket.io-client";
// import io from 'socket.io-client';
import './App.css';

class Tab extends React.Component {
  

  constructor(props) {
    super(props)
    this.state = {
      context: {},
      msg: this.props.msg,
      firstTime: true,
      // socket : io("http://127.0.0.1:5000", {
      //   autoConnect: false,
      //   transports: ['websocket']
      // }),

    }

  }


  appendMessage(message) {
    this.setState({ msg: this.state.msg.concat([message]) })
  }

  //React lifecycle method that gets called once a component has finished mounting
  //Learn more: https://reactjs.org/docs/react-component.html#componentdidmount
  componentDidMount() {
    app.initialize().then(() => {

      // Get the user context from Teams and set it in the state
      app.getContext().then(async (context) => {
        this.setState({
          meetingId: context.meeting.id,
          userName: context.user.userPrincipalName,
          // msg: ["Hello World", "assadwe"]
        });
      });
    });


    // Next steps: Error handling using the error object
  }

  componentDidUpdate() {
    // document.title = `You clicked ${this.state.count} times`;
    // this.setState({ msg: this.state.msg.concat([ " - aafaaa"])  })
    
  }



  render() {
    // let meetingId = this.state.meetingId ?? "";
    // let userPrincipleName = this.state.userName ?? "";

    // let now = Date.now()
    // let hours = now.getHours()
    // let minutes = now.getMinutes()

    return (
      <div>
        <h1>Tiago Gama : </h1>

        

        {this.state.msg.map((msg) => (
          <><h2>{Date().toLocaleLowerCase().split(' ')[4] + "  :  " + msg}</h2><h2>--------------------</h2></>
        ))}

        <button onClick={() => this.setState({ msg: this.state.msg.concat([" - aafaaa"]) })}>click me</button>
        {/* <h1>In-meeting app sample</h1>
      <h1>HELOOOOOOOOOOOOOOOOOOOOOOO55555OO</h1>
      <h3>Principle Name:</h3>
      <p>{userPrincipleName}</p>
      <h3>Meeting ID:</h3>
      <p>{meetingId}</p> */}

        {/* <MediaQuery maxWidth={280}>
          <h3>This is the side panel</h3>
          <a href="https://docs.microsoft.com/en-us/microsoftteams/platform/apps-in-teams-meetings/teams-apps-in-meetings">Need more info, open this document in new tab or window.</a>
        </MediaQuery> */}
      </div>
    );
  }
}

export default Tab;