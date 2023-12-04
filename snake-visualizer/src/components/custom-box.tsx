import React, {useEffect} from 'react';
import { Box } from "@react-three/drei";
import {MathUtils, MeshPhongMaterial, Vector3} from 'three';
import { apple, field, snake, snakeHead } from "../helpers/materials";

const CustomBox = ({ mode, x_index, y_index, max_x, max_y, isDonut }) => {


    const dountRadius = 20
    const dountThickness = 7.5

    const [position, setPosition] = React.useState<Vector3>(new Vector3);
    const [object_mode, setObjectMode] = React.useState<MeshPhongMaterial>(field);
    const [rotationZ, setRotationZ] = React.useState<number>(0);
    const getMaterial = (mode:number) => {        
        switch (mode) {
            case 1:
                return snake;
            case 2:
                return snakeHead
            case 3:
                return field;
            case 4:
                return apple;
        }
        return field;
    }

    const calculate_brick_position = () => {
        if (isDonut){
            let vertical = MathUtils.DEG2RAD * y_index * (360 / max_y);
            let horizontal = MathUtils.DEG2RAD * x_index * (360 / max_x)            
            setRotationZ(horizontal)
            return new Vector3(
                (dountRadius + dountThickness * Math.cos(vertical)) * Math.cos(horizontal),
                (dountRadius + dountThickness * Math.cos(vertical)) * Math.sin(horizontal),
                dountThickness * Math.sin(vertical)
            )
        } else{
            return new Vector3(
                x_index - max_x / 2 + 0.5,
                y_index - max_y / 2 + 0.5,
                0
            )
        }
    }

    useEffect(() => {
        const brickPosition = calculate_brick_position()
        setPosition(brickPosition);
    }, [x_index, y_index, max_x, max_y]);

    useEffect(() => {
        setObjectMode(getMaterial(mode))
    }, [mode])

    const onClick = () => setObjectMode(apple)

    return (
        <Box
            onDoubleClick={onClick}
            position={position}
            key={`${x_index}${y_index}`}
            material={object_mode}
            rotation={[0, 0, rotationZ]}
        />
    );
};

export default React.memo(CustomBox);