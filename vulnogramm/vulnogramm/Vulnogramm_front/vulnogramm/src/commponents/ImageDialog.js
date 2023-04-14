import {Component} from "react";
import { saveAs} from 'file-saver';
import Validate from './Validate';

async function showPost(credentials) {
    return fetch(`${window.location.origin}/backend/yourpost`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${JSON.parse(localStorage.getItem('jwt'))['access_token']}`
        },
        body: JSON.stringify(credentials)
    })
        .then(data => data.json());
}

export class Image extends Component{
    constructor(props) {
        super(props);
        this.state={
            isOpen : false,
            AllData: this.props.item.props.photoData,
            mainPhoto: "",
            dialogPhoto: ""
        }
        this.state.mainPhoto = 'data:image/png;base64,'.concat(this.state.AllData.photoForAll);
        this.state.dialogPhoto = 'data:image/png;base64,'.concat(this.state.AllData.photoForAll);
    }
    handleShowDialog = async () => {
        if (!(await Validate())) {
            document.getElementById('logout').click();
        }
        let owner = localStorage.getItem('jwt');
        owner = JSON.parse(owner);
        owner = owner.login;
        let token = localStorage.getItem('jwt');
        token = JSON.parse(token);
        token = token.access_token;
        const newPhoto = await showPost({
            id: this.state.AllData.id,
            owner: owner,
            token: token
        });
        if (newPhoto != null){
            this.setState({dialogPhoto: 'data:image/png;base64,'.concat(newPhoto.photoForAll)})
        }
        this.setState({isOpen: !this.state.isOpen}, function (){console.log("clicked")});
    };
    saveImage = () => {
        if(!Validate())
        {
            document.getElementById('logout').click();
        }
        let dataURI = this.state.dialogPhoto;
        const byteString = atob(dataURI.split(',')[1]);
        const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], {type: mimeString});
        saveAs(blob, "saved.png");
    }
    render() {
        return(
            <div className={'Image'} key={this.state.AllData.id}>
                <img
                    className="small"
                    src={this.state.mainPhoto}
                    onClick={this.handleShowDialog}
                    alt="no image"
                />
                {this.state.isOpen && (
                    <dialog
                        className="dialog"
                        style={{position: "fixed",
                            top: "50%",
                            left: "50%",
                            background: "#507799",
                            "font-size":"24px",
                            transform: "translate(-50%, -50%)",
                            "border-radius": "4px",
                            "border-color" : "#1e3145",
                            width: "50%",}}
                        open
                        onClick={this.handleShowDialog}
                    >
                        <h1>User : {this.state.AllData.owner}</h1>
                        <img
                            className="image"
                            src={this.state.dialogPhoto}
                            onClick={this.handleShowDialog}
                         alt={"small image"}/>
                        <h1>{this.state.AllData.subscript}</h1>
                        <button id='dialogbutton' className="ButSave"
                                onClick={() => this.saveImage()} hidden></button>
                        <label htmlFor='dialogbutton' className="dialog">Save</label>
                        </dialog>
                )}

            </div>
        )
    }
}
export default Image