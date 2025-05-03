import React, { useEffect, useState } from "react";
import FileRow from "../components/FileRow";
import { parseFilePath } from "../utils";

interface Recording {
  id: number;
  s3_filepath: string;
  rec_date: string;
  school: string;
}
const getCamId = (name: string): string => {
  const parts: string[] = name.split("*");
  const camId = parts[2];
  return camId;
};

const RecordingsPage = () => {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  // const [selected, setSelected] = useState<Recording | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const fetchRecordings = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/recordings/");
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
        <h2 className="text-2xl font-figtree font-bold m-3 ml-40">Recordings: Click to Download</h2>
      </header>
      {/* {selected && (
        <div className="mb-6 flex justify-center">
          <video
            controls
            className="w-full max-w-4xl border"
            src={`http://127.0.0.1:8000/api/recordings/${selected.id}/download/`}
          >
            Your browser doesn’t support HTML5 video.
          </video>
        </div>
      )} */}
      <div className="flex justify-center">
        <div className="container items-end border">
          <div className="font-bold">
            <FileRow
              fileName="FILE NAME"
              modifiedDate="DATE MODIFIED"
              camID="CAMERA ID"
            />
          </div>
          {recordings.map((rec) => (
            <a
              key={rec.id}
              href={`http://127.0.0.1:8000/api/recordings/${rec.id}/download/`}
              className="block no-underline hover:bg-gray-50"
            >
              <FileRow
                fileName={parseFilePath(rec.s3_filepath)}
                modifiedDate={rec.rec_date}
                camID={getCamId(rec.s3_filepath)}
              />
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};
export default RecordingsPage;
