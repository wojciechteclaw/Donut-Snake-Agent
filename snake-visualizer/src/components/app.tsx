import {ModelViewer} from "./model-viewer";
import {useState} from "react";

export const App = () => {

    const appStyle = {
        height: '100vh',
        width: '100vw',

    }


    return (
        <div style={appStyle}>
            <ModelViewer/>
        </div>
    )
}