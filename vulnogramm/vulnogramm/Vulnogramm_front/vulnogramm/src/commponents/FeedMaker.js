import Table from "./ImageTable";
import Image from "./ImageDialog";
import React from 'react';

export default class FeedMaker extends React.Component {
    constructor(props) {
        super(props);
        this.state={
            fullTable: [],
        }
        this.addImage =this.addImage.bind(this);
        this.logFeed = this.logFeed.bind(this);
    }
    componentDidMount() {
        setInterval(()=>{this.logFeed();
            }, 5000
        );
    }

    async logFeed() {
        function makeFeed() {
            return fetch('https://localhost:7180/feed', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            })
                .then(data => data.json());
        }
        const AllPosts = await makeFeed();
        let newPosts = [];
        this.setState( {fullTable: []}, function (){console.log("clean success")});
        for (let i = AllPosts.length; i--;)
        {
            newPosts = newPosts.concat(<Image photoData={AllPosts[i]}/>);
        }
        this.setState( {fullTable: newPosts}, function (){console.log("add success")});
        return newPosts;
    }
    
    async addImage(img) {
        console.log(img);
        this.setState( {fullTable: this.state.fullTable.concat(<Image photoData={img}/>)}, function (){console.log("add success")});
    };
    render() {
        return (
            <div className="divFeed">
                <Table Table={this.state.fullTable} />
            </div>
        );
    }
}