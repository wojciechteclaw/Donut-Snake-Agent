import {Simulate} from 'react-dom/test-utils';
import {Canvas} from 'react-three-fiber';
import {useEffect, useState} from "react";
import {ISnake} from '../interfaces/snake.interface';
import {SceneViewer} from "./scene-viewer";
import io from 'socket.io-client';
import {TraningParameters} from "./traning-parameters";
import CustomBox from "./custom-box";
import { Scene } from 'three';
import { AxesHelper } from 'three';


export const ModelViewer = () => {

    const [boxes, setBoxes] = useState({});
    const [environemnt, setEnvironment] = useState<Array<Array<number>>>([]);
    const [xrows, setXRows] = useState<number>(0);
    const [yrows, setYRows] = useState<number>(0);
    const [isSphere, setIsSphere] = useState<boolean>(false);
    const [currentReward, setCurrentReward] = useState<number>(0);
    const [currentScore, setCurrentScore] = useState<number>(0);
    const [currentStatus, setCurrentStatus] = useState<number>(0);
    const [numberOfSteps, setNumberOfSteps] = useState<number>(0);
    const [numberOfStepsWithoutFood, setNumberOfStepsWithoutFood] = useState<number>(0);
    const [numberOfGames, setNumberOfGames] = useState<number>(0);
    const [scene, setScene] = useState<Scene>();

    useEffect(() => {
        const socketInstance = io("localhost:5001/");

        socketInstance.on("connect", () => {
            console.log('connected');
        });

        socketInstance.on("disconnect", () => {
            console.log('disconnected');
        });

        socketInstance.on('new_environment', (data) => {
            const { environment_object,
                    x_rows, 
                    y_rows,
                    is_sphere,
                    is_alive,
                    reward,
                    score,
                    number_of_steps,
                    number_of_steps_without_food,
                    number_of_games} = data;
            setEnvironment(environment_object);
            setXRows(x_rows);
            setYRows(y_rows);
            setIsSphere(is_sphere);
            setCurrentStatus(is_alive ? 1 : 0);
            setCurrentReward(reward);
            setCurrentScore(score);
            setNumberOfSteps(number_of_steps);
            setNumberOfStepsWithoutFood(number_of_steps_without_food);
            setNumberOfGames(number_of_games);

        });

    }, [])

    useEffect(() => createNewBoard(), [environemnt])

    const createNewBoard = () => {
        const boxesEnv = {}
        for (let i = 0; i < xrows; i++){
            for (let j = 0; j < yrows; j++){
                boxesEnv[`${i}-${j}`] = <CustomBox key={`${i}-${j}`}
                                                   x_index={i}
                                                   y_index={j}
                                                   max_x={xrows}
                                                   max_y={yrows}
                                                   mode={environemnt[i][j]}
                                                   isSphere={isSphere}
                                                   />
            }
        }
        setBoxes({...boxesEnv});
    }

    const canvasStyle = {
        height: '100%',
        width: '100%',
    }

    useEffect(() => {
        if (scene) {
            const helper = new AxesHelper(5);
            scene.add(helper);
        }
    }, [scene])

    return <>
        <TraningParameters  currentReward={currentReward} 
                            status={currentStatus} 
                            currentScore={currentScore}
                            numberOfGames={numberOfGames}
                            numberOfSteps={numberOfSteps}
                            numberOfStepsWithoutFood={numberOfStepsWithoutFood}
                            />
        <Canvas style={canvasStyle}>
            {Object.values(boxes)}
            <SceneViewer setScene={setScene}/>
        </Canvas>
    </>
}