import {Component} from "react";
import Image from "./ImageDialog";

export class Table extends Component{
    render() {
        return(
            <div>
                {this.props.Table.map(el =>(<Image key={el.props.photoData.id} item={el} />))}
            </div>
        )
    }
}
export default Table