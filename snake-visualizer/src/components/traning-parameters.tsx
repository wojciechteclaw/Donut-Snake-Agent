import {FC} from "react";

interface ITraningParameters {
    currentReward: number;
    currentScore: number;
    numberOfGames: number;
    numberOfStepsWithoutFood: number;
    numberOfSteps: number;
    status: number;
}

export const TraningParameters:FC<ITraningParameters> = ({
    status,
    currentReward,
    currentScore,
    numberOfGames,
    numberOfSteps,
    numberOfStepsWithoutFood
                                                         }) => {

    const style = {
        top: '0.5rem',
        left: '2rem',
        fontSize: '2rem',
        color: 'black',
    }

    const getStatus = (status:number) => {
        switch (status) {
            case 0:
                return <p style={{color:'red'}}>Lost</p>;
            case 1:
                return <p style={{color:'green'}}>Running</p>;
        }
    }

    return <>
        <div style={{position: "absolute", zIndex:100}}>
            <div style={style}>
                <p>{getStatus(status)}</p>
                <p>No food steps#: <b>{numberOfStepsWithoutFood}</b></p>
                <p>Steps#: <b>{numberOfSteps}</b></p>
                <p>Games#: <b>{numberOfGames ? numberOfGames:0}</b></p>
                <p>Reward: <b>{Math.round(currentReward * 1000) / 1000}</b></p>
                <p>Score: <b>{currentScore}</b></p>
            </div>
        </div>
    </>
}