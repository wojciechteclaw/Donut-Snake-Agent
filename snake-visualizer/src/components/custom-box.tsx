import React, {useEffect} from 'react';
import { Box } from "@react-three/drei";
import {MathUtils, MeshPhongMaterial, Vector3} from 'three';
import { apple, field, snake, snakeHead } from "../helpers/materials";

const CustomBox = ({ mode, x_index, y_index, max_x, max_y, isSphere, sphereRadious= 15 }) => {

    const [position, setPosition] = React.useState<Vector3>(new Vector3);
    const [object_mode, setObjectMode] = React.useState<MeshPhongMaterial>(field);
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
        if (isSphere){
            let angle_v = MathUtils.DEG2RAD* (x_index - max_x / 2) * (360 / max_x);
            let angle_h = MathUtils.DEG2RAD * (y_index - max_y / 2 +0.5) * (180 / max_y - 1)
            return new Vector3(
                sphereRadious * Math.cos(angle_v) * Math.cos(angle_h),
                sphereRadious * Math.sin(angle_v) * Math.cos(angle_h),
                sphereRadious * Math.sin(angle_h)
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
    }, [x_index, y_index, max_x, max_y, sphereRadious]);

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
        />
    );
};

export default React.memo(CustomBox);