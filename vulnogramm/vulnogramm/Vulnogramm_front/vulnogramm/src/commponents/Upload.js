import React, { handleChangeFile, handleFile, useState } from 'react'
import axios from 'axios';

export default function Home ({setPhoto}){



  handleFile = (e) => {      
    const content = e.target.result;
    console.log(content);
    setPhoto(content);
  }
    
  handleChangeFile = (file) => {
      let fileData = new FileReader();
      fileData.onloadend = handleFile;
      fileData.readAsDataURL(file); 
  }



    return (
      <div >
          <form onSubmit={e => this.submit(e)}>  
            <input type="file" accept="image/png,image/bmp,image/svg" id="upload" hidden  onChange={e => handleChangeFile(e.target.files[0])}></input>
            <label id="upload_label" for="upload" className="button">Choose your photo</label>
          </form> 
      </div>
    );

}



