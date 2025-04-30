import React, { useEffect, useState } from "react";
import FileRow from "../components/FileRow";
import { parseFilePath } from "../utils";

interface Recording {
  s3_filepath: string;
  rec_date: string;
  school: string;
}
const RecordingsPage = () => {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchRecordings = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/recordings/recordings/"
        );
        const data = await response.json();
        console.log(data);
        setRecordings(data);
      } catch (error) {
        console.error("Error fetching: ", error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecordings();
  }, []);
  if (loading) {
    return <div>"Loading"</div>;
  }
  return (
    <div>
      <header className="mb-2">
        <h2 className="text-2xl font-figtree font-bold m-3">Recordings</h2>
      </header>
      <div className="flex justify-center">
        <div className="container items-end border">
          {recordings.map((recording) => (
            <FileRow
              fileName={parseFilePath(recording.s3_filepath)}
              modifiedDate={recording.rec_date}
              fileSize="FILESIZE TODO"
            />
          ))}
        </div>
      </div>
    </div>
  );
};
export default RecordingsPage;
