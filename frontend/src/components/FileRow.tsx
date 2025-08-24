import React from "react";
import { parseFilePath } from "../utils";

interface fileRowProps {
  fileName: string;
  modifiedDate: string;
  camID: string;
}
const FileRow = ({ fileName, modifiedDate, camID }: fileRowProps) => {
  const schoolName = parseFilePath(fileName);
  return (
  <div className="flex items-center p-2 border-b hover:bg-gray-50">
        <div className="mr-4">
            <span>{schoolName}</span>
        </div>
        <div className="mx-4">
            <span>{modifiedDate}</span>
        </div>
        <div className="ml-4">
            <span>{camID}</span>
        </div>
  </div>

  );
};

export default FileRow;
