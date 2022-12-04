import React, { useEffect, useState } from "react";
import { HashRouter as Router, Route } from "react-router-dom";
import Privacy from "./Privacy";
import TermsOfUse from "./TermsOfUse";
import Tab from "./Tab";
import TabConfig from "./TabConfig";
import socketIOClient from "socket.io-client";
// import MessageHandler from "./MessageHandler";
import "./App.css";

/**
 * The main app which handles the initialization and routing
 * of the app.
 */
export default function App() {
  
  const [messages, setMessages] = useState([]);
  const ENDPOINT = "http://127.0.0.1:30992";

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    const c_messages = messages.slice();
    socket.on("Message", msg => {
      // display msg
      c_messages.unshift(msg);
      console.log(msg);

      setMessages(c_messages);
      // call appendMessage method from Tab.jsx
      // this.appendMessage(msg); 

      // Tab.appendMessage(msg);
    });
  });

  return (

    <Router>
      <Route exact path="/privacy" component={Privacy} />
      <Route exact path="/termsofuse" component={TermsOfUse} />
      <Route exact path="/config" component={TabConfig} />
      <Route exact path="/tab" component={() => <Tab msg={messages}/>} />
    </Router>
  );
}
