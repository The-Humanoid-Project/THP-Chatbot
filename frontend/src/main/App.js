import React, { useEffect, useState } from "react";
import "../styles/main.css";
import "../styles/normalize.css";
import { library_data } from "./data";
import logo from "../assets/Humanoid.png";
import user from "../assets/user2.png";
import robot_gif from "../assets/robot2.gif";
import robot_png from "../assets/robot2.png";
import Typewriter from "typewriter-effect";
import ClipLoader from "react-spinners/BeatLoader";

const CSSProperties = {
  display: "block",
  margin: "0 auto",
  borderColor: "red",
};

const App = () => {
  const [input, setInput] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [mode, setMode] = useState("light");
  const [loading, setLoading] = useState(false);
  const [robot, setRobot] = useState(robot_png);
  const [showImg, setShowImg] = useState(false);
  const [img, setImg] = useState();
  const [bookData, setBookData] = useState();

  const changeGif = () => {
    // setRobot(robot_png);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setBookData();
    setImg();
    setChatLog([]);
    setRobot(robot_gif);
    setChatLog([{ user: "me", message: input }]);
    setInput("");
    setLoading(true);

    const response = await fetch(
      "http://localhost:5002/webhooks/rest/webhook",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sender: "user", message: input }),
      }
    );
    const data = await response.json();
    const res = data[0].custom;
    console.log(res);
    let image = <img src={"assets/latestimg.png"} className="latestImg" />;
    setChatLog(
      (prev) => [...prev, { user: "chatgpt", ...res }],
      () => console.log(chatLog)
    );
    if (res?.isImage) {
      setImg(image);
    }
    if (res?.accessionNo) {
      setTimeout(() => setBookData(library_data[res.accessionNo]),5000)
    }
    setLoading(false);
  };
  const clearChat = () => {
    setRobot(robot_png);
    setBookData();
    setImg();
    setLoading(false);
    setChatLog([]);
    location.reload(true)
  };
  const changeMode = () => {
    setMode(mode === "dark" ? "white" : "dark");
  };

  return (
    <div className="app">
      <aside className="side-menu">
        <div className="side-menu-newChat" onClick={clearChat}>
          <span className="plus">+</span> New chat
        </div>
        <div className="side-menu-bottom">
          <hr />
          <div className="side-menu-newChat" onClick={changeMode}>
            <span className="plus">
              <svg
                stroke="currentColor"
                fill="none"
                strokeWidth="2"
                viewBox="0 0 24 24"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-4 w-4"
                height="1em"
                width="1em"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
            </span>
            Light Mode
          </div>
          <a
            href="https://help.openai.com/en/collections/3742473-chatgpt"
            target="_blank"
          >
            <div className="side-menu-newChat">
              <span className="plus">
                <svg
                  stroke="currentColor"
                  fill="none"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="h-4 w-4"
                  height="1em"
                  width="1em"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </span>
              Updates & FAQ
            </div>
          </a>
        </div>
      </aside>
      <section
        className={`chatbox ${mode === "dark" ? "bg-dark" : "bg-white"}`}
      >
        <div className="chat-body">
          <div className="chat-log">
            <h1 className="start-converstion">
              The Humanoid Project
              <br />
              <span className="sub-text">Ask anything</span>
            </h1>
            <div className="botHeader">
              <img src={robot} className="gif-robot" alt="loading..." />
            </div>
            {chatLog.length > 0 ? (
              <ChatQuestion message={chatLog[0]} mode={mode} />
            ) : (
              <div></div>
            )}
            {loading ? (
              <div className="loaderBody">
                <ClipLoader
                  color="#862442"
                  loading={loading}
                  cssOverride={CSSProperties}
                  size={20}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
              </div>
            ) : (
              <div></div>
            )}
            {chatLog.length > 1 && (
              <ChatMessage
                message={chatLog[1]}
                mode={mode}
                img={img}
                bookData={bookData}
              />
            )}
          </div>
        </div>

        <div className={`chat-input blur`}>
          <div className={`chat-input-div`}>
            <form onSubmit={handleSubmit}>
              <input
                placeholder="Start here"
                className={`chat-input-box ${
                  mode === "dark" ? "bg-dark" : "bg-white"
                }`}
                value={input}
                disabled={loading}
                onChange={(e) => {
                  setInput(e.target.value);
                }}
              />
            </form>
            <span className="chat-input-icon">
              <svg
                stroke="currentColor"
                fill="none"
                strokeWidth="2"
                viewBox="0 0 24 24"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-4 w-4 mr-1"
                height="1.13em"
                width="1.13em"
                xmlns="http://www.w3.org/2000/svg"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </span>
          </div>
          <div className="chat-about">
            <span>Built with ❤️ by the Humanoid Project</span>
          </div>
        </div>
      </section>
    </div>
  );
};
export default App;

const ChatQuestion = ({ message, mode }) => {
  return (
    <div className={`chat-message ${mode === "dark" ? "bg-dark" : "bg-white"}`}>
      <div className="chat-message-center">
        {message.user === "me" ? (
          <img src={user} alt="humanoid" className="avatar" />
        ) : (
          <img src={logo} alt="humanoid" className="humanoidLogo" />
        )}
        <div>
          <div className="message">{message.message}</div>
        </div>
      </div>
    </div>
  );
};

const ChatMessage = ({ message, mode, img, bookData }) => {
  console.log(message.message);
  return (
    <div className={`chat-message ${mode === "dark" ? "bg-dark" : "bg-white"}`}>
      <div className="chat-message-center">
        {message.user === "me" ? (
          <img src={user} alt="humanoid" className="avatar" />
        ) : (
          <img src={logo} alt="humanoid" className="humanoidLogo" />
        )}
        <div>
          <div className="message">
            {img}
            <Typewriter
              onInit={(typewriter) => {
                typewriter.changeDelay(50).typeString(message.message).start();
              }}
            />
            <br />
            <br />
            {bookData && (
              <>
                <div>
                  <b>Title: </b>
                  {bookData.name}
                </div>
                <div>
                  <b>Authors: </b>
                  {bookData.author}
                </div>
                <div>
                  <b>Status: </b>
                  {bookData.status}
                </div>
                <div>
                  <b>Due Date: </b>
                  {bookData.duedate}
                </div>
                <div>
                  <b>Barcode: </b>
                  {bookData.barcode}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
