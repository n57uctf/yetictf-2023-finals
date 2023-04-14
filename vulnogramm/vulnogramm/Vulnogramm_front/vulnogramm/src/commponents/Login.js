import React, {useState} from "react";
import axios from 'axios';
import PropTypes from 'prop-types';



async function loginUser(credentials) {
    return fetch(`${window.location.origin}/backend/authentication`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json());
}

export default function Login({setToken}){

    const [login, setLogin] = useState();
    const [password, setPassword] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        let token = await loginUser({
            login,
            password
          });
        
       
          let myObject = JSON.stringify(token);
          if( myObject === '{"errorText":"Invalid username or password."}' || myObject.startsWith('{"type":"https://tools.ietf.org/html/rfc7231#section-6.5.1","title":"One or more validation errors occurred."') )
          {
            myObject = null;
          }
          
        localStorage.setItem('jwt',myObject);
        setToken(myObject);
    }
    
    function registrate()
    {
        const url = `${window.location.origin}/backend/adduser`;
        return axios.post(url,{
            login,
            password
        }).then(response => console.log(response.status));
    }

    

    return (
            <div>
                <div className="logwin">
                    <div>
                        <input id="login" type="text" className="TextPlace"  onChange={e => setLogin(e.target.value)}></input>
                    </div>
                    <div>
                        <input id="password" type="password" className="TextPlace" onChange={e => setPassword(e.target.value)}></input>
                    </div>
                    <div>
                        <button type="submit" id = "submit" onClick ={handleSubmit} hidden>Login</button>
                        <label for = "submit" className="button">Login</label>
                        <button type="submit" id = "reg" hidden onClick={registrate} >Registrate</button>
                        <label  for = "reg" className="reg" >Registrate</label>
                    </div>
                </div>
            </div>
    );
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
 };
