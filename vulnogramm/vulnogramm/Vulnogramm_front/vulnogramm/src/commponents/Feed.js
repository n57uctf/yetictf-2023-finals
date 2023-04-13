import React, { useState} from 'react';
import Post from './Post';
import Login from './Login';
import Validate from './Validate';
import FeedMaker from './FeedMaker';

export default function Feed() {
  const [showModal, setShowModal] = useState(false);
  const [token, setToken] = useState();

  const toggleShowModal = () => {
    if(!Validate())
    {
      document.getElementById('logout').click();
    }
    setShowModal(!showModal);
  };

  function logout()
  {
    document.cookie = null;
    localStorage.setItem('jwt',null);
    setToken(null);
  }

  if(token==null)
  {
    return <Login setToken={setToken} />
  }

  return(
    <div className='feed'>
      <div id="bar">
        <br></br>
        <button onClick={logout} id='logout' hidden></button>
        <label for='logout' className='logout_style'>Logout</label>
        <label className='feed_label'>Vulnogramm feed</label>
        <Post show={showModal} close_button_click={toggleShowModal} />
        <button id="new_post" onClick={toggleShowModal} hidden></button>
        <label for="new_post" className="btn_post"> New post</label>
        <br></br>
      </div>
      <FeedMaker id={"FeedMaker"}/>
    </div>
  );
}