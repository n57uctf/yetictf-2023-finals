import React,{useState} from "react";
import Home from "./Upload";
import './Post.css';
import Validate from "./Validate";
export default function Post({show, close_button_click})
{
  const [photo,setPhoto] = useState();
  const [sign, setSign] = useState();
  const [subscript, setSubscript] = useState();

 function newPost(credentials) {
    return fetch('https://localhost:7180/api/Post', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json());
}


  if (!show) {
    return null;
  }

  function new_post()
  {
    if(!Validate())
    {
      document.getElementById('logout').click();
    }
    let owner = localStorage.getItem('jwt');
    owner = JSON.parse(owner);
    owner =  owner.login;
    let checked = document.querySelector('input[name="sign"]:checked');
    let method = 0; 
    if( checked ){ method = checked.dataset.method - '0'; }
    console.log(1);
    const post = newPost({
      photo,
      owner,
      method,
      sign,
      subscript
    });
  }

  return(
    <div className="modal-wrapper">
    <div className="modal">
      <div className="body">
        <img></img>
        <div>
            <label>Sign:
            <input id="sign" type="text" className="text" maxLength="32" onChange={e => setSign(e.target.value)} ></input>
              </label>
        </div>
          <br></br>
        <div>
          <label>Subscript:
            <input id="subscript" type="text" className="text" maxLength="32" onChange={e => setSubscript(e.target.value)}></input>
          </label>
        </div>
        <form>
          <p>Choose Method:</p>
          <label>1
          <input type="radio" name="sign" data-method='0'></input>
            </label><label>2
          <input type="radio" name="sign" data-method='1'></input>
          </label><label>3
          <input type="radio" name="sign" data-method='2'></input>
          </label>
        </form>
      </div>
      <div className="footer">
        <button id='close_button' onClick={close_button_click} hidden></button>
        <label for='close_button' className="close_button"> Close</label>

        <Home setPhoto={setPhoto}/>

        <button id='new_post' hidden onClick={new_post}></button>
        <label for='new_post' id="new_post"> New Post</label>
      </div>
    </div>
  </div>
  );
}