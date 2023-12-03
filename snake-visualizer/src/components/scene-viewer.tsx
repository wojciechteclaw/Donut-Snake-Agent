import {OrbitControls} from '@react-three/drei';
import {useEffect} from 'react';
import {useThree} from 'react-three-fiber';
import {
    AmbientLight,
    Color,
    DirectionalLight,
    Vector3,
} from 'three';



export const SceneViewer = ({setScene}) => {

    const { camera, scene } = useThree();

    useEffect(() => {
        const light1 = new DirectionalLight(0xffeeff, 0.8);
        light1.position.set(1, 1, 1);
        const light2 = new DirectionalLight(0xffffff, 0.8);
        light2.position.set(-1, 0.5, -1);
        const ambientLight = new AmbientLight(0xffffee, 0.25);
        scene.add(...[light1, light2, ambientLight]);
        scene.background = new Color(0xffffff);
        scene.up = new Vector3(0, 0, 1);
        setScene(scene);
    }, [scene]);

    useEffect(() => {
        if (camera) {
            camera.position.set(25, 25, 10);
            camera.lookAt(0, 0, 0);
            camera.far = 5000;
            camera.near = 0.001;
            camera.up = new Vector3(0, 0, 1);
        }
    }, [camera]);


    return (
        <>
            <OrbitControls/>
        </>
    );
}