import React, {useEffect, useState} from 'react'

const RecordingsPage =()=>{
    const [recordings, setRecordings] = useState<number[]>([]);
    useEffect(()=>{
        const testRecordings = [1,2,3];
        setRecordings(testRecordings);
    })
    return(
        <>
        <h1>RECORDINGS</h1>
        <div>
            <ul>
            {recordings.map((x) => 
            <li>
                {x}
            </li>)}
            </ul>
        </div>
        </>
    );

}
export default RecordingsPage