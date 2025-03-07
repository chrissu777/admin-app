import React, { useEffect, useState } from "react";

interface Recording{
    s3_filepath: string;
    rec_date: string;
    school: string;
}
const RecordingsPage = () => {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  useEffect(() => {
    const fetchRecordings = async () => {
        const response = await fetch(
            'http://127.0.0.1:8000/api/recordings/recordings/'
        );
        const data = await response.json();
        console.log(data);
        setRecordings(data);
    };
    fetchRecordings();
  }, []);

  return (
    <>
      <h1>RECORDINGS</h1>
      <div>
        <ul>
          {recordings.map((data) => (
            <li>{data.s3_filepath}</li>
          ))}
        </ul>
      </div>
    </>
  );
};
export default RecordingsPage;
